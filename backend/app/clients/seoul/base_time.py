from bus_api import get_route_stations


# 기본 이동 시간 계산
def calculate_base_time(
    route_id,
    start_station,
    end_station
):

    data = get_route_stations(
        route_id
    )

    try:

        item_list = (
            data["ServiceResult"]
            ["msgBody"]
            ["itemList"]
        )

        start_seq = None
        end_seq = None

        for item in item_list:

            station_name = item["stationNm"]

            station_seq = int(
                item["seq"]
            )

            if start_station in station_name:

                start_seq = station_seq

            if end_station in station_name:

                end_seq = station_seq

        if (
            start_seq is None
            or end_seq is None
        ):

            return None

        # 정류장 수 계산
        station_count = abs(
            end_seq - start_seq
        )

        # 정류장당 2분
        base_time = (
            station_count * 2
        )

        return {

            "station_count": station_count,

            "base_time": base_time

        }

    except:

        return None



# 테스트 코드
if __name__ == "__main__":

    route_id = "100100118"

    result = calculate_base_time(

        route_id,

        "강남역",

        "서울역"

    )

    print("\n===== 서울 기본 이동 시간 =====\n")

    print(result)