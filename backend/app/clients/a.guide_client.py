import requests
from datetime import datetime, timedelta

# 인증키 설정
PUBLIC_DATA_KEY = "KEY"

def get_weather_guide():
    """기상청 단기예보를 통해 강수 상태 확인 및 안내 문구 생성"""
    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
    
    # 1. 최신 발표 시점 계산 (기상청 3시간 주기 대응)
    now = datetime.now()
    current_hour = now.hour
    
    # 발표 주기 리스트: 02, 05, 08, 11, 14, 17, 20, 23
    base_hours = [2, 5, 8, 11, 14, 17, 20, 23]
    # 현재 시각보다 이전이면서 가장 가까운 발표 시각 찾기
    past_hours = [h for h in base_hours if h <= current_hour]
    
    if not past_hours: # 00시, 01시 등인 경우 전날 23시 데이터 사용
        base_date = (now - timedelta(days=1)).strftime('%Y%m%d')
        base_time = "2300"
    else:
        base_date = now.strftime('%Y%m%d')
        base_time = f"{max(past_hours):02d}00"

    params = {
        "serviceKey": PUBLIC_DATA_KEY,
        "dataType": "JSON",
        "base_date": base_date,
        "base_time": base_time,
        "nx": "62", "ny": "121", # 죽전 인근 좌표
        "numOfRows": "100"
    }

    try:
        res = requests.get(url, params=params).json()
        items = res['response']['body']['items']['item']
        
        # 'PTY'(강수 형태) 확인: 0(없음), 1(비), 2(비/눈), 3(눈), 4(소나기)
        # 'POP'(강수 확률) 확인
        rain_status = "0"
        rain_prob = "0"
        
        for item in items:
            if item['category'] == 'PTY':
                rain_status = item['fcstValue']
            if item['category'] == 'POP':
                rain_prob = item['fcstValue']
        
        # 안내 문구 로직
        if rain_status != "0":
            return f"☔ 현재 비나 눈 예보가 있습니다. 우산을 꼭 챙기세요! (강수 확률: {rain_prob}%)"
        elif int(rain_prob) >= 50:
            return f"☁️ 강수 확률이 {rain_prob}%로 높습니다. 우산을 챙기는 것을 추천드려요."
        else:
            return "☀️ 맑은 날씨입니다. 가벼운 차림으로 등교하세요!"
            
    except:
        return "⚠️ 날씨 정보를 불러오는 데 실패했습니다."

def get_air_guide():
    """대기오염정보(에어코리아)를 통해 미세먼지 등급 확인 및 안내 문구 생성"""
    url = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty"
    params = {
        "serviceKey": PUBLIC_DATA_KEY,
        "returnType": "json",
        "stationName": "수지", # 죽전과 가장 가까운 측정소
        "dataTerm": "DAILY",
        "ver": "1.0"
    }

    try:
        res = requests.get(url, params=params).json()
        item = res['response']['body']['items'][0]
        
        grade = item.get('pm10Grade') # 1:좋음, 2:보통, 3:나쁨, 4:매우나쁨
        
        if grade == '1':
            return "🍃 미세먼지 농도가 좋습니다. 공기가 쾌적해요!"
        elif grade == '2':
            return "✅ 미세먼지 농도가 보통입니다."
        elif grade == '3':
            return "😷 미세먼지가 나쁩니다. 마스크를 꼭 착용하세요!"
        elif grade == '4':
            return "🚨 미세먼지 매우 나쁨! 가급적 외출을 자제하고 마스크를 착용하세요."
        else:
            return "🔍 미세먼지 정보를 확인 중입니다."
            
    except:
        return "⚠️ 미세먼지 정보를 불러오는 데 실패했습니다."

if __name__ == "__main__":
    print("\n" + "="*50)
    print(" [Part 1. 실시간 등교 가이드 - 안내 문구 파트] ")
    print("="*50)
    print(f" 📅 확인 시각: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f" {get_weather_guide()}")
    print(f" {get_air_guide()}")
    print("="*50 + "\n")