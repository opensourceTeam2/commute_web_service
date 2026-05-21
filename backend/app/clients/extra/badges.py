def get_badges(

    easy_success_count,
    hard_success_count,
    rain_success_count,
    early_morning_count,
    long_distance_count

):

    badge_list = []

    total_points = 0



    # 1️⃣ 여유로운 통학의 신
    # 지각확률 20% 이하 30회 성공

    if easy_success_count >= 30:

        badge_list.append(
            "여유로운 통학의 신"
        )

        total_points += 50



    # 2️⃣ 아슬아슬 마스터
    # 지각확률 50% 이상 10회 성공

    if hard_success_count >= 10:

        badge_list.append(
            "아슬아슬 마스터"
        )

        total_points += 50



    # 3️⃣ 비를 뚫는 자
    # 비 오는 날 10회 성공

    if rain_success_count >= 10:

        badge_list.append(
            "비를 뚫는 자"
        )

        total_points += 50



    # 4️⃣ 새벽 통학생
    # 오전 7시 이전 통학 20회

    if early_morning_count >= 20:

        badge_list.append(
            "새벽 통학생"
        )

        total_points += 50



    # 5️⃣ 강철 체력
    # 왕복 2시간 이상 통학 20회 성공

    if long_distance_count >= 20:

        badge_list.append(
            "강철 체력"
        )

        total_points += 50



    # 1️⃣ + 2️⃣ 세트 보상

    main_set = [

        "여유로운 통학의 신",
        "아슬아슬 마스터"
    ]


    if all(

        badge in badge_list
        for badge in main_set

    ):

        total_points += 300



    # 전체 뱃지 보상

    all_set = [

        "여유로운 통학의 신",
        "아슬아슬 마스터",
        "비를 뚫는 자",
        "새벽 통학생",
        "강철 체력"
    ]


    if all(

        badge in badge_list
        for badge in all_set

    ):

        total_points += 500



    return {

        "badge_list":
        badge_list,

        "badge_count":
        len(badge_list),

        "total_points":
        total_points
    }



# 테스트 코드
if __name__ == "__main__":


    result = get_badges(

        # 지각확률 20% 이하 성공 횟수
        easy_success_count = 35,

        # 지각확률 50% 이상 성공 횟수
        hard_success_count = 12,

        # 비 오는 날 성공 횟수
        rain_success_count = 10,

        # 오전 7시 이전 통학 횟수
        early_morning_count = 21,

        # 왕복 2시간 이상 통학 횟수
        long_distance_count = 18
    )


    print("\n===== 획득한 뱃지 =====\n")


    for badge in result["badge_list"]:

        print(
            f"🏅 {badge}"
        )


    print(

        f"\n획득 뱃지 수: "
        f"{result['badge_count']}개"

    )


    print(

        f"\n총 획득 포인트: "
        f"{result['total_points']}P"

    )