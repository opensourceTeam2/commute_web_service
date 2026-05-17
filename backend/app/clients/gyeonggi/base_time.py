from bus_api import get_route_stations


# 정류장 하나당 평균 이동 시간(분)
AVERAGE_MIN_PER_STATION = 2


def get_all_station_sequences(stations, station_name):

    route_stations = (
        stations
        .get("response", {})
        .get("msgBody", {})
        .get("busRouteStationList", [])
    )

    result = []

    for station in route_stations:

        name = station.get("stationName", "")

        if station_name in name:

            result.append({
                "stationSeq": int(station.get("stationSeq")),
                "stationName": name
            })

    return result


def calculate_base_time(route_id, start_station, end_station):

    stations = get_route_stations(route_id)

    # 출발 정류장 후보
    start_candidates = get_all_station_sequences(
        stations,
        start_station
    )

    # 도착 정류장 후보
    end_candidates = get_all_station_sequences(
        stations,
        end_station
    )

    if not start_candidates or not end_candidates:

        return {
            "error": "정류장을 찾을 수 없습니다"
        }

    # 기본적으로 가장 첫 출발 정류장 사용
    start_seq = start_candidates[0]["stationSeq"]

    # 출발 이후에 오는 도착 정류장 선택
    end_seq = None

    for end in end_candidates:

        if end["stationSeq"] > start_seq:

            end_seq = end["stationSeq"]
            break

    if end_seq is None:

        return {
            "error": "올바른 방향의 도착 정류장을 찾을 수 없습니다"
        }

    # 정류장 개수 계산
    station_count = end_seq - start_seq

    # 기본 이동시간 계산
    base_time = station_count * AVERAGE_MIN_PER_STATION

    return {

        "start_station": start_station,
        "end_station": end_station,

        "start_seq": start_seq,
        "end_seq": end_seq,

        "station_count": station_count,

        "base_time": base_time
    }



# 테스트 코드
if __name__ == "__main__":

    # 용인 24번
    route_id = 241428004

    # 죽전 > 단국대
    result = calculate_base_time(
        route_id,
        "죽전역",
        "단국대"
    )

    print("\n===== 기본 이동시간 계산 =====")
    print(result)