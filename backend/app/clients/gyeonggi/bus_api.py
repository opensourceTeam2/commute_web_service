import requests

SERVICE_KEY = "KEY"


# 1️⃣ 버스 노선 조회
def get_route_info(route_name):

    url = (
        "http://apis.data.go.kr/6410000/"
        "busrouteservice/v2/"
        "getBusRouteListv2"
    )

    params = {
        "serviceKey": SERVICE_KEY,
        "keyword": route_name,
        "format": "json"
    }

    response = requests.get(url, params=params)

    return response.json()


# 2️⃣ 노선별 정류장 조회
def get_route_stations(route_id):

    url = (
        "http://apis.data.go.kr/6410000/"
        "busrouteservice/v2/"
        "getBusRouteStationListv2"
    )

    params = {
        "serviceKey": SERVICE_KEY,
        "routeId": route_id,
        "format": "json"
    }

    response = requests.get(url, params=params)

    return response.json()


# 3️⃣ 실시간 버스 도착 정보
def get_realtime_arrival(station_id):

    url = (
        "http://apis.data.go.kr/6410000/"
        "busarrivalservice/v2/"
        "getBusArrivalListv2"
    )

    params = {
        "serviceKey": SERVICE_KEY,
        "stationId": station_id,
        "format": "json"
    }

    response = requests.get(url, params=params)

    return response.json()


# 4️⃣ 버스 위치 조회
def get_bus_location(route_id):

    url = (
        "http://apis.data.go.kr/6410000/"
        "buslocationservice/v2/"
        "getBusLocationListv2"
    )

    params = {
        "serviceKey": SERVICE_KEY,
        "routeId": route_id,
        "format": "json"
    }

    response = requests.get(url, params=params)

    return response.json()



# 테스트 코드
if __name__ == "__main__":

    print("\n===== 1. 버스 노선 조회 =====")

    route_data = get_route_info("24")

    print(route_data)

    # 용인 24번 routeId
    route_id = 228000204

    print("\n===== 2. 정류장 조회 =====")

    station_data = get_route_stations(route_id)

    print(station_data)

    print("\n===== 3. 버스 위치 조회 =====")

    location_data = get_bus_location(route_id)

    print(location_data)