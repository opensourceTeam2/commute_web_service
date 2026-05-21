import requests


# 레일포털 인증키
SERVICE_KEY = "$2a$10$crFZ6BOcvthSaMBJtsVveeqCHOep1xGf5uJGVcVtlrITmFo4aO7rO"


# 도시철도 전체 노선 정보 조회
def get_subway_route_info(
    mreaWideCd,
    lnCd
):

    url = (
        "http://openapi.kric.go.kr/openapi/"
        "trainUseInfo/subwayRouteInfo"
    )

    params = {

        "serviceKey": SERVICE_KEY,
        "format": "json",
        "mreaWideCd": mreaWideCd, # 권역코드
        "lnCd": lnCd # 노선코드
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        return response.json()

    except Exception as e:

        return {
            "error": str(e)
        }



# 테스트 코드
if __name__ == "__main__":

    result = get_subway_route_info(

        # 수도권
        "01",

        # 수인분당선
        "K1"
    )

    print(result)