from datetime import datetime, timedelta
from app.clients.guide.guide_message import make_guide_message

from app.clients.kakao_local_api import get_place_coordinate
from app.clients.odsay_api import search_public_transit_routes
from app.services.lateness_service import (
    get_remaining_minutes,
    calculate_lateness_probability,
)


DESTINATION_KEYWORD = "단국대학교 죽전캠퍼스"


def to_list(value):
    if value is None:
        return []

    if isinstance(value, list):
        return value

    return [value]


def flatten_list(value):
    """
    리스트가 한 번 더 감싸져 있는 경우를 풀어준다.
    예:
    [[{...}, {...}]] -> [{...}, {...}]
    [{...}, {...}] -> [{...}, {...}]
    {...} -> [{...}]
    """
    items = to_list(value)
    result = []

    for item in items:
        if isinstance(item, list):
            result.extend(item)
        else:
            result.append(item)

    return result


def safe_dict(value):
    """
    value가 dict면 그대로 반환.
    value가 list면 첫 번째 dict를 찾아 반환.
    아니면 빈 dict 반환.
    """
    if isinstance(value, dict):
        return value

    if isinstance(value, list):
        for item in value:
            if isinstance(item, dict):
                return item

    return {}


def get_path_type_name(path_type):
    if path_type == 1:
        return "지하철"
    if path_type == 2:
        return "버스"
    if path_type == 3:
        return "버스 + 지하철"

    return "대중교통"


def get_traffic_type_name(traffic_type):
    if traffic_type == 1:
        return "지하철"
    if traffic_type == 2:
        return "버스"
    if traffic_type == 3:
        return "도보"

    return "이동"


def get_lane_name(sub_path):
    sub_path = safe_dict(sub_path)

    lanes = flatten_list(sub_path.get("lane"))

    if not lanes:
        return ""

    lane = safe_dict(lanes[0])

    if not lane:
        return ""

    if sub_path.get("trafficType") == 1:
        return lane.get("name") or lane.get("nameKor") or "지하철"

    if sub_path.get("trafficType") == 2:
        bus_no = lane.get("busNo") or lane.get("busNoKor")
        if bus_no:
            return f"{bus_no}번 버스"
        return "버스"

    return ""


def make_step_text(sub_path):
    sub_path = safe_dict(sub_path)

    traffic_type = sub_path.get("trafficType")
    section_time = sub_path.get("sectionTime", 0)

    if traffic_type == 3:
        return f"도보 이동 약 {section_time}분"

    traffic_name = get_traffic_type_name(traffic_type)
    lane_name = get_lane_name(sub_path)

    start_name = sub_path.get("startName", "출발지")
    end_name = sub_path.get("endName", "도착지")
    station_count = sub_path.get("stationCount")

    if station_count is not None:
        return (
            f"{start_name}에서 {lane_name} 탑승 → "
            f"{end_name} 하차 "
            f"({station_count}개 정류장, 약 {section_time}분)"
        )

    return (
        f"{start_name}에서 {traffic_name} 탑승 → "
        f"{end_name} 하차 "
        f"(약 {section_time}분)"
    )


def make_route_summary(info, path_type_name):
    info = safe_dict(info)

    first = info.get("firstStartStation") or "출발지"
    last = info.get("lastEndStation") or "단국대"

    return f"{first} → {last} ({path_type_name})"


def get_paths_from_odsay_data(odsay_data):
    """
    odsay_api.py가 어떤 형태로 반환하든 path 리스트를 꺼낸다.

    가능한 형태:
    1. {"result": {"path": [...]}}
    2. {"result": [{"path": [...]}]}
    3. {"path": [...]}
    4. [...]
    """
    if isinstance(odsay_data, list):
        return flatten_list(odsay_data)

    if not isinstance(odsay_data, dict):
        return []

    result = odsay_data.get("result")

    if isinstance(result, dict):
        return flatten_list(result.get("path"))

    if isinstance(result, list):
        paths = []

        for item in result:
            if isinstance(item, dict):
                paths.extend(flatten_list(item.get("path")))
            elif isinstance(item, list):
                paths.extend(flatten_list(item))

        return paths

    if "path" in odsay_data:
        return flatten_list(odsay_data.get("path"))

    return []


