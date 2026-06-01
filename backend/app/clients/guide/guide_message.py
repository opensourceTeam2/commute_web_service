from app.clients.guide.air_quality import get_air_data
from app.clients.guide.rain import get_rain_probability


# 안내 문구 생성
def make_guide_message():

    messages = []

    air = get_air_data()

    rain = get_rain_probability()


    if air["status"] == "very_bad":

        messages.append(
        "🚨 미세먼지가 매우 심해요. KF94 마스크 착용을 권장해요!"
        )

    elif air["status"] == "bad":

        messages.append(
        "😷 미세먼지가 심해요. 마스크를 챙기세요!"
        )

    elif air["status"] == "normal":

        messages.append(
        "🙂 오늘 미세먼지는 보통 수준이에요."
        )

    else:

        messages.append(
        "🌿 오늘 공기가 좋아요!"
        )

    # 비
    if rain["rain_percent"] >= 60:

        messages.append(
            "☔ 비 올 확률이 높아요. 우산 챙기세요!"
        )

    elif rain["rain_percent"] >= 30:

        messages.append(
            "🌧️ 비가 올 수도 있어요."
        )

    else:

        messages.append(
            "☀️ 오늘은 화창한 날씨예요!"
        )

    return messages



# 테스트 코드
if __name__ == "__main__":

    result = make_guide_message()

    print("\n===== 안내 문구 =====\n")

    for message in result:

        print(message)