from datetime import datetime, timedelta
from app.clients.guide.guide_message import make_guide_message
from app.clients.kakao_local_api import get_place_coordinate
from app.clients.odsay_api import search_public_transit_routes


def parse_class_start_time(class_start_time):
    """
    사용자가 입력한 수업 시작 시간을 datetime 형식으로 변환한다.

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

    # 입력한 수업 시간이 이미 지난 시간이면 다음 날 수업으로 처리
    if class_datetime < now:
        class_datetime += timedelta(days=1)

    return class_datetime


def get_remaining_minutes(class_start_time):
    """
    현재 시각 기준으로 수업 시작까지 남은 시간을 분 단위로 계산한다.
    """
    class_datetime = parse_class_start_time(class_start_time)
    now = datetime.now()

    return max(0, int((class_datetime - now).total_seconds() // 60))


def calculate_lateness_probability(
    total_minutes,
    remaining_minutes,
    transfer_count=0,
    interval_minutes=0,
    weather=None,
    fine_dust=None,
):
    """
    실시간 API에서 받아온 경로 정보를 기반으로 지각 확률을 계산한다.
     """

    total_minutes = int(total_minutes or 0)
    remaining_minutes = int(remaining_minutes or 0)
    transfer_count = int(transfer_count or 0)
    interval_minutes = int(interval_minutes or 0)

    diff = total_minutes - remaining_minutes
    reasons = []

    # 도착 여유 시간 기준 기본 지각 확률 계산
    if diff <= -20:
        probability = 5
    elif diff <= -10:
        probability = 15
    elif diff <= 0:
        probability = 30
    else:
        probability = min(60 + diff * 3, 90)

    if diff > 0:
        reasons.append(f"예상 도착이 수업 시작보다 약 {diff}분 늦습니다.")
    else:
        reasons.append(f"수업 시작보다 약 {abs(diff)}분 일찍 도착할 수 있습니다.")

    # 환승 횟수 반영
    if transfer_count > 0:
        transfer_penalty = min(transfer_count * 5, 15)
        probability += transfer_penalty
        reasons.append(f"환승 {transfer_count}회로 인해 지연 가능성을 추가 반영했습니다.")

    # 배차간격 반영
    if interval_minutes > 0:
        interval_penalty = min(interval_minutes * 0.5, 15)
        probability += interval_penalty
        reasons.append(f"배차간격 {interval_minutes}분을 반영하여 지각 가능성을 계산했습니다.")

    # 날씨 영향 반영
    weather_text = str(weather).lower() if weather else ""

    if "rain" in weather_text or "비" in weather_text:
        probability += 7
        reasons.append("비로 인해 이동 시간이 늘어날 가능성을 반영했습니다.")

    if "snow" in weather_text or "눈" in weather_text:
        probability += 12
        reasons.append("눈으로 인해 도로 상황이 좋지 않을 가능성을 반영했습니다.")

    if "fog" in weather_text or "안개" in weather_text:
        probability += 5
        reasons.append("안개로 인한 이동 지연 가능성을 반영했습니다.")

    probability = max(0, min(100, round(probability)))

    if probability <= 20:
        status_message = "지각 가능성이 낮습니다."
    elif probability <= 50:
        status_message = "조금 여유가 있지만 주의가 필요합니다."
    elif probability <= 80:
        status_message = "지각 가능성이 있습니다. 서두르는 것이 좋습니다."
    else:
        status_message = "지각 가능성이 높습니다. 다른 경로를 고려하세요."

    try:
        guide_messages = make_guide_message()
    except Exception:
        guide_messages = []

        weather_text = str(weather).lower() if weather else ""
        fine_dust_text = str(fine_dust).lower() if fine_dust else ""

        if "rain" in weather_text or "비" in weather_text:
            guide_messages.append("비가 오니 우산을 챙기세요.")

        if "snow" in weather_text or "눈" in weather_text:
            guide_messages.append("눈이 오니 이동 시간을 여유 있게 잡으세요.")

        if "fog" in weather_text or "안개" in weather_text:
            guide_messages.append("안개로 인해 이동이 지연될 수 있습니다.")

        if fine_dust_text == "bad" or fine_dust_text == "나쁨":
            guide_messages.append("미세먼지가 나쁘니 마스크를 착용하세요.")

        if not guide_messages:
            guide_messages.append("특별한 날씨 안내 사항이 없습니다.")

    return {
        "lateProbability": probability,
        "statusMessage": status_message,
        "reasons": reasons,
        "guideMessages": guide_messages,
        "detail": {
            "totalMinutes": total_minutes,
            "remainingMinutes": remaining_minutes,
            "differenceMinutes": diff,
            "transferCount": transfer_count,
            "intervalMinutes": interval_minutes,
            "weather": weather,
            "fineDust": fine_dust,
        },
    }

def calculate_lateness_from_api_data(
    class_start_time,
    route_data,
    weather_data=None,
):
    """
    ODSAY API, 날씨 API에서 받아온 데이터를 지각 확률 계산 함수에 연결한다.

    class_start_time:
        사용자가 입력한 수업 시작 시간

    route_data:
        ODSAY API에서 받아온 경로 정보

    weather_data:
        날씨 API에서 받아온 날씨/미세먼지 정보
    """

    weather_data = weather_data or {}

    remaining_minutes = get_remaining_minutes(class_start_time)

    total_minutes = extract_total_minutes(route_data)
    transfer_count = extract_transfer_count(route_data)
    interval_minutes = extract_interval_minutes(route_data)

    weather = weather_data.get("weather")
    fine_dust = weather_data.get("fine_dust")

    return calculate_lateness_probability(
        total_minutes=total_minutes,
        remaining_minutes=remaining_minutes,
        transfer_count=transfer_count,
        interval_minutes=interval_minutes,
        weather=weather,
        fine_dust=fine_dust,
    )


def extract_total_minutes(route_data):
    """
    ODSAY API 결과에서 총 소요 시간을 추출한다.
    프로젝트에서 사용하는 실제 key 이름에 맞게 여러 경우를 처리한다.
    """
    if not route_data:
        return 0

    if "totalTime" in route_data:
        return route_data["totalTime"]

    if "total_minutes" in route_data:
        return route_data["total_minutes"]

    if "totalMinutes" in route_data:
        return route_data["totalMinutes"]

    if "info" in route_data and "totalTime" in route_data["info"]:
        return route_data["info"]["totalTime"]

    return 0


def extract_transfer_count(route_data):
    """
    ODSAY API 결과에서 환승 횟수를 추출한다.
    """
    if not route_data:
        return 0

    if "transferCount" in route_data:
        return route_data["transferCount"]

    if "transfer_count" in route_data:
        return route_data["transfer_count"]

    if "transfer" in route_data:
        return route_data["transfer"]

    if "info" in route_data and "busTransitCount" in route_data["info"]:
        bus_count = route_data["info"].get("busTransitCount", 0)
        subway_count = route_data["info"].get("subwayTransitCount", 0)
        total_transit_count = bus_count + subway_count

        if total_transit_count > 0:
            return max(0, total_transit_count - 1)

    return 0


def extract_interval_minutes(route_data):
    """
    ODSAY API 결과에서 배차간격 정보를 추출한다.
    없으면 0으로 처리한다.
    """
    if not route_data:
        return 0

    if "intervalMinutes" in route_data:
        return route_data["intervalMinutes"]

    if "interval_minutes" in route_data:
        return route_data["interval_minutes"]

    if "interval" in route_data:
        return route_data["interval"]

    return 0

def select_best_route(odsay_data):
    """
    ODSAY 결과 중 총 소요 시간이 가장 짧은 경로를 선택한다.
    """
    result = odsay_data.get("result", {})
    paths = result.get("path", [])

    if not paths:
        raise ValueError("사용 가능한 대중교통 경로가 없습니다.")

    return min(paths, key=lambda path: path.get("info", {}).get("totalTime", 9999))


def extract_interval_from_subpaths(route):
    """
    세부 경로 구간에서 배차간격 정보를 추출한다.
    여러 구간이 있으면 가장 긴 배차간격을 사용한다.
    """
    subpaths = route.get("subPath", [])
    intervals = []

    for subpath in subpaths:
        lane_list = subpath.get("lane", [])

        for lane in lane_list:
            interval = lane.get("interval")
            if interval is not None:
                try:
                    intervals.append(int(interval))
                except (TypeError, ValueError):
                    pass

    if not intervals:
        return 0

    return max(intervals)


def build_route_data_from_odsay(odsay_data):
    """
    ODSAY API 전체 응답에서 지각 확률 계산용 route_data를 만든다.
    """
    best_route = select_best_route(odsay_data)
    info = best_route.get("info", {})

    total_minutes = int(info.get("totalTime", 0))
    bus_count = int(info.get("busTransitCount", 0))
    subway_count = int(info.get("subwayTransitCount", 0))

    total_transit_count = bus_count + subway_count
    transfer_count = max(0, total_transit_count - 1) if total_transit_count > 0 else 0

    interval_minutes = extract_interval_from_subpaths(best_route)

    return {
        "totalTime": total_minutes,
        "transferCount": transfer_count,
        "intervalMinutes": interval_minutes,
    }


def calculate_lateness_with_realtime_api(
    start_keyword,
    end_keyword,
    class_start_time,
    weather_data=None,
):
    """
    팀원이 만든 Kakao/ODSay API 코드를 사용해서
    실시간 경로 데이터를 가져오고 지각 확률을 계산한다.
    """
    weather_data = weather_data or {}

    start_place = get_place_coordinate(start_keyword)
    end_place = get_place_coordinate(end_keyword)

    odsay_data = search_public_transit_routes(
        start_x=start_place["x"],
        start_y=start_place["y"],
        end_x=end_place["x"],
        end_y=end_place["y"],
    )

    route_data = build_route_data_from_odsay(odsay_data)

    result = calculate_lateness_from_api_data(
        class_start_time=class_start_time,
        route_data=route_data,
        weather_data=weather_data,
    )

    result["routeInfo"] = {
        "startPlace": start_place,
        "endPlace": end_place,
        "routeData": route_data,
    }

    return result