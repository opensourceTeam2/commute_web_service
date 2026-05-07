import requests
from datetime import datetime

STAT_KEY = "576667566d6372793634694f586241"

def get_seat_analysis(current_station, direction="하행"):
    """
    station_name: 현재 위치한 역
    direction: 상행(서울행) 또는 하행(수원행)
    """
    target_date = "202404"
    # 죽전 인근 10개 역 리스트
    stations = ["정자", "미금", "오리", "죽전", "보정", "구성", "신갈", "기흥", "상갈", "청명"]
    current_hour = datetime.now().hour
    
    url = f"http://openapi.seoul.go.kr:8088/{STAT_KEY}/json/CardSubwayTime/1/1000/{target_date}/"
    
    try:
        res = requests.get(url).json()
        rows = res['CardSubwayTime']['row']
        
        # 1. 방향 가중치 설정 (오전 8시 기준 추정)
        # 오전 하행선은 상행선보다 하차 비중이 낮으므로 전체 하차의 약 30%만 하행으로 가정
        dir_factor = 0.3 if direction == "하행" else 0.7
        
        # 2. 10개 역 하차 데이터 분석
        analysis_report = []
        for st in stations:
            row = next((r for r in rows if st in r['STTN'] and "분당" in r['SBWY_ROUT_LN_NM']), None)
            if row:
                off_total = float(row.get(f'HR_{current_hour}_GET_OFF_NOPE', 0))
                # 방향성을 고려한 하차 인원 추정
                estimated_off = int(off_total * dir_factor)
                
                # 착석 확률 계산 (추정치 기반 보정)
                # (예상하차 / 500) * 100 형태로 보정 (500명 내릴 때 확률 대폭 상승)
                prob = min(int((estimated_off / 500) * 100), 90)
                if prob < 10: prob = 15
                
                analysis_report.append({
                    "station": st,
                    "off_count": estimated_off,
                    "prob": prob
                })

        # 3. 현재 내가 있는 역의 데이터 추출
        my_data = next((item for item in analysis_report if item['station'] == current_station), None)
        
        # 4. 주변 역 중 가장 앉기 좋은 'Best 역' 추천
        best_st = max(analysis_report, key=lambda x: x['off_count'])

        return {
            "status": "success",
            "direction": direction,
            "current": my_data,
            "best_option": best_st,
            "full_report": analysis_report
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    # 테스트: 죽전역에서 하행선을 타고 있을 때
    res = get_seat_analysis("죽전", "하행")
    
    if res["status"] == "success":
        cur = res['current']
        best = res['best_option']
        
        print("\n" + "="*60)
        print(f" 💺 [수인분당선 {res['direction']}] 실시간 착석 분석 ")
        print("="*60)
        print(f"📍 현재 역: {cur['station']}역")
        print(f"🚩 착석 확률: {cur['prob']}% (약 {cur['off_count']}명 하차 예상)")
        print("-" * 60)
        print(f"💡 착석 팁: 현재 구간에서 {best['station']}역의 하차 인원이")
        print(f"   가장 많습니다. {best['station']}역에서 자리를 노려보세요!")
        print("="*60 + "\n")