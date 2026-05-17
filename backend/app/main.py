from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.clients.gyeonggi.bus_api import (
    get_route_info,
    get_route_stations,
    get_realtime_arrival,
)
from app.clients.weather import get_weather


app = FastAPI()

# React 프론트엔드에서 FastAPI 백엔드로 요청할 수 있게 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CommuteRequest(BaseModel):
    busStop: str
    busNumber: str
    classStartTime: str
    loginId: str | None = None


@app.get("/")
def read_root():
    return {"Hello": "OpenSource"}


def to_list(value):
    if value is None:
        return []
    if isinstance(value, dict):
        return [value]
    return value


def parse_class_start_time(class_start_time):
    """
    예시:
    오전 09:00
    오후 01:30
    """
    period, time_text = class_start_time.split(" ")
    hour, minute = map(int, time_text.split(":"))

    if period == "오후" and hour != 12:
        hour += 12
    if period == "오전" and hour == 12:
        hour = 0

    now = datetime.now()
    class_datetime = now.replace(
        hour=hour,
        minute=minute,
        second=0,
        microsecond=0,
    )

    # 이미 지난 시간이면 다음 날 수업으로 계산
    if class_datetime < now:
        class_datetime += timedelta(days=1)

    return int((class_datetime - now).total_seconds() // 60)


def find_route_id(bus_number, bus_stop):
    data = get_route_info(bus_number)

    route_list = (
        data
        .get("response", {})
        .get("msgBody", {})
        .get("busRouteList", [])
    )

    route_list = to_list(route_list)

    if not route_list:
        raise ValueError("해당 버스 번호의 노선을 찾을 수 없습니다.")

    print("노선 후보 개수:", len(route_list))

    for route in route_list:
        route_name = str(route.get("routeName"))
        route_id = route.get("routeId")

        print("노선 후보:", route_name, route_id)

        if route_name != str(bus_number):
            continue

        station_data = get_route_stations(route_id)

        station_list = (
            station_data
            .get("response", {})
            .get("msgBody", {})
            .get("busRouteStationList", [])
        )

        station_list = to_list(station_list)

        start_candidates = []

        for station in station_list:
            station_name = station.get("stationName", "")

            if bus_stop in station_name:
                start_candidates.append(station)

        print("출발 정류장 후보:", [
            {
                "stationName": s.get("stationName"),
                "stationSeq": s.get("stationSeq"),
            }
            for s in start_candidates
        ])

        for start_station in start_candidates:
            start_seq = int(start_station.get("stationSeq"))

            for station in station_list:
                station_name = station.get("stationName", "")
                station_seq = int(station.get("stationSeq"))

                if "단국대" in station_name and station_seq > start_seq:
                    print("선택된 노선:", route_id)
                    print("선택된 출발:", start_station.get("stationName"), start_seq)
                    print("선택된 도착:", station_name, station_seq)
                    return route_id

    raise ValueError(
        f"{bus_number}번 노선 중 '{bus_stop}' 이후에 단국대 정류장이 나오는 노선을 찾을 수 없습니다."
    )


def find_station(route_id, bus_stop):
    data = get_route_stations(route_id)

    station_list = (
        data
        .get("response", {})
        .get("msgBody", {})
        .get("busRouteStationList", [])
    )

    station_list = to_list(station_list)

    if not station_list:
        raise ValueError("해당 노선의 정류장 목록을 찾을 수 없습니다.")

    for station in station_list:
        station_name = station.get("stationName", "")

        if bus_stop in station_name:
            return {
                "stationId": station.get("stationId"),
                "stationName": station_name,
                "stationSeq": int(station.get("stationSeq")),
            }

    raise ValueError("입력한 정류장을 해당 버스 노선에서 찾을 수 없습니다.")


def find_end_station_after_start(route_id, start_seq):
    """
    도착지는 단국대가 들어간 정류장으로 임시 고정.
    출발 정류장보다 뒤에 나오는 단국대 정류장을 찾음.
    """
    data = get_route_stations(route_id)

    station_list = (
        data
        .get("response", {})
        .get("msgBody", {})
        .get("busRouteStationList", [])
    )

    station_list = to_list(station_list)

    for station in station_list:
        station_name = station.get("stationName", "")

        if "단국대" in station_name:
            station_seq = int(station.get("stationSeq"))

            if station_seq > start_seq:
                return {
                    "stationName": station_name,
                    "stationSeq": station_seq,
                }

    raise ValueError("출발 정류장 이후의 단국대 정류장을 찾을 수 없습니다.")


def get_bus_wait_time(station_id, bus_number):
    data = get_realtime_arrival(station_id)

    arrival_list = (
        data
        .get("response", {})
        .get("msgBody", {})
        .get("busArrivalList", [])
    )

    arrival_list = to_list(arrival_list)

    if not arrival_list:
        raise ValueError("실시간 버스 도착 정보가 없습니다.")

    for bus in arrival_list:
        if str(bus.get("routeName")) == str(bus_number):
            predict_time = bus.get("predictTime1")

            if predict_time is not None and predict_time != "":
                return int(predict_time)

    raise ValueError("해당 버스의 실시간 도착 정보를 찾을 수 없습니다.")


def get_weather_delay():
    """
    용인 죽전 기준 nx=62, ny=123
    날씨 API가 실패하면 일단 지연시간 0으로 처리
    """
    try:
        weather_list = get_weather(62, 123)
    except Exception:
        return 0

    max_rain_percent = 0

    for weather in weather_list:
        rain_percent = int(weather.get("rain_percent", 0))

        if rain_percent > max_rain_percent:
            max_rain_percent = rain_percent

    if max_rain_percent >= 80:
        return 8
    elif max_rain_percent >= 60:
        return 6
    elif max_rain_percent >= 30:
        return 3

    return 0


def get_rush_delay():
    current_hour = datetime.now().hour

    if 7 <= current_hour < 9:
        return 10
    if 17 <= current_hour < 19:
        return 10

    return 0


@app.post("/api/commute/calculate")
def calculate_commute(request: CommuteRequest):
    print("\n========== 통학 계산 요청 시작 ==========")
    print("요청값:", request)

    try:
        print("1단계: route_id 찾기 시작")
        route_id = find_route_id(request.busNumber, request.busStop)
        print("1단계 성공 route_id:", route_id)

        print("2단계: 출발 정류장 찾기 시작")
        start_station = find_station(
            route_id=route_id,
            bus_stop=request.busStop,
        )
        print("2단계 성공 start_station:", start_station)

        print("3단계: 단국대 도착 정류장 찾기 시작")
        end_station = find_end_station_after_start(
            route_id=route_id,
            start_seq=start_station["stationSeq"],
        )
        print("3단계 성공 end_station:", end_station)

        station_count = end_station["stationSeq"] - start_station["stationSeq"]
        base_time = station_count * 2
        print("4단계 base_time:", base_time)

        print("5단계: 실시간 버스 도착 정보 찾기 시작")
        bus_wait = get_bus_wait_time(
            station_id=start_station["stationId"],
            bus_number=request.busNumber,
        )
        print("5단계 성공 bus_wait:", bus_wait)

        print("6단계: 날씨 지연 계산 시작")
        weather_delay = get_weather_delay()
        print("6단계 성공 weather_delay:", weather_delay)

        rush_delay = get_rush_delay()
        print("7단계 rush_delay:", rush_delay)

        total_time = base_time + bus_wait + weather_delay + rush_delay
        remain_time = parse_class_start_time(request.classStartTime)

        diff = total_time - remain_time
        late_probability = 50 + diff * 5

        if late_probability < 0:
            late_probability = 0
        elif late_probability > 100:
            late_probability = 100

        late_probability = round(late_probability)

        if late_probability >= 70:
            status_message = "지각 위험이 높습니다. 조금 더 빨리 출발하는 것이 좋습니다."
        elif late_probability >= 40:
            status_message = "지각 가능성이 있습니다. 버스 도착 시간을 주의해서 확인하세요."
        else:
            status_message = "현재 기준으로는 지각 위험이 낮습니다."

        print("========== 통학 계산 성공 ==========\n")

        return {
            "busStop": start_station["stationName"],
            "busNumber": request.busNumber,
            "classStartTime": request.classStartTime,
            "arrivalMinutes": bus_wait,
            "lateProbability": late_probability,
            "statusMessage": status_message,
            "checkedAt": datetime.now().strftime("%Y. %m. %d. %H:%M:%S"),
            "routeId": route_id,
            "stationId": start_station["stationId"],
            "endStation": end_station["stationName"],
            "baseTime": base_time,
            "busWait": bus_wait,
            "weatherDelay": weather_delay,
            "rushDelay": rush_delay,
            "totalTime": total_time,
            "remainTime": remain_time,
        }

    except ValueError as error:
        print("400 에러 원인:", str(error))
        print("========== 통학 계산 실패 ==========\n")
        raise HTTPException(status_code=400, detail=str(error))

    except Exception as error:
        print("500 에러 원인:", str(error))
        print("========== 통학 계산 실패 ==========\n")
        raise HTTPException(
            status_code=500,
            detail=f"통학 계산 중 오류가 발생했습니다: {error}",
        )