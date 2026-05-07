import requests
from datetime import datetime

def get_day_status():
    """
    오늘의 날짜 상태를 판별
    우선순위: 1. 공휴일(빨간 날) > 2. 주말 > 3. 평일
    """
    now = datetime.now()
    today_str = now.strftime('%Y%m%d')
    
    # 공휴일 체크
    url = "http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo"
    params = {
        "serviceKey": "1ece7d5a0ede503b80498ab64c86c4e0d219707cc99d7ff4479843f619b6abd0",
        "solYear": now.strftime('%Y'),
        "solMonth": now.strftime('%m'),
        "_type": "json"
    }
    
    try:
        response = requests.get(url, params=params).json()
        body = response.get('response', {}).get('body', {})
        
        if body.get('totalCount', 0) > 0:
            items = body.get('items', {}).get('item', [])
            if isinstance(items, dict): 
                items = [items]
            
            for item in items:
                # 공휴일이면 주말 여부와 상관없이 즉시 반환
                if str(item['locdate']) == today_str:
                    return f"공휴일({item['dateName']})"
    except:
        pass

    # 주말 체크 (공휴일이 아닐 때만 실행)
    day_of_week = now.weekday() # 0:월, 1:화, 2:수, 3:목, 4:금, 5:토, 6:일
    if day_of_week == 5:
        return "주말(토요일)"
    elif day_of_week == 6:
        return "주말(일요일)"

    # 모두 해당 없으면 평일
    return "평일"

if __name__ == "__main__":
    status = get_day_status()
    print("="*40)
    print(f" 조회 날짜: {datetime.now().strftime('%Y-%m-%d')}")
    print(f" 오늘의 상태: {status}")
    print("="*40)