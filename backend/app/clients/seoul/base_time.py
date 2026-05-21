from app.clients.seoul.bus_api import get_route_stations


# 정류장 하나당 평균 이동 시간(분)
AVERAGE_MIN_PER_STATION = 2



# 정류장 순서 찾기
def get_all_station_sequences(

    stations,
    station_name

):

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


        if station_name in name:

            result.append({

                "stationSeq":
                int(
                    station.get(
                        "seq",
                        0
                    )
                ),

                "stationName":
                name
            })


    return result



# 기본 이동 시간 계산
def calculate_base_time(

    route_id,
    start_station,
    end_station

):

    stations = get_route_stations(
        route_id
    )


    # 출발 정류장 후보
    start_candidates = (
        get_all_station_sequences(

            stations,
            start_station
        )
    )


    # 도착 정류장 후보
    end_candidates = (
        get_all_station_sequences(

            stations,
            end_station
        )
    )


    if (
        not start_candidates
        or not end_candidates
    ):

        return {

            "error":
            "정류장을 찾을 수 없습니다"

        }


    # 가장 첫 출발 정류장 사용
    start_seq = (
        start_candidates[0]
        ["stationSeq"]
    )


    # 출발 이후에 오는 도착 정류장 선택
    end_seq = None


    for end in end_candidates:

        if (
            end["stationSeq"]
            > start_seq
        ):

            end_seq = (
                end["stationSeq"]
            )

            break


    if end_seq is None:

        return {

            "error":
            "올바른 방향의 도착 정류장을 찾을 수 없습니다"

        }


    # 정류장 수 계산
    station_count = (
        end_seq - start_seq
    )


    # 기본 이동 시간 계산
    base_time = (

        station_count
        * AVERAGE_MIN_PER_STATION

    )


    return {

        "start_station":
        start_station,

        "end_station":
        end_station,

        "start_seq":
        start_seq,

        "end_seq":
        end_seq,

        "station_count":
        station_count,

        "base_time":
        base_time
    }



# 테스트 코드
if __name__ == "__main__":


    # 241번 route_id
    route_id = "100100595"
    

    # 청량리역 > 상봉역
    result = calculate_base_time(

        route_id,

        "청량리수산시장",
        "상봉역.중랑우체국"

    )


    print("\n===== 서울 기본 이동시간 계산 =====\n")

    print(result)