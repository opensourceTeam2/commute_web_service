def calculate_points(

    late_probability,
    rain_type,
    is_rush_hour,
    is_arrived

):

    earned_points = 0
    mission_list = []

    # 1️⃣ 지각확률 20% 이하 + 지각 안 함

    if (
        late_probability <= 20
        and is_arrived
    ):
        earned_points += 40
        mission_list.append(
            "여유로운 통학 성공"
        )


    # 2️⃣ 지각확률 50% 이상 + 지각 안 함

    if (
        late_probability >= 50
        and is_arrived
    ):
        earned_points += 20
        mission_list.append(
            "아슬아슬 통학 성공"
        )


    # 3️⃣ 비 오는 날 + 지각 안 함

    if (
        rain_type == "비"
        or
        rain_type == "눈"
        or
        rain_type == "비/눈"
        and is_arrived
    ):
        earned_points += 10
        mission_list.append(
            "험난한 날씨 속 통학 성공"
        )


    # 4️⃣ 출퇴근 시간 + 지각 안 함

    if (
        is_rush_hour
        and is_arrived
    ):
        earned_points += 10
        mission_list.append(
            "혼잡 시간 통학 성공"
        )

    return {
        "earned_points":
        earned_points,
        "missions":
        mission_list
    }



# 테스트 코드

if __name__ == "__main__":

    result = calculate_points(

        # 지각 확률
        late_probability = 20,

        # 비 / 눈 / 없음
        rain_type = "비/눈",

        # 출퇴근 시간 여부
        is_rush_hour = True,

        # 도착 버튼 클릭 여부
        is_arrived = True

    )

    print("\n===== 오늘의 통학 미션 =====\n")

    for mission in result["missions"]:

        print(
            f"✅ {mission}"
        )


    print(
        f"\n오늘도 통학 성공! "
        f"+{result['earned_points']}P 획득"
    )