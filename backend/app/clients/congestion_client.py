import requests
from datetime import datetime

# 인증키
API_KEYS = {
    "SUBWAY_CONGESTION": "KEY",   # 서울 데이터
    "SUBWAY_PASSENGER": "KEY",   # 서울 데이터
    "BUS_ROUTE_USER": "KEY",   # 경기 데이터
    "BUS_STATION_USER": "KEY"   # 경기 데이터
}

def get_congestion_weight(station_nm="죽전", bus_route_id="233000031"):
    now = datetime.now()
    # API 데이터 갱신 속도를 고려해 안전하게 며칠 전 날짜를 사용하거나 오늘 날짜 사용
    today = "20260501" 
    hour = now.strftime('%H')
    
    weights = 0.0

    # 지하철 혼잡도 (서울 데이터 - 현재 ERROR-500 대비 예외처리)
    try:
        url_1 = f"http://openapi.seoul.go.kr:8088/{API_KEYS['SUBWAY_CONGESTION']}/json/statnTrainConections/1/5/{station_nm}"
        res_1 = requests.get(url_1).json()
        # 변수명 확인: trainAlmTime, congestion
        for row in res_1.get('statnTrainConections', {}).get('row', []):
            if row.get('trainAlmTime') == hour:
                if float(row.get('congestion', 0)) > 120: 
                    weights += 0.08
                    print(f"-> 지하철 혼잡도 가중치 반영 (+0.08)")
                break
    except: 
        print("! 지하철 혼잡도 API 서버 오류로 건너뜁니다.")

    # 지하철 승하차인원
    try:
        url_2 = f"http://openapi.seoul.go.kr:8088/{API_KEYS['SUBWAY_PASSENGER']}/json/CardSubwayStatsNew/1/1000/{today}"
        res_2 = requests.get(url_2).json()
        for row in res_2.get('CardSubwayStatsNew', {}).get('row', []):
            # 최신 변수명: SBWY_STNS_NM, GTON_TNOPE, GTOFF_TNOPE
            if station_nm == row.get('SBWY_STNS_NM'):
                total = int(row.get('GTON_TNOPE', 0)) + int(row.get('GTOFF_TNOPE', 0))
                if total > 15000: 
                    weights += 0.05
                    print(f"-> 역별 승하차인원 가중치 반영 (+0.05)")
                break
    except: pass

    # 노선별 버스 이용객 (경기 데이터 - 리스트 인덱스 예외처리)
    try:
        url_3 = f"https://openapi.gg.go.kr/BusRouteUser?KEY={API_KEYS['BUS_ROUTE_USER']}&Type=json&ROUTE_ID={bus_route_id}"
        res_3 = requests.get(url_3).json()
        # 경기 데이터는 결과가 있으면 index 1에 데이터가 위치함
        data_list = res_3.get('BusRouteUser')
        if data_list and len(data_list) > 1:
            row_3 = data_list[1].get('row', [{}])[0]
            if int(row_3.get('RIDE_CNT', 0)) > 1000: 
                weights += 0.04
                print(f"-> 버스 노선 이용객 가중치 반영 (+0.04)")
    except: pass

    # 정류소간 버스 이용객 (경기 데이터)
    try:
        url_4 = f"https://openapi.gg.go.kr/BusRouteStationUser?KEY={API_KEYS['BUS_STATION_USER']}&Type=json&ROUTE_ID={bus_route_id}"
        res_4 = requests.get(url_4).json()
        data_list_4 = res_4.get('BusRouteStationUser')
        if data_list_4 and len(data_list_4) > 1:
            rows_4 = data_list_4[1].get('row', [])
            for row in rows_4:
                # 죽전역 명칭 포함 여부 확인
                if station_nm in row.get('STATION_NM', ''):
                    if int(row.get('ALIGHT_CNT', 0)) > 300: 
                        weights += 0.03
                        print(f"-> 정류소별 하차인원 가중치 반영 (+0.03)")
                        break
    except: pass

    return weights

if __name__ == "__main__":
    print(f"--- 📊 [{datetime.now().strftime('%H시')}] 혼잡도 가중치 분석 시작 ---")
    final_weight = get_congestion_weight("죽전", "233000031")
    print(f"\n✅ 최종 산출된 지각 확률 가중치: {round(final_weight * 100, 2)}%")