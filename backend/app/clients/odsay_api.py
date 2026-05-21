from app.clients.api_keys import ODSAY_API_KEY
import requests



def get_odsay_error_message(error):
    """
    ODsay error가 dict로 오든 list로 오든 안전하게 메시지를 꺼낸다.
    """
    default_message = "대중교통 경로 검색에 실패했습니다."

    if error is None:
        return default_message

    if isinstance(error, dict):
        return (
            error.get("message")
            or error.get("msg")
            or error.get("errorMessage")
            or default_message
        )

    if isinstance(error, list):
        messages = []

        for item in error:
            if isinstance(item, dict):
                message = (
                    item.get("message")
                    or item.get("msg")
                    or item.get("errorMessage")
                )

                if message:
                    messages.append(message)
            else:
                messages.append(str(item))

        if messages:
            return " / ".join(messages)

        return default_message

    return str(error)


def search_public_transit_routes(start_x, start_y, end_x, end_y):
    url = "https://api.odsay.com/v1/api/searchPubTransPathT"

    params = {
        "SX": start_x,
        "SY": start_y,
        "EX": end_x,
        "EY": end_y,
        "apiKey": ODSAY_API_KEY,
    }

    response = requests.get(
        url,
        params=params,
        timeout=10,
    )

    print("ODsay status_code:", response.status_code)
    print("ODsay response_text:", response.text)

    if response.status_code != 200:
        raise RuntimeError(
            f"ODsay API 요청 실패: {response.status_code} / {response.text}"
        )

    data = response.json()

    error = data.get("error")

    if error:
        message = get_odsay_error_message(error)

        print("ODsay API 오류 응답:", error)
        print("ODsay API 오류 메시지:", message)

        raise RuntimeError(message)

    return data