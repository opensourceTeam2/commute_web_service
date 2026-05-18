import requests


SERVICE_KEY = "KEY"


# 미세먼지 조회
def get_air_data():

    url = (
        "http://apis.data.go.kr/"
        "B552584/ArpltnInforInqireSvc/"
        "getMsrstnAcctoRltmMesureDnsty"
    )

    params = {

        "serviceKey": SERVICE_KEY,
        "returnType": "json",
        "stationName": "수지",  # 단국대 죽전 근처
        "dataTerm": "DAILY",
        "ver": "1.3",
        "numOfRows": 1,
        "pageNo": 1
    }

    response = requests.get(
        url,
        params=params
    )

    data = response.json()

    item = (
        data["response"]
        ["body"]
        ["items"][0]
    )

    pm10 = item["pm10Value"]

    # 값 없을 경우
    if pm10 == "-":

        pm10 = 0

    else:

        pm10 = int(pm10)

    
    # 상태 판별
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
        "status": status
    }



# 테스트 코드
if __name__ == "__main__":

    print("\n===== 미세먼지 정보 =====\n")

    result = get_air_data()

    print(result)