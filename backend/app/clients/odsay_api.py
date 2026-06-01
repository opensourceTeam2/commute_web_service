from app.clients.api_keys import ODSAY_API_KEY
import requests
import json


def get_odsay_error_message(error):
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

    if response.status_code != 200:
        raise RuntimeError(
            f"ODsay API 요청 실패: {response.status_code}"
        )

    try:
        data = response.json()
    except json.JSONDecodeError:
        raise RuntimeError(
            "ODsay API 응답이 JSON 형식이 아닙니다. API 키 또는 요청 좌표를 확인해주세요."
        )

    error = data.get("error")

    if error:
        message = get_odsay_error_message(error)
        raise RuntimeError(message)

    return data