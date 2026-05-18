import requests


from bus_api import SERVICE_KEY


# 정류장 검색
def search_station(station_name):

    url = (
        "http://ws.bus.go.kr/api/rest/"
        "stationinfo/getStationByName"
    )

    params = {

        "ServiceKey": SERVICE_KEY,
        "stSrch": station_name,
        "resultType": "json"

    }

    response = requests.get(
        url,
        params=params
    )

    print("\n[정류장검색 URL]")
    print(response.url)

    print("\n[정류장검색 응답]")
    print(response.text)

    data = response.json()

    try:

        item_list = (
            data["msgBody"]
            ["itemList"]
        )

        # 결과 1개 처리
        if isinstance(item_list, dict):

            item_list = [item_list]

        result = []

        for item in item_list:

            result.append({

                "station_name": item["stNm"],

                "station_id": item["stId"],

                "ars_id": item["arsId"],

                "gps_x": item["tmX"],

                "gps_y": item["tmY"]

            })

        return result

    except:

        return {
            "error": "정류장을 찾을 수 없습니다"
        }


# 테스트 코드
if __name__ == "__main__":

    print("\n===== 서울 정류장 검색 =====\n")

    result = search_station(
        "강남역"
    )

    print(result)