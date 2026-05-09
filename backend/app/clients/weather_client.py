import requests
from datetime import datetime, timedelta

def get_weather_forecast():
    """현재 시간을 기준으로 가장 최신 예보를 가져와 날짜와 시간을 함께 반환"""
    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
    
    # 1. 현재 시각에 맞춰 최신 발표 시점 찾기
    now = datetime.now()
    
    # 기상청 발표 주기: 02, 05, 08, 11, 14, 17, 20, 23 (3시간 간격)
    # 발표 후 데이터 처리 시간을 고려하여 10분 정도 여유
    current_hour = now.hour
    
    if current_hour < 2:
        base_date = (now - timedelta(days=1)).strftime('%Y%m%d')
        base_time = "2300"
    elif current_hour < 5:
        base_date = now.strftime('%Y%m%d')
        base_time = "0200"
    elif current_hour < 8:
        base_date = now.strftime('%Y%m%d')
        base_time = "0500"
    elif current_hour < 11:
        base_date = now.strftime('%Y%m%d')
        base_time = "0800"
    elif current_hour < 14:
        base_date = now.strftime('%Y%m%d')
        base_time = "1100"
    elif current_hour < 17:
        base_date = now.strftime('%Y%m%d')
        base_time = "1400"
    elif current_hour < 20:
        base_date = now.strftime('%Y%m%d')
        base_time = "1700"
    elif current_hour < 23:
        base_date = now.strftime('%Y%m%d')
        base_time = "2000"
    else:
        base_date = now.strftime('%Y%m%d')
        base_time = "2300"

    params = {
        "serviceKey": "KEY",
        "dataType": "JSON",
        "base_date": base_date, 
        "base_time": base_time,
        "nx": "62", "ny": "121",
        "numOfRows": "1000"
    }
    
    try:
        response = requests.get(url, params=params).json()
        items = response['response']['body']['items']['item']
        
        forecast_list = []
        for item in items:
            if item['category'] == 'POP': # 강수 확률
                # 날짜를 읽기 쉽게 변환 (예: 20260506 -> 05월 06일)
                f_date = f"{item['fcstDate'][4:6]}월 {item['fcstDate'][6:8]}일"
                f_time = f"{item['fcstTime'][:2]}시"
                prob = item['fcstValue']
                forecast_list.append(f"{f_date} {f_time} -> 비 올 확률: {prob}%")
        
        return forecast_list[:12] # 향후 12시간 정보 반환
    except:
        return ["날씨 예보를 가져오지 못했습니다."]

def get_air_pollution_now():
    """실시간 미세먼지 정보"""
    url = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty"
    params = {
        "serviceKey": "KEY",
        "returnType": "json", "stationName": "수지", "dataTerm": "DAILY", "ver": "1.0"
    }
    
    try:
        response = requests.get(url, params=params).json()
        item = response['response']['body']['items'][0]
        pm10 = item['pm10Value']
        grade = item['pm10Grade']
        
        # 등급에 따른 텍스트 가이드
        status = "확인 불가"
        if grade == '1': status = "쾌적함"
        elif grade == '2': status = "보통"
        elif grade == '3': status = "마스크 필요"
        elif grade == '4': status = "외출 자제"
        
        return {
            "농도": f"{pm10} (등급: {grade})",
            "상태": status
        }
    except:
        return {"농도": "정보 없음", "상태": "확인 불가"}

if __name__ == "__main__":
    print("\n" + "="*45)
    print("      [강수 확률과 미세먼지 정보]      ")
    print("="*45)
    
    # 1. 날씨 예보 출력
    print("\n[1] 시간별 강수 예측")
    for f in get_weather_forecast():
        print(f" {f}")
        
    print("-" * 45)
    
    # 2. 미세먼지 출력
    air = get_air_pollution_now()
    print("[2] 실시간 미세먼지")
    print(f" -> 현재 미세먼지: {air['농도']}")
    print(f" -> 행동 가이드: {air['상태']}")
    print("="*45 + "\n")