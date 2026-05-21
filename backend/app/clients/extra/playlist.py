import random
from googleapiclient.discovery import build


# 발급받은 API KEY
API_KEY = "AIzaSyABs4wWeNnwPTkYtrpwdTIdlTYD_xTg104"


# YouTube API 연결
youtube = build(

    "youtube",
    "v3",

    developerKey=API_KEY
)


# 유튜브 플레이리스트 검색

def get_playlist(

    keyword,

    count
):

    request = youtube.search().list(

        q=keyword,

        part="snippet",

        type="video",

        maxResults=20
    )


    response = request.execute()


    result = []


    for item in response["items"]:

        video_id = item["id"]["videoId"]

        title = item["snippet"]["title"]

        channel = item["snippet"]["channelTitle"]


        url = (
            f"https://youtube.com/watch?v={video_id}"
        )


        thumbnail = (
            item["snippet"]["thumbnails"]
            ["high"]["url"]
        )


        result.append({

            "title": title,

            "channel": channel,

            "url": url,

            "thumbnail": thumbnail
        })


    # 검색 결과 중 랜덤 추천
    return random.sample(

        result,

        min(count, len(result))
    )


# 상황별 플레이리스트 추천

def recommend_playlist(

    rain_probability,
    late_probability,
    current_hour

):

    final_playlist = []

    active_conditions = []


    # 비 오는 날

    if rain_probability >= 80:

        active_conditions.append({

            "type": "rain",

            "keyword":
            "비 오는 날 감성 플리"
        })


    # 지각 확률 높음

    if late_probability >= 50:

        active_conditions.append({

            "type": "late",

            "keyword":
            "텐션 높은 플레이리스트"
        })


    # 새벽 통학

    if current_hour < 7:

        active_conditions.append({

            "type": "morning",

            "keyword":
            "새벽 감성 플레이리스트"
        })


    # 일반 통학 플리(조건이 하나도 없을 때)

    if not active_conditions:

        return get_playlist(

            "통학 플레이리스트",

            5
        )



    # 상황 1개 → 해당 플리 5개

    if len(active_conditions) == 1:

        condition = active_conditions[0]


        final_playlist.extend(

            get_playlist(

                condition["keyword"],

                5
            )
        )


    # 상황 2개 → 각 2개 + 일반 플리 1개

    elif len(active_conditions) == 2:

        for condition in active_conditions:

            final_playlist.extend(

                get_playlist(

                    condition["keyword"],

                    2
                )
            )


        final_playlist.extend(

            get_playlist(

                "통학 플레이리스트",

                1
            )
        )


    # 상황 3개 → 각 상황 2개씩

    elif len(active_conditions) == 3:

        for condition in active_conditions:

            final_playlist.extend(
            
                get_playlist(

                    condition["keyword"],

                    2
                )
            )

    # 최종 랜덤 섞기
    random.shuffle(
        final_playlist
    )


    return final_playlist



# 테스트 코드

if __name__ == "__main__":


    playlist = recommend_playlist(

        # 비 올 확률
        rain_probability = 90,

        # 지각 확률
        late_probability = 70,

        # 현재 시각
        current_hour = 6
    )


    print("\n===== 추천 플레이리스트 =====\n")


    for music in playlist:

        print({

            "title":
            music["title"],

            "channel":
            music["channel"],

            "url":
            music["url"]
        })