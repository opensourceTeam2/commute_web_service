from rail_api import (
    get_subway_route_info
)


# 지하철역 검색
def search_station(
    mreaWideCd,
    lnCd,
    keyword
):

    data = get_subway_route_info(
        mreaWideCd,
        lnCd
    )

    station_list = (
        data
        .get("body", [])
    )

    result = []

    for station in station_list:

        # 레일포털용 이름
        rail_name = station.get(
            "stinNm",
            ""
        )

        # 서울 API용 이름
        realtime_name = (
            rail_name
            .split("(")[0]
        )

        # 사용자 검색
        if keyword in realtime_name:

            result.append({

                # 프론트 표시용
                "display_name":
                realtime_name,

                # 레일포털용
                "rail_name":
                rail_name,

                # 실시간 지하철용
                "realtime_name":
                realtime_name
            })

    return result



# 테스트 코드
if __name__ == "__main__":

    result = search_station(

        # 수도권
        "01",

        # 수인분당선
        "K1",

        # 검색어
        "죽전"
    )

    print("\n===== 지하철역 검색 =====\n")

    for station in result:

        print(station)