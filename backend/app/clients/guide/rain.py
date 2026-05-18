import requests

from datetime import (
    datetime,
    timedelta
)


SERVICE_KEY = "KEY"


# 발표 날짜/시간 계산
def get_base_datetime():

    now = datetime.now()

    if now.hour < 2:

        base_date = (
            now - timedelta(days=1)
        ).strftime("%Y%m%d")

        base_time = "2300"

    elif now.hour < 5:

        base_date = now.strftime("%Y%m%d")
        base_time = "0200"

    elif now.hour < 8:

        base_date = now.strftime("%Y%m%d")
        base_time = "0500"

    elif now.hour < 11:

        base_date = now.strftime("%Y%m%d")
        base_time = "0800"

    elif now.hour < 14:

        base_date = now.strftime("%Y%m%d")
        base_time = "1100"

    elif now.hour < 17:

        base_date = now.strftime("%Y%m%d")
        base_time = "1400"

    elif now.hour < 20:

        base_date = now.strftime("%Y%m%d")
        base_time = "1700"

    elif now.hour < 23:

        base_date = now.strftime("%Y%m%d")
        base_time = "2000"

    else:

        base_date = now.strftime("%Y%m%d")
        base_time = "2300"

    return {

        "base_date": base_date,
        "base_time": base_time
    }


# 강수확률 조회
def get_rain_probability():

    base_info = get_base_datetime()

    url = (
        "http://apis.data.go.kr/"
        "1360000/VilageFcstInfoService_2.0/"
        "getVilageFcst"
    )

    params = {

        "serviceKey": SERVICE_KEY,
        "pageNo": 1,
        "numOfRows": 1000,
        "dataType": "JSON",
        "base_date": base_info["base_date"],
        "base_time": base_info["base_time"],

        # 단국대 죽전3동
        "nx": 62,
        "ny": 122
    }

    response = requests.get(
        url,
        params=params
    )

    data = response.json()

    items = (
        data["response"]
        ["body"]
        ["items"]
        ["item"]
    )

    now = datetime.now()

    current_hour = now.hour

    # 현재 시간 이후 가장 가까운 강수확률
    for item in items:

        if item["category"] == "POP":

            fcst_time = int(
                item["fcstTime"][:2]
            )

            if fcst_time >= current_hour:

                return {

                    "forecast_time": item["fcstTime"],

                    "rain_percent": int(
                        item["fcstValue"]
                    )
                }

    return {

        "forecast_time": None,
        "rain_percent": 0
    }



# 테스트 코드
if __name__ == "__main__":

    print("\n===== 강수확률 =====\n")

    result = get_rain_probability()

    print(result)