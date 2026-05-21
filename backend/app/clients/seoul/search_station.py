from bus_api import (
    get_route_stations
)


# 정류장 검색
def search_station(

    route_id,
    keyword

):

    stations = get_route_stations(
        route_id
    )


    route_stations = (
        stations
        .get("msgBody", {})
        .get("itemList", [])
    )


    # 데이터 1개일 경우
    if isinstance(
        route_stations,
        dict
    ):

        route_stations = [
            route_stations
        ]


    result = []


    for station in route_stations:


        name = station.get(
            "stationNm",
            ""
        )


        # 검색어 포함 여부
        if keyword in name:


            result.append({

                "stationName":
                name,

                "stationSeq":
                station.get(
                    "seq"
                ),

                "stationId":
                station.get(
                    "station"
                ),

                "arsId":
                station.get(
                    "arsId"
                )
            })


    return result



# 테스트 코드
if __name__ == "__main__":


    # 241번 route_id
    route_id = "100100595"


    result = search_station(
        route_id,
        "청량리"

    )


    print("\n===== 서울 정류장 검색 =====\n")

    print(result)