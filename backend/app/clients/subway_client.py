import requests

# 인증키
KEYS = {
    "ARRIVAL": "KEY",   # 실시간 도착정보
    "POSITION": "KEY"   # 실시간 열차 위치정보
}

def get_subway_status_v2(station_nm="죽전"):
    # [1] 실시간 도착 정보 호출
    arrival_url = f"http://swopenapi.seoul.go.kr/api/subway/{KEYS['ARRIVAL']}/json/realtimeStationArrival/0/5/{station_nm}"
    arrival_data = requests.get(arrival_url).json()
    
    # [2] 실시간 열차 위치 정보 호출 (수인분당선)
    pos_url = f"http://swopenapi.seoul.go.kr/api/subway/{KEYS['POSITION']}/json/realtimePosition/0/50/수인분당선"
    pos_data = requests.get(pos_url).json()

    print(f"\n--- 🚉 {station_nm}역 통합 관제 모니터링 (상세) ---")

    # [1] 도착 예정 정보 (ETA)
    if "realtimeArrivalList" in arrival_data:
        print(f"\n[1] 도착 예정 정보 (ETA)")
        for arr in arrival_data["realtimeArrivalList"]:
            # arvlMsg2에 이미 '진입', '도착' 등의 텍스트가 포함되어 나옵니다.
            print(f" ▶ {arr.get('trainLineNm')}: {arr.get('arvlMsg2')}")
    
    # [2] 위치 정보 출력 (진입/도착/출발 세분화)
    if "realtimePositionList" in pos_data:
        print(f"\n[2] 주변 역 실제 열차 위치")
        for pos in pos_data["realtimePositionList"]:
            statn_nm = pos.get('statnNm')
            
            # 죽전역 주변 역들만 필터링
            if statn_nm in ["죽전", "오리", "보정", "미금", "구성"]:
                updn = "상행(왕십리)" if pos.get('updnLine') == "0" else "하행(인천/고색)"
                
                # trainSttus 코드 세분화
                # 0: 진입, 1: 도착, 2: 출발, 3: 전역출발
                raw_status = pos.get('trainSttus')
                if raw_status == "0":
                    status = "🔔 진입 중"
                elif raw_status == "1":
                    status = "🛑 도착/정차"
                elif raw_status == "2":
                    status = "🚀 출발 완료"
                else:
                    status = "🏃 주행 중"
                
                print(f" 📍 {statn_nm}역 ({updn}) - 상태: {status} (열차번호: {pos.get('trainNo')})")

if __name__ == "__main__":
    get_subway_status_v2("죽전")