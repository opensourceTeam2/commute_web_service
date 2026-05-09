import requests

# [서울열린데이터광장] 시간대별 역별 승하차인원 인증키
SEOUL_DATA_KEY = "KEY"

def get_fever_time_analysis(station_name, current_hour):
    """
    프론트엔드로부터 역 이름과 시각을 전달받아 피버타임을 분석합니다.
    """
    service_name = "CardSubwayTime"
    target_date = "202404"
    
    # URL 인코딩 이슈 방지를 위한 전체 데이터 필터링 방식
    url = f"http://openapi.seoul.go.kr:8088/{SEOUL_DATA_KEY}/json/{service_name}/1/1000/{target_date}/"
    
    try:
        response = requests.get(url)
        res = response.json()
        
        if service_name not in res:
            return {"status": "error", "message": "API 응답 오류"}

        rows = res[service_name]['row']
        target_row = next((r for r in rows if station_name in r.get('STTN', '') and "분당" in r.get('SBWY_ROUT_LN_NM', '')), None)
        
        if not target_row:
            return {"status": "error", "message": f"'{station_name}'역 데이터를 찾을 수 없습니다."}

        # 1. 전 시간대 유동인구 합산 (승차+하차)
        traffic_by_hour = {h: float(target_row.get(f'HR_{h}_GET_ON_NOPE', 0)) + 
                             float(target_row.get(f'HR_{h}_GET_OFF_NOPE', 0)) for h in range(4, 24)}
        
        # 2. 상위 3개 피버타임 추출 (수정님 제안 로직)
        sorted_hours = sorted(traffic_by_hour.items(), key=lambda x: x[1], reverse=True)
        top_3_hours = sorted([item[0] for item in sorted_hours[:3]])
        
        # 3. 판별 및 결과물 조립
        is_fever = current_hour in top_3_hours
        
        return {
            "status": "success",
            "data": {
                "station": station_name,
                "input_hour": f"{current_hour}시",
                "is_fever_time": is_fever,
                "fever_hours_list": [f"{h}시" for h in top_3_hours],
                "peak_traffic": f"{int(sorted_hours[0][1]):,}명",
                "penalty_score": 15 if is_fever else 5
            }
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}

# ---------------------------------------------------------
# [프론트엔드 연동 가상 테스트]
# ---------------------------------------------------------
if __name__ == "__main__":
    print("\n" + "="*60)
    print(" 🖥️  Front-End -> Back-End API Call Simulation ")
    print("="*60)

    # 예시 1: 프론트에서 '죽전', '8시'를 보냈을 때
    sample_res1 = get_fever_time_analysis("죽전", 8)
    if sample_res1["status"] == "success":
        d = sample_res1["data"]
        print(f" [결과1] {d['station']}역 {d['input_hour']} 조회")
        print(f"  > 피버타임 여부: {'🔥 매 우 혼 잡' if d['is_fever_time'] else '✅ 원 활'}")
        print(f"  > 해당 역 피크 시간대: {d['fever_hours_list']}")
        print(f"  > 최대 유동인구: {d['peak_traffic']}")
        print(f"  > 적용 패널티: +{d['penalty_score']}%")
    
    print("-" * 60)

    # 예시 2: 프론트에서 '보정', '15시'를 보냈을 때
    sample_res2 = get_fever_time_analysis("보정", 15)
    if sample_res2["status"] == "success":
        d = sample_res2["data"]
        print(f" [결과2] {d['station']}역 {d['input_hour']} 조회")
        print(f"  > 피버타임 여부: {'🔥 매 우 혼 잡' if d['is_fever_time'] else '✅ 원 활'}")
        print(f"  > 해당 역 피크 시간대: {d['fever_hours_list']}")
        print(f"  > 적용 패널티: +{d['penalty_score']}%")

    print("="*60 + "\n")