def normalize_odsay_path(path, remaining_minutes):
    path = safe_dict(path)

    info = safe_dict(path.get("info"))

    total_minutes = int(info.get("totalTime", 0) or 0)
    payment = int(info.get("payment", 0) or 0)

    bus_transfer_count = int(info.get("busTransitCount", 0) or 0)
    subway_transfer_count = int(info.get("subwayTransitCount", 0) or 0)
    transfer_count = bus_transfer_count + subway_transfer_count

    interval_minutes = int(info.get("totalIntervalTime", 0) or 0)

    path_type = path.get("pathType")
    path_type_name = get_path_type_name(path_type)

    sub_paths = flatten_list(path.get("subPath"))
    steps = []

    for sub_path in sub_paths:
        if isinstance(sub_path, dict):
            steps.append(make_step_text(sub_path))

    lateness = calculate_lateness_probability(
        total_minutes=total_minutes,
        remaining_minutes=remaining_minutes,
        transfer_count=transfer_count,
        interval_minutes=interval_minutes,
    )

    expected_arrival_time = datetime.now() + timedelta(minutes=total_minutes)

    return {
        "routeSummary": make_route_summary(info, path_type_name),
        "pathType": path_type_name,
        "steps": steps,
        "totalMinutes": total_minutes,
        "payment": payment,
        "transferCount": transfer_count,
        "busTransferCount": bus_transfer_count,
        "subwayTransferCount": subway_transfer_count,
        "remainingMinutes": remaining_minutes,
        "expectedArrivalTime": expected_arrival_time.strftime("%H:%M"),
        "lateProbability": lateness["lateProbability"],
        "statusMessage": lateness["statusMessage"],
        "reasons": lateness["reasons"],
    }


def recommend_commute_routes(start_location, class_start_time):
    """
    사용자가 어떤 출발지를 입력해도:
    1. 출발지 좌표 검색
    2. 단국대 좌표 검색
    3. ODsay 대중교통 경로 검색
    4. 지각확률 계산
    5. 낮은 순서 3개 반환
    """
    start_place = get_place_coordinate(start_location)
    destination_place = get_place_coordinate(DESTINATION_KEYWORD)

    odsay_data = search_public_transit_routes(
        start_x=start_place["x"],
        start_y=start_place["y"],
        end_x=destination_place["x"],
        end_y=destination_place["y"],
    )

    #print("ODsay 응답 타입:", type(odsay_data))
    #print("ODsay 응답 내용:", odsay_data)

    paths = get_paths_from_odsay_data(odsay_data)

    paths = [
        path for path in paths
        if isinstance(path, dict)
    ]

    if not paths:
        raise ValueError("대중교통 경로를 찾지 못했습니다.")

    remaining_minutes = get_remaining_minutes(class_start_time)

    calculated_routes = []

    for path in paths:
        route = normalize_odsay_path(path, remaining_minutes)
        calculated_routes.append(route)

    calculated_routes.sort(
        key=lambda route: (
            route["lateProbability"],
            route["totalMinutes"],
            route["transferCount"],
        )
    )

    top_three = calculated_routes[:3]

    for index, route in enumerate(top_three, start=1):
        route["rank"] = index

    try:
        guide_messages = make_guide_message()
    except Exception as error:
        print("안내문구 생성 실패:", error)
        guide_messages = ["날씨/미세먼지 안내를 불러오지 못했습니다."]

    return {
        "startPlace": start_place,
        "destinationPlace": destination_place,
        "routes": top_three,
        "guideMessages": guide_messages,
    }