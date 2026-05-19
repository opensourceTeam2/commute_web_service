import requests


# 공공데이터포털 인증키
SERVICE_KEY = ("KEY")


# 1️⃣ 버스 노선 조회
def get_route_info(
    bus_number
):

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

    return response.json()



# 2️⃣ 정류장 검색
def search_station(
    station_name
):

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

    return response.json()



# 3️⃣ 노선별 정류장 조회
def get_route_stations(
    route_id
):

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

    return response.json()



# 4️⃣ 실시간 버스 위치 조회
def get_bus_location(
    route_id
):

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

    return response.json()



# 5️⃣ 도착 예정 정보 조회
def get_arrival_info(

    station_id,
    route_id,
    order
):

    url = (
        "http://ws.bus.go.kr/api/rest/"
        "arrive/getArrInfoByRoute"
    )

    params = {

        "ServiceKey": SERVICE_KEY,
        "stId": station_id,
        "busRouteId": route_id,
        "ord": order,
        "resultType": "json"
    }

    response = requests.get(
        url,
        params=params
    )

    return response.json()



# 테스트 코드
if __name__ == "__main__":


    print("\n===== 1. 버스 노선 조회 =====\n")

    route_data = get_route_info(
        "241"
    )

    print(route_data)


    # 241 route_id
    route_id = "100100595"


    print("\n===== 2. 정류장 조회 =====\n")

    station_data = get_route_stations(
        route_id
    )

    print(station_data)


    print("\n===== 3. 버스 위치 조회 =====\n")

    location_data = get_bus_location(
        route_id
    )

    print(location_data)


    print("\n===== 4. 상봉역 정류장 검색 =====\n")

    search_data = search_station(
        "상봉역"
    )

    print(search_data)


    # 상봉역.중랑우체국
    station_id = "106000004"
    station_order = "102"


    print("\n===== 5. 도착 예정 정보 =====\n")

    arrival_data = get_arrival_info(

        station_id,
        route_id,
        station_order
    )

    print(arrival_data)