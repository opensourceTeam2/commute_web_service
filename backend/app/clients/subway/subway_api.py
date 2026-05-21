import requests


# 서울 열린데이터광장 지하철 인증키
SERVICE_KEY = "KEY"


# 1️⃣ 지하철 실시간 도착 정보
def get_realtime_arrival(station_name):

    url = (
        f"http://swopenapi.seoul.go.kr/api/subway/"
        f"{SERVICE_KEY}/json/"
        f"realtimeStationArrival/0/20/"
        f"{station_name}"
    )

    response = requests.get(url)

    return response.json()


# 2️⃣ 지하철 실시간 열차 위치 정보
def get_realtime_position(line_name):

    url = (
        f"http://swopenapi.seoul.go.kr/api/subway/"
        f"{SERVICE_KEY}/json/"
        f"realtimePosition/0/20/"
        f"{line_name}"
    )

    response = requests.get(url)

    return response.json()



# 테스트 코드
if __name__ == "__main__":

    print("\n===== 1. 지하철 실시간 도착 정보 =====")

    arrival_data = get_realtime_arrival("죽전")

    print(arrival_data)


    print("\n===== 2. 지하철 실시간 열차 위치 정보 =====")

    position_data = get_realtime_position("수인분당선")

    print(position_data)