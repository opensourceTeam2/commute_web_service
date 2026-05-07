import requests

# 인증키
SEOUL_DATA_KEY = "64445a6d71637279383553656b4247"

def get_fever_times_safe():
    service_name = "CardSubwayTime"
    target_date = "202604"
    # 우리가 찾고 싶은 역 리스트
    target_stations = ["죽전", "오리", "미금", "정자", "보정", "구성", "신갈", "기흥", "상갈", "청명"]
    
    url = f"http://openapi.seoul.go.kr:8088/{SEOUL_DATA_KEY}/json/{service_name}/1/1000/{target_date}/"
    
    print(f"\n🔍 [수인분당선 구간 피버타임 데이터 필터링 분석 - {target_date}]")
    print("="*65)

    try:
        response = requests.get(url)
        res = response.json()

        if service_name in res:
            rows = res[service_name]['row']
            found_count = 0

            for row in rows:
                line_name = row.get('SBWY_ROUT_LN_NM', '')
                station_name = row.get('STTN', '')

                # 수인분당선(또는 분당선)이면서 우리가 찾는 10개 역 중 하나라면 분석
                if ("분당" in line_name) and (station_name in target_stations):
                    traffic_by_hour = {}
                    
                    # 4시부터 23시까지 데이터 합산
                    for h in range(4, 24):
                        on = float(row.get(f'HR_{h}_GET_ON_NOPE', 0))
                        off = float(row.get(f'HR_{h}_GET_OFF_NOPE', 0))
                        traffic_by_hour[h] = on + off

                    # 상위 3개 피버타임 추출
                    fever_hours = sorted(traffic_by_hour, key=traffic_by_hour.get, reverse=True)[:3]
                    fever_hours_str = ", ".join([f"{h}시" for h in sorted(fever_hours)])
                    
                    print(f" ✅ {station_name:4s}역 ({line_name}) | 피버타임: {fever_hours_str}")
                    found_count += 1
            
            if found_count == 0:
                print(" ❌ 해당 날짜의 수인분당선 데이터를 찾을 수 없습니다. (날짜 확인 필요)")
        else:
            print(f" ❌ API 응답 오류: {res.get('RESULT', {}).get('MESSAGE', '데이터 없음')}")

    except Exception as e:
        print(f" ❌ 시스템 오류: {e}")

    print("="*65 + "\n")

if __name__ == "__main__":
    get_fever_times_safe()