from app.clients.api_keys import KAKAO_REST_API_KEY
import requests



def get_kakao_headers():
    if not KAKAO_REST_API_KEY:
        raise RuntimeError("KAKAO_REST_API_KEY가 설정되지 않았습니다.")

    return {
        "Authorization": f"KakaoAK {KAKAO_REST_API_KEY}"
    }


def search_keyword_place(keyword):
    """
    장소명으로 좌표 검색
    예: 수원역, 미금역, 단국대학교 죽전캠퍼스
    """
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"

    params = {
        "query": keyword,
        "size": 1
    }

    response = requests.get(
        url,
        headers=get_kakao_headers(),
        params=params,
        timeout=10
    )

    if response.status_code != 200:
        print("카카오 키워드 검색 API 요청 실패")
        print("status_code:", response.status_code)
        print("response_text:", response.text)
        print("used_key_prefix:", KAKAO_REST_API_KEY[:6])
        raise RuntimeError(
            f"Kakao Local API 오류: {response.status_code} / {response.text}"
        )

    data = response.json()
    documents = data.get("documents", [])

    if not documents:
        return None

    place = documents[0]

    return {
        "name": place.get("place_name"),
        "address": place.get("address_name"),
        "roadAddress": place.get("road_address_name"),
        "x": float(place.get("x")),  # 경도
        "y": float(place.get("y")),  # 위도
    }


def search_address_place(keyword):
    """
    주소로 좌표 검색
    예: 경기도 용인시 수지구 죽전로 152
    """
    url = "https://dapi.kakao.com/v2/local/search/address.json"

    params = {
        "query": keyword,
        "size": 1
    }

    response = requests.get(
        url,
        headers=get_kakao_headers(),
        params=params,
        timeout=10
    )

    if response.status_code != 200:
        print("카카오 주소 검색 API 요청 실패")
        print("status_code:", response.status_code)
        print("response_text:", response.text)
        raise RuntimeError(
            f"Kakao Address API 오류: {response.status_code} / {response.text}"
        )

    data = response.json()
    documents = data.get("documents", [])

    if not documents:
        return None

    place = documents[0]

    address = place.get("address")
    road_address = place.get("road_address")

    return {
        "name": keyword,
        "address": address.get("address_name") if address else None,
        "roadAddress": road_address.get("address_name") if road_address else None,
        "x": float(place.get("x")),
        "y": float(place.get("y")),
    }


def get_place_coordinate(keyword):
    """
    사용자가 입력한 장소명을 좌표로 변환한다.
    1. 장소명 검색
    2. 실패하면 주소 검색
    """
    keyword = keyword.strip()

    if not keyword:
        raise ValueError("출발 위치를 입력해주세요.")

    place = search_keyword_place(keyword)

    if place:
        return place

    place = search_address_place(keyword)

    if place:
        return place

    raise ValueError(f"'{keyword}' 위치를 찾을 수 없습니다.")