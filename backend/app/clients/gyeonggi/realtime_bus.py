from bus_api import get_realtime_arrival


# 실시간 버스 조회
def get_realtime_buses(station_id, route_name):

    data = get_realtime_arrival(
        station_id
    )

    arrival_list = (
        data
        .get("response", {})
        .get("msgBody", {})
        .get("busArrivalList", [])
    )

    if not arrival_list:

        return []

    # dict 하나만 오면 리스트로 변환
    if isinstance(arrival_list, dict):
        arrival_list = [arrival_list]

    result = []

    for bus in arrival_list:

        bus_name = str(
            bus.get("routeName", "")
        )

        # 원하는 노선만 조회
        if route_name == bus_name:

            # 첫 번째 버스
            predict1 = bus.get("predictTime1")
            location1 = bus.get("locationNo1")

            # 두 번째 버스
            predict2 = bus.get("predictTime2")
            location2 = bus.get("locationNo2")

            # 첫 번째 버스 추가
            if predict1 != '' and predict1 is not None:

                result.append({

                    "route_name": bus_name,

                    "predict_time": predict1,

                    "remain_station": location1

                })

            # 두 번째 버스 추가
            if predict2 != '' and predict2 is not None:

                result.append({

                    "route_name": bus_name,

                    "predict_time": predict2,

                    "remain_station": location2

                })

    # 시간 순 정렬
    result.sort(
        key=lambda x: x["predict_time"]
    )

    return result



# 테스트 코드
if __name__ == "__main__":

    # 죽전역.수지레스피아
    station_id = 228001028

    result = get_realtime_buses(
        station_id,
        "24"
    )

    print("\n===== 실시간 버스 정보 =====\n")

    for bus in result:

        print(bus)