import requests
import xml.etree.ElementTree as ET

# 공공데이터포털 인증키
API_KEY = "1ece7d5a0ede503b80498ab64c86c4e0d219707cc99d7ff4479843f619b6abd0"

def get_realtime_24_bus():
    # 우리가 찾은 죽전역.수지레스피아 정류소 ID
    STATION_ID = "228001028"
    # 24번 버스의 진짜 노선 ID (아까 시스템에서 확인된 값)
    ROUTE_ID = "228000174" 

    url = f"http://openapi.gbis.go.kr/ws/rest/busarrivalservice/station?serviceKey={API_KEY}&stationId={STATION_ID}"
    
    print(f"--- 🚍 24번 버스 실시간 도착 정보 (죽전역.수지레스피아) ---")
    
    try:
        res = requests.get(url)
        root = ET.fromstring(res.content)
        arrival_list = root.findall(".//busArrivalList")
        
        found = False
        for arr in arrival_list:
            # 정류소에 오는 여러 버스 중 '24번(ROUTE_ID)'만 골라내기
            if arr.findtext('routeId') == ROUTE_ID:
                found = True
                print(f"✅ 24번 버스 확인!")
                print(f"📍 첫 번째: {arr.findtext('predictTime1')}분 후 도착 ({arr.findtext('locationNo1')}정류장 전)")
                print(f"📍 두 번째: {arr.findtext('predictTime2')}분 후 도착 ({arr.findtext('locationNo2')}정류장 전)")
                print(f"💺 잔여 좌석: {arr.findtext('remainSeatCnt1')}석")
                break
        
        if not found:
            print("⚠️ 현재 운행 중인 24번 버스 정보가 없습니다.")
            
    except Exception as e:
        print(f"❌ API 호출 중 오류 발생: {e}")

if __name__ == "__main__":
    get_realtime_24_bus()