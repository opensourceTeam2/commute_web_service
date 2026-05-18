from bus_api import get_arrival_info


# 실시간 버스 대기 시간
def get_bus_wait_time(
    station_id,
    route_id
):

    data = get_arrival_info(
        station_id,
        route_id
    )

    try:

        item = (
            data["ServiceResult"]
            ["msgBody"]
            ["itemList"]
        )

        # 초 → 분
        wait_time = int(
            item["arrmsg1"]
            .split("[")[0]
            .replace("분", "")
            .strip()
        )

        return wait_time

    except:

        return None


# 테스트 코드
if __name__ == "__main__":

    # 예시
    station_id = "123456"

    route_id = "100100118"

    result = get_bus_wait_time(
        station_id,
        route_id
    )

    print("\n===== 서울 실시간 버스 =====\n")

    print(result)