from bus_api import get_route_stations


def search_station(route_id, keyword):

    stations = get_route_stations(route_id)

    route_stations = (
        stations
        .get("response", {})
        .get("msgBody", {})
        .get("busRouteStationList", [])
    )

    result = []

    for station in route_stations:

        name = station.get("stationName", "")

        if keyword in name:

            result.append({
                "stationName": name,
                "stationSeq": station.get("stationSeq"),
                "stationId": station.get("stationId")
            })

    return result



# 테스트 코드
if __name__ == "__main__":

    route_id = 241428004

    result = search_station(
        route_id,
        "미금"
    )

    print(result)