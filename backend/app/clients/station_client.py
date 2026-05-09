import requests

# 인증키
GYEONGGI_KEY = "f3589e2f0e154c6ab44348a527ffe283"
RAIL_API_KEY = "$2a$10$crFZ6BOcvthSaMBJtsVveeqCHOep1xGf5uJGVcVtlrITmFo4aO7rO"

class StationClient:
    def __init__(self):
        self.bus_key = GYEONGGI_KEY
        self.rail_key = RAIL_API_KEY
        # 우리가 확정한 24번 버스 정류소 ID 3개
        self.target_bus_ids = ["228001028", "228001055", "228002971"]

    # [1] 지하철 위치 정보 (레일포털 - 파라미터 최소화로 재시도)
    def get_subway_location(self, station_nm):
        url = "	https://openapi.kric.go.kr/openapi/trainUseInfo/subwayRouteInfo"
        params = {
            "serviceKey": self.rail_key,
            "format": "json",
            "statnNm": station_nm # '죽전'만 넣어봅니다
        }
        try:
            res = requests.get(url, params=params)
            return res.json()
        except:
            return "지하철 연결 실패"

    # [2] 확정된 버스 정류소 정보들만 가져오기
    def get_fixed_bus_stops(self):
        url = "https://openapi.gg.go.kr/BusStation"
        # 용인시 데이터 중 우리가 찾은 ID만 필터링
        params = {
            "KEY": self.bus_key,
            "Type": "json",
            "pIndex": 1,
            "pSize": 1000,
            "SIGUN_NM": "용인시"
        }
        
        try:
            res = requests.get(url, params=params)
            data = res.json()
            rows = data["BusStation"][1]["row"]
            # 우리 ID 3개에 해당하는 데이터만 추출
            return [r for r in rows if r.get('STATION_ID') in self.target_bus_ids]
        except:
            return "버스 연결 실패"

if __name__ == "__main__":
    client = StationClient()
    
    print("--- 🚉 [지하철] 죽전역 위치 정보 ---")
    subway = client.get_subway_location("죽전")
    print(subway)
    
    print("\n--- 🚍 [버스] 확정된 24번 정류소 리스트 ---")
    bus_stops = client.get_fixed_bus_stops()
    for s in bus_stops:
        print(f"📍 {s.get('STATION_NM_INFO')} ({s.get('STATION_ID')})")
        print(f"   위치: {s.get('WGS84_LAT')}, {s.get('WGS84_LOGT')}")