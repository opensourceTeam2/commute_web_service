import requests
import xmltodict


SERVICE_KEY = "85abb6d423ec9823c7eeb463966d478f5e87d56b85e94d77468fb1c1315c7a23"


# 1️⃣ 버스 노선 조회
def get_route_info(bus_number):

    url = (
        "http://ws.bus.go.kr/api/rest/"
        "busRouteInfo/getBusRouteList"
    )

    params = {

        "ServiceKey": SERVICE_KEY,
        "strSrch": bus_number,
        "resultType": "json"

    }

    response = requests.get(
        url,
        params=params
    )

    print("\n[노선조회 URL]")
    print(response.url)

    print("\n[노선조회 응답]")
    print(response.text)

    return response.json()


# 2️⃣ 노선별 정류장 조회
def get_route_stations(route_id):

    url = (
        "http://ws.bus.go.kr/api/rest/"
        "busRouteInfo/getStaionByRoute"
    )

    params = {

        "ServiceKey": SERVICE_KEY,

        "busRouteId": route_id,

        "resultType": "json"

    }

    response = requests.get(
        url,
        params=params
    )

    print("\n[정류장조회 URL]")
    print(response.url)

    print("\n[정류장조회 응답]")
    print(response.text)

    return response.json()


# 3️⃣ 실시간 버스 위치 조회
def get_bus_location(route_id):

    url = (
        "http://ws.bus.go.kr/api/rest/"
        "buspos/getBusPosByRtid"
    )

    params = {

        "ServiceKey": SERVICE_KEY,

        "busRouteId": route_id,

        "resultType": "json"

    }

    response = requests.get(
        url,
        params=params
    )

    print("\n[버스위치 URL]")
    print(response.url)

    print("\n[버스위치 응답]")
    print(response.text)

    return response.json()


# 4️⃣ 버스 도착 예정 정보
def get_arrival_info(station_id, route_id):

    url = (
        "http://ws.bus.go.kr/api/rest/"
        "arrive/getArrInfoByRoute"
    )

    params = {

        "ServiceKey": SERVICE_KEY,

        "stId": station_id,

        "busRouteId": route_id,

        "ord": "1",

        "resultType": "json"

    }

    response = requests.get(
        url,
        params=params
    )

    print("\n[도착정보 URL]")
    print(response.url)

    print("\n[도착정보 응답]")
    print(response.text)

    return response.json()


# 5️⃣ 정류장 검색 / 자동완성
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

    return response.json()



# 테스트 코드
if __name__ == "__main__":

    print("\n===== 1. 버스 노선 조회 =====\n")

    route_data = get_route_info(
        "470"
    )

    print(route_data)


    print("\n===== 2. 정류장 검색 =====\n")

    station_data = search_station(
        "강남역"
    )

    print(station_data)


    # 예시 route_id
    route_id = "100100118"


    print("\n===== 3. 노선별 정류장 조회 =====\n")

    route_station_data = get_route_stations(
        route_id
    )

    print(route_station_data)


    print("\n===== 4. 실시간 버스 위치 조회 =====\n")

    location_data = get_bus_location(
        route_id
    )

    print(location_data)


    # 예시 station_id
    station_id = "111000001"


    print("\n===== 5. 도착 예정 정보 =====\n")

    arrival_data = get_arrival_info(
        station_id,
        route_id
    )

    print(arrival_data)