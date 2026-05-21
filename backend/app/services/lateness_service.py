from datetime import datetime, timedelta


def parse_class_start_time(class_start_time):
    """
    예:
    오전 09:00
    오후 03:30
    """
    try:
        period, time_text = class_start_time.strip().split(" ")
        hour, minute = map(int, time_text.split(":"))
    except ValueError:
        raise ValueError("수업 시작 시간 형식이 올바르지 않습니다. 예: 오후 03:30")

    if period == "오후" and hour != 12:
        hour += 12

    if period == "오전" and hour == 12:
        hour = 0

    now = datetime.now()

    class_datetime = now.replace(
        hour=hour,
        minute=minute,
        second=0,
        microsecond=0,
    )

    if class_datetime < now:
        class_datetime += timedelta(days=1)

    return class_datetime


def get_remaining_minutes(class_start_time):
    class_datetime = parse_class_start_time(class_start_time)
    now = datetime.now()

    return max(0, int((class_datetime - now).total_seconds() // 60))


def calculate_lateness_probability(
    total_minutes,
    remaining_minutes,
    transfer_count=0,
    interval_minutes=0,
):
    """
    total_minutes: 경로 총 예상 소요시간
    remaining_minutes: 수업 시작까지 남은 시간
    transfer_count: 환승 횟수
    interval_minutes: 전체 배차간격 정보
    """
    diff = total_minutes - remaining_minutes

    reasons = []

    probability = 25 + diff * 4

    if diff > 0:
        reasons.append(f"예상 도착이 수업 시작보다 약 {diff}분 늦습니다.")
    else:
        reasons.append(f"수업 시작보다 약 {abs(diff)}분 일찍 도착할 수 있습니다.")

    if transfer_count > 0:
        transfer_penalty = transfer_count * 5
        probability += transfer_penalty
        reasons.append(f"환승 {transfer_count}회로 인해 {transfer_penalty}%를 추가 반영했습니다.")

    if interval_minutes > 0:
        interval_penalty = min(interval_minutes * 0.5, 15)
        probability += interval_penalty
        reasons.append(f"배차간격 변수로 약 {round(interval_penalty)}%를 추가 반영했습니다.")

    probability = max(0, min(100, round(probability)))

    if probability <= 20:
        status_message = "지각 가능성이 낮습니다."
    elif probability <= 50:
        status_message = "조금 여유가 있지만 주의가 필요합니다."
    elif probability <= 80:
        status_message = "지각 가능성이 있습니다. 서두르는 것이 좋습니다."
    else:
        status_message = "지각 가능성이 높습니다. 다른 경로를 고려하세요."

    return {
        "lateProbability": probability,
        "statusMessage": status_message,
        "reasons": reasons,
    }