import requests
from datetime import datetime

SEOUL_DATA_KEY = "64445a6d71637279383553656b4247"
PUBLIC_DATA_KEY = "1ece7d5a0ede503b80498ab64c86c4e0d219707cc99d7ff4479843f619b6abd0"

def get_late_probability(station_name, current_hour):
    target_date = datetime.now().strftime('%Y%m%d')
    
    # 1. 공휴일 체크
    try:
        res_h = requests.get("http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo", 
                             params={"serviceKey": PUBLIC_DATA_KEY, "solYear": target_date[:4], "solMonth": target_date[4:6], "_type": "json"}).json()
        items = res_h.get('response', {}).get('body', {}).get('items', {}).get('item', [])
        if isinstance(items, dict): items = [items]
        if any(str(it['locdate']) == target_date for it in items):
            return {"status": "holiday", "message": "오늘은 공휴일이므로 지각 확률이 0%입니다."}
    except: pass

    # 2. 기본 및 날씨 가중치 계산
    total_prob = 5 
    weather_log = "평일 기본 가중치: +5%"
    rain_log = "맑음: +0%"

    try:
        res_w = requests.get("http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst", 
                             params={"serviceKey": PUBLIC_DATA_KEY, "dataType": "JSON", "base_date": target_date, "base_time": "1400", "nx": "62", "ny": "121", "numOfRows": "50"}).json()
        pop = next((int(i['fcstValue']) for i in res_w['response']['body']['items']['item'] if i['category'] == 'POP'), 0)
        if pop >= 50:
            total_prob += 10
            rain_log = f"비 가중치(강수확률 {pop}%): +10%"
        else:
            rain_log = f"맑음(강수확률 {pop}%): +0%"
    except: pass

    # 3. 피버타임 3단계 정밀 분석
    fever_data = {}
    try:
        # 데이터가 가장 안정적인 202604로 조회
        res_s = requests.get(f"http://openapi.seoul.go.kr:8088/{SEOUL_DATA_KEY}/json/CardSubwayTime/1/1000/202604/").json()
        rows = res_s['CardSubwayTime']['row']
        target_row = next((r for r in rows if station_name in r['STTN'] and "분당" in r['SBWY_ROUT_LN_NM']), None)
        
        if target_row:
            traffic = {h: float(target_row[f'HR_{h}_GET_ON_NOPE']) + float(target_row[f'HR_{h}_GET_OFF_NOPE']) for h in range(4, 24)}
            # 인원수 기준으로 내림차순 정렬
            sorted_traffic = sorted(traffic.items(), key=lambda x: x[1], reverse=True)
            
            top_1_hour = sorted_traffic[0][0] # 유동인구 1위 시간
            top_2_3_hours = [sorted_traffic[1][0], sorted_traffic[2][0]] # 2, 3위 시간
            
            # 3단계 판별 로직
            if current_hour == top_1_hour:
                status_text = "🔥 매 우 혼 잡"
                penalty = 15
            elif current_hour in top_2_3_hours:
                status_text = "🟠 혼 잡"
                penalty = 10
            else:
                status_text = "✅ 원 활"
                penalty = 5
                
            total_prob += penalty
            fever_data = {
                "status_text": status_text,
                "peak_hours": [f"{h}시" for h in sorted([top_1_hour] + top_2_3_hours)],
                "max_traffic": f"{int(sorted_traffic[0][1]):,}명",
                "penalty": penalty
            }
    except: pass

    return {
        "station": station_name,
        "hour": current_hour,
        "total_prob": total_prob,
        "weather_log": weather_log,
        "rain_log": rain_log,
        "fever_data": fever_data
    }

if __name__ == "__main__":
    # 테스트: 죽전역 8시
    res = get_late_probability("죽전", 8)
    
    print("\n" + "="*55)
    print(f"📍 역: {res['station']} / 시간: {res['hour']}시")
    print(f"🚩 최종 지각 확률: {res['total_prob']}%")
    print("-" * 55)
    print(f" > {res['weather_log']}")
    print(f" > {res['rain_log']}")
    print("-" * 55)
    fd = res['fever_data']
    print(f" > 피버타임 여부: {fd['status_text']}")
    print(f" > 해당 역 피크 시간대: {fd['peak_hours']}")
    print(f" > 최대 유동인구: {fd['max_traffic']}")
    print(f" > 적용 패널티: +{fd['penalty']}%")
    print("="*55 + "\n")