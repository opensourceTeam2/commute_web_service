from math import radians
from math import sin
from math import cos
from math import sqrt
from math import atan2
from datetime import datetime

from base_time import calculate_base_time
from realtime_bus import get_realtime_buses
from weather import get_weather
from bus_api import get_route_stations


# 거리 계산(m)
def calculate_distance(

    lat1,
    lon1,

    lat2,
    lon2

):

    R = 6371000

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (

        sin(dlat / 2) ** 2

        +

        cos(radians(lat1))
        *

        cos(radians(lat2))
        *

        sin(dlon / 2) ** 2

    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

    return R * c


# 정류장 정보 조회
def get_station_info(

    route_id,
    station_keyword

):

    data = get_route_stations(
        route_id
    )

    station_list = (
        data
        .get("response", {})
        .get("msgBody", {})
        .get("busRouteStationList", [])
    )

    if isinstance(station_list, dict):

        station_list = [station_list]

    for station in station_list:

        station_name = station.get(
            "stationName",
            ""
        )

        if station_keyword in station_name:

            return {

                "station_name": station_name,

                "station_id": station.get(
                    "stationId"
                ),

                "x": station.get("x"),

                "y": station.get("y")

            }

    return None


# 환승 시간 계산
def calculate_transfer_time(

    current_station,

    next_station,

    next_bus_wait

):

    distance = calculate_distance(

        current_station["y"],
        current_station["x"],

        next_station["y"],
        next_station["x"]

    )

    # 도보 시간(분)
    walk_time = distance / 80

    walk_time = round(walk_time)

    print(f"\n환승 거리: {round(distance)}m")
    print(f"도보 시간: {walk_time}분")
    print(f"다음 버스 대기: {next_bus_wait}분")

    # 버스를 탈 수 있음
    if walk_time <= next_bus_wait:

        transfer_time = next_bus_wait

    # 버스를 놓침
    else:

        # 다음 버스 기다림
        transfer_time = next_bus_wait + 10

    return transfer_time


# 버스 1개 계산
def calculate_route_time(route):

    # 기본 이동시간
    base_result = calculate_base_time(

        route["route_id"],

        route["start_station"],

        route["end_station"]

    )

    if "error" in base_result:

        return base_result

    base_time = base_result[
        "base_time"
    ]

    # 실시간 버스
    realtime_result = get_realtime_buses(

        route["station_id"],

        route["route_name"]

    )

    if not realtime_result:

        return {

            "error": "실시간 버스 없음"

        }

    bus_wait = realtime_result[0][
        "predict_time"
    ]

    total = base_time + bus_wait

    return {

        "route_name": route[
            "route_name"
        ],

        "start_station": route[
            "start_station"
        ],

        "end_station": route[
            "end_station"
        ],

        "base_time": base_time,

        "bus_wait": bus_wait,

        "route_total": total

    }


# 환승 포함 지각 확률
def calculate_transfer_probability(

    routes,
    class_time

):

    total_time = 0

    route_results = []

    # 각 버스 계산
    for idx, route in enumerate(routes):

        result = calculate_route_time(
            route
        )

        if "error" in result:

            return result

        total_time += result[
            "route_total"
        ]

        route_results.append(result)

        # 환승 계산
        if idx > 0:

            current_station = get_station_info(

                routes[idx - 1][
                    "route_id"
                ],

                routes[idx - 1][
                    "end_station"
                ]

            )

            next_station = get_station_info(

                route["route_id"],

                route["start_station"]

            )

            realtime = get_realtime_buses(

                route["station_id"],

                route["route_name"]

            )

            if realtime:

                next_bus_wait = realtime[0][
                    "predict_time"
                ]

            else:

                next_bus_wait = 10

            transfer_time = calculate_transfer_time(

                current_station,

                next_station,

                next_bus_wait

            )

            total_time += transfer_time

    # 날씨는 전체 1번만
    weather_result = get_weather(
        62,
        123
    )

    weather_delay = 0

    max_rain = 0

    for weather in weather_result:

        rain = weather[
            "rain_percent"
        ]

        if rain > max_rain:

            max_rain = rain

    if max_rain >= 80:

        weather_delay = 8

    elif max_rain >= 60:

        weather_delay = 5

    elif max_rain >= 30:

        weather_delay = 3

    total_time += weather_delay

    # 출퇴근 시간도 전체 1번만
    now = datetime.now()

    current_hour = now.hour

    rush_delay = 0

    if 7 <= current_hour < 9:

        rush_delay = 10

    elif 17 <= current_hour < 19:

        rush_delay = 10

    total_time += rush_delay

    remain_time = class_time

    diff = total_time - remain_time

    # 부드러운 확률 계산
    probability = 30 + (diff * 5)

    if probability < 0:

        probability = 0

    elif probability > 100:

        probability = 100

    return {

        "routes": route_results,

        "weather_delay": weather_delay,

        "rush_delay": rush_delay,

        "total_time": total_time,

        "remain_time": remain_time,

        "late_probability": probability

    }



# 테스트 코드
if __name__ == "__main__":

    routes = [

    {

        "route_id": 241423001,

        "route_name": "22",

        "start_station": "미금역",

        "end_station": "죽전역",

        "station_id": 206000087

    },

    {

        "route_id": 241428004,

        "route_name": "24",

        "start_station": "죽전역",

        "end_station": "단국대",

        "station_id": 228001028

    }

]

    result = calculate_transfer_probability(

        routes,

        class_time=60

    )

    print("\n===== 환승 지각 확률 =====\n")

    print(result)