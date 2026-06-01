import requests
import json
from datetime import datetime, timedelta

from app.clients.api_keys import WEATHER_API_KEY


def get_base_datetime():
    now = datetime.now()

    if now.hour < 2:
        base_date = (now - timedelta(days=1)).strftime("%Y%m%d")
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
        "base_time": base_time,
    }


def get_rain_probability():
    if not WEATHER_API_KEY or WEATHER_API_KEY == "key":
        print("강수확률 API 키가 없어 기본값으로 처리합니다.")
        return {
            "forecast_time": None,
            "rain_percent": 0,
        }

    base_info = get_base_datetime()

    url = (
        "http://apis.data.go.kr/"
        "1360000/VilageFcstInfoService_2.0/"
        "getVilageFcst"
    )

    params = {
        "serviceKey": WEATHER_API_KEY,
        "pageNo": 1,
        "numOfRows": 1000,
        "dataType": "JSON",
        "base_date": base_info["base_date"],
        "base_time": base_info["base_time"],
        "nx": 62,
        "ny": 122,
    }

    response = requests.get(url, params=params, timeout=10)

    #print("Rain status_code:", response.status_code)
    #print("Rain content_type:", response.headers.get("Content-Type"))
    #print("Rain response_text:", response.text[:500])

    if response.status_code != 200:
        return {
            "forecast_time": None,
            "rain_percent": 0,
        }

    try:
        data = response.json()
    except json.JSONDecodeError:
        return {
            "forecast_time": None,
            "rain_percent": 0,
        }

    try:
        items = data["response"]["body"]["items"]["item"]
        now = datetime.now()
        current_hour = now.hour

        for item in items:
            if item["category"] == "POP":
                fcst_time = int(item["fcstTime"][:2])

                if fcst_time >= current_hour:
                    return {
                        "forecast_time": item["fcstTime"],
                        "rain_percent": int(item["fcstValue"]),
                    }

        return {
            "forecast_time": None,
            "rain_percent": 0,
        }

    except Exception as error:
        print("강수확률 데이터 파싱 실패:", error)
        return {
            "forecast_time": None,
            "rain_percent": 0,
        }