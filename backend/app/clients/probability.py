from datetime import datetime

from base_time import calculate_base_time
from realtime_bus import get_realtime_buses
from weather import get_weather


# 지각 확률 계산
def calculate_late_probability(

    route_id,
    start_station,
    end_station,
    station_id,
    route_name,
    class_time

):

    # 기본 이동시간
    base_result = calculate_base_time(

        route_id,
        start_station,
        end_station

    )

    if "error" in base_result:

        return base_result

    base_time = base_result[
        "base_time"
    ]


    # 실시간 버스 정보
    realtime_result = get_realtime_buses(

        station_id,
        route_name

    )

    if not realtime_result:

        return {

            "error": "실시간 버스 정보 없음"

        }

    # 가장 빨리 오는 버스
    first_bus = realtime_result[0]

    bus_wait = first_bus[
        "predict_time"
    ]


    # 날씨 정보(용인 죽전 기준)
    weather_result = get_weather(
        62,
        123
    )

    weather_delay = 0

    max_rain_percent = 0

    for weather in weather_result:

        rain_percent = weather[
            "rain_percent"
        ]

        if rain_percent > max_rain_percent:

            max_rain_percent = rain_percent

    # 비 확률 기반 지연시간
    if max_rain_percent >= 80:

        weather_delay = 8

    elif max_rain_percent >= 60:

        weather_delay = 6

    elif max_rain_percent >= 30:

        weather_delay = 3


    # 출퇴근 시간 계산
    now = datetime.now()

    current_hour = now.hour

    rush_delay = 0

    # 출근시간
    if 7 <= current_hour < 9:

        rush_delay = 10

    # 퇴근시간
    elif 17 <= current_hour < 19:

        rush_delay = 10


    # 총 예상 시간
    total_time = (

        base_time
        + bus_wait
        + weather_delay
        + rush_delay

    )


    # 수업까지 남은 시간
    remain_time = class_time


    # 시간 차이 계산
    diff = total_time - remain_time


    # 부드러운 확률 계산
    probability = 50 + (diff * 5)

    # 0~100 제한
    if probability < 0:

        probability = 0

    elif probability > 100:

        probability = 100


    return {

        "base_time": base_time,

        "bus_wait": bus_wait,

        "weather_delay": weather_delay,

        "rush_delay": rush_delay,

        "total_time": total_time,

        "remain_time": remain_time,

        "late_probability": probability

    }



# 테스트 코드
if __name__ == "__main__":

    result = calculate_late_probability(

        route_id=241428004,

        start_station="죽전역",

        end_station="단국대",

        station_id=228001028,

        route_name="24",

        # 수업까지 남은 시간(분)
        class_time=25

    )

    print("\n===== 지각 확률 계산 =====\n")

    print(result)