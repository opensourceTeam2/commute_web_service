from rail_api import get_subway_route_info


# 역 하나당 평균 이동 시간(분)
AVERAGE_MIN_PER_STATION = 2


def get_all_station_orders(
    stations,
    station_name
):

    route_stations = (
        stations
        .get("body", [])
    )

    result = []

    for station in route_stations:

        name = station.get(
            "stinNm",
            ""
        )

        # 역 이름 포함 검사
        if station_name in name:

            result.append({

                "stationOrder": int(
                    station.get(
                        "stinConsOrdr"
                    )
                ),

                "stationName": name
            })

    return result


def calculate_base_time(
    mreaWideCd,
    lnCd,
    start_station,
    end_station
):

    stations = get_subway_route_info(
        mreaWideCd,
        lnCd
    )

    # API 오류 확인
    if "error" in stations:

        return stations

    # 출발역 후보
    start_candidates = (
        get_all_station_orders(
            stations,
            start_station
        )
    )

    # 도착역 후보
    end_candidates = (
        get_all_station_orders(
            stations,
            end_station
        )
    )

    if (
        not start_candidates
        or
        not end_candidates
    ):

        return {
            "error": "역을 찾을 수 없습니다"
        }

    # 첫 번째 출발역 사용
    start_order = (
        start_candidates[0]
        ["stationOrder"]
    )

    # 출발 이후 도착역 찾기
    end_order = None

    for end in end_candidates:

        if (
            end["stationOrder"]
            >
            start_order
        ):

            end_order = (
                end["stationOrder"]
            )

            break

    if end_order is None:

        return {
            "error":
            "올바른 방향의 도착역을 찾을 수 없습니다"
        }

    # 역 개수 계산
    station_count = (
        end_order
        -
        start_order
    )

    # 기본 이동시간 계산
    base_time = (
        station_count
        *
        AVERAGE_MIN_PER_STATION
    )

    return {

        "start_station": start_station,
        "end_station": end_station,

        "start_order": start_order,
        "end_order": end_order,

        "station_count": station_count,

        "base_time": base_time
    }



# 테스트 코드
if __name__ == "__main__":

    result = calculate_base_time(

        # 수도권
        "01",

        # 수인분당선
        "K1",

        # 출발역
        "미금",

        # 도착역
        "죽전"
    )

    print("\n===== 기본 이동시간 계산 =====\n")

    print(result)