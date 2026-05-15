import requests
from datetime import datetime


SERVICE_KEY = "KEY"


def get_weather(nx, ny):

    now = datetime.now()

    base_date = now.strftime("%Y%m%d")

    hour = now.strftime("%H")

    # 초단기예보 발표시간
    base_time = f"{hour}30"

    url = (
        "http://apis.data.go.kr/"
        "1360000/VilageFcstInfoService_2.0/"
        "getUltraSrtFcst"
    )

    params = {

        "serviceKey": SERVICE_KEY,

        "pageNo": 1,

        "numOfRows": 100,

        "dataType": "JSON",

        "base_date": base_date,

        "base_time": base_time,

        "nx": nx,

        "ny": ny

    }

    response = requests.get(
        url,
        params=params
    )

    data = response.json()

    items = (
        data
        .get("response", {})
        .get("body", {})
        .get("items", {})
        .get("item", [])
    )

    weather_dict = {}

    for item in items:

        fcst_time = item.get("fcstTime")
        category = item.get("category")
        value = item.get("fcstValue")

        # 시간별 데이터 저장
        if fcst_time not in weather_dict:

            weather_dict[fcst_time] = {

                "rain_percent": 0,
                "rain_type": "없음"

            }

        # 강수확률
        if category == "POP":

            weather_dict[fcst_time][
                "rain_percent"
            ] = int(value)

        # 강수형태
        elif category == "PTY":

            if value == "1":

                weather_dict[fcst_time][
                    "rain_type"
                ] = "비"

            elif value == "2":

                weather_dict[fcst_time][
                    "rain_type"
                ] = "비/눈"

            elif value == "3":

                weather_dict[fcst_time][
                    "rain_type"
                ] = "눈"

    result = []

    count = 0

    # 1~3시간 데이터만 사용
    for time, info in weather_dict.items():

        result.append({

            "forecast_time": time,

            "rain_percent": info[
                "rain_percent"
            ],

            "rain_type": info[
                "rain_type"
            ]

        })

        count += 1

        if count == 3:
            break

    return result



# 테스트 코드
if __name__ == "__main__":

    # 용인
    nx = 62
    ny = 123

    result = get_weather(
        nx,
        ny
    )

    print("\n===== 날씨 예보 =====\n")

    for weather in result:

        print(weather)