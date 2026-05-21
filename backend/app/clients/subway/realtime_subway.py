from subway_api import (
    get_realtime_arrival
)


# 도착 코드 변환
ARRIVAL_CODE_MAP = {

    "0": "진입",
    "1": "도착",
    "2": "출발",
    "3": "전역출발",
    "4": "전역진입",
    "5": "전역도착",
    "99": "운행중"
}


# 실시간 지하철 조회
def get_realtime_subways(
    station_name
):

    data = get_realtime_arrival(
        station_name
    )

    arrival_list = (
        data
        .get(
            "realtimeArrivalList",
            []
        )
    )

    if not arrival_list:

        return []

    result = []

    for train in arrival_list:

        # 열차 방향 정보
        train_line = train.get(
            "trainLineNm"
        )

        # 현재 위치
        current_station = train.get(
            "arvlMsg3"
        )

        # 도착 상태 메시지
        arrival_status = train.get(
            "arvlMsg2"
        )

        # 도착 코드
        arrival_code = str(
            train.get(
                "arvlCd"
            )
        )

        # 한국어 변환
        arrival_code_name = (
            ARRIVAL_CODE_MAP.get(
                arrival_code,
                "알수없음"
            )
        )

        # 급행 / 일반 여부
        train_type = train.get(
            "btrainSttus"
        )

        # 상행 / 하행
        updn_line = train.get(
            "updnLine"
        )

        result.append({

            "train_line": train_line,
            "current_station": current_station,
            "arrival_status": arrival_status,
            "arrival_code": arrival_code_name,
            "train_type": train_type,
            "updn_line": updn_line
        })

    return result



# 테스트 코드
if __name__ == "__main__":

    result = get_realtime_subways(
        "죽전"
    )

    print("\n===== 실시간 지하철 정보 =====\n")

    for train in result:

        print(train)