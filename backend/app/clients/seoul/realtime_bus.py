from bus_api import (
    get_arrival_info
)


# 실시간 버스 조회
def get_realtime_buses(

    station_id,
    route_id,
    station_order,
    route_name

):

    data = get_arrival_info(

        station_id,
        route_id,
        station_order
    )


    arrival_list = (
        data
        .get("msgBody", {})
        .get("itemList", [])
    )


    if not arrival_list:

        return []


    # dict 하나만 올 경우
    if isinstance(
        arrival_list,
        dict
    ):

        arrival_list = [
            arrival_list
        ]


    result = []


    for bus in arrival_list:


        bus_name = str(
            bus.get(
                "rtNm",
                ""
            )
        )


        # 원하는 노선만 조회
        if route_name == bus_name:


            # 첫 번째 버스
            arrival_msg1 = bus.get(
                "arrmsg1"
            )

            remain_station1 = bus.get(
                "staOrd"
            )


            # 두 번째 버스
            arrival_msg2 = bus.get(
                "arrmsg2"
            )

            remain_station2 = bus.get(
                "staOrd"
            )


            # 첫 번째 버스 추가
            if arrival_msg1:

                result.append({

                    "route_name":
                    bus_name,

                    "arrival_message":
                    arrival_msg1,

                    "remain_station":
                    remain_station1
                })


            # 두 번째 버스 추가
            if arrival_msg2:

                result.append({

                    "route_name":
                    bus_name,

                    "arrival_message":
                    arrival_msg2,

                    "remain_station":
                    remain_station2
                })


    return result




# 테스트 코드
if __name__ == "__main__":


    # 상봉역.중랑우체국
    station_id = "106000004"

    # 241번 route_id
    route_id = "100100595"

    # 정류장 순서
    station_order = "102"


    result = get_realtime_buses(

        station_id,
        route_id,
        station_order,
        "241"
    )


    print("\n===== 서울 실시간 버스 정보 =====\n")


    for bus in result:

        print(bus)