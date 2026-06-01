import requests
import json

from app.clients.api_keys import WEATHER_API_KEY


def get_air_data():
    if not WEATHER_API_KEY or WEATHER_API_KEY == "key":
        print("미세먼지 API 키가 없어 기본값으로 처리합니다.")
        return {
            "pm10": 0,
            "status": "unknown",
        }

    url = (
        "http://apis.data.go.kr/"
        "B552584/ArpltnInforInqireSvc/"
        "getMsrstnAcctoRltmMesureDnsty"
    )

    params = {
        "serviceKey": WEATHER_API_KEY,
        "returnType": "json",
        "stationName": "수지",
        "dataTerm": "DAILY",
        "ver": "1.3",
        "numOfRows": 1,
        "pageNo": 1,
    }

    response = requests.get(url, params=params, timeout=10)

    #print("Air status_code:", response.status_code)
    #print("Air content_type:", response.headers.get("Content-Type"))
    #print("Air response_text:", response.text[:500])

    if response.status_code != 200:
        return {
            "pm10": 0,
            "status": "unknown",
        }

    try:
        data = response.json()
    except json.JSONDecodeError:
        return {
            "pm10": 0,
            "status": "unknown",
        }

    try:
        item = data["response"]["body"]["items"][0]
        pm10 = item["pm10Value"]

        if pm10 == "-":
            pm10 = 0
        else:
            pm10 = int(pm10)

        if pm10 <= 30:
            status = "good"
        elif pm10 <= 80:
            status = "normal"
        elif pm10 <= 150:
            status = "bad"
        else:
            status = "very_bad"

        return {
            "pm10": pm10,
            "status": status,
        }

    except Exception as error:
        print("미세먼지 데이터 파싱 실패:", error)
        return {
            "pm10": 0,
            "status": "unknown",
        }