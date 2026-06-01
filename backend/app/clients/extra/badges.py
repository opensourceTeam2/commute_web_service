from app.db import database

def update_badges(
    login_id,
    badge_data,
    late_probability,
    rain_type,
    current_hour,
    commute_minutes,
    is_on_time
):
    earned_badges = []

    # 1️⃣ 여유로운 통학

    if (late_probability <= 20
        and is_on_time):

        badge_data[
            "easy_success_count"
        ] += 1
        
        database.update_badge_count(
        login_id,
        "easy_success_count"
        )
        
        earned_badges.append(
            "여유로운 통학의 신"
        )

    # 2️⃣ 아슬아슬 마스터

    if (late_probability >= 50
        and is_on_time):

        badge_data[
            "hard_success_count"
        ] += 1
        
        database.update_badge_count(
        login_id,
        "hard_success_count"
        )

        earned_badges.append(
            "아슬아슬 마스터"
        )

    # 3️⃣ 비 / 눈

    if (
    rain_type in [

        "비",
        "눈",
        "비/눈"
    ]
    and is_on_time):

        badge_data[
            "rain_success_count"
        ] += 1

        database.update_badge_count(
        login_id,
        "rain_success_count"
        )

        earned_badges.append(
            "비를 뚫는 자"
        )

    # 4️⃣ 새벽 통학생

    if (5 < current_hour < 10
        and is_on_time):

        badge_data[
            "early_morning_count"
        ] += 1
        
        database.update_badge_count(
        login_id,
        "early_morning_count"
        )
        
        earned_badges.append(
            "새벽 통학생"
        )

    # 5️⃣ 편도 1시간 이상

    if (commute_minutes >= 60
        and is_on_time):

        badge_data[
            "long_distance_count"
        ] += 1

        database.update_badge_count(
        login_id,
        "long_distance_count"
        )

        earned_badges.append(
            "강철 체력"
        )

    badge_list = []
    total_points = 0

    if badge_data[
        "easy_success_count"
    ] >= 30:

        badge_list.append(
            "여유로운 통학의 신"
        )

        total_points += 50


    if badge_data[
        "hard_success_count"
    ] >= 10:

        badge_list.append(
            "아슬아슬 마스터"
        )

        total_points += 50

    if badge_data[
        "rain_success_count"
    ] >= 10:

        badge_list.append(
            "비를 뚫는 자"
        )

        total_points += 50

    if badge_data[
        "early_morning_count"
    ] >= 20:

        badge_list.append(
            "새벽 통학생"
        )

        total_points += 50

    if badge_data[
        "long_distance_count"
    ] >= 20:

        badge_list.append(
            "강철 체력"
        )

        total_points += 50

    return {

        "badge_list":
        badge_list,
        
        "earned_badges":
        earned_badges,

        "badge_count":
        len(badge_list),

        "total_points":
        total_points,

        "badge_data":
        badge_data
    }