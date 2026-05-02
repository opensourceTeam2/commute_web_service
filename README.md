# commute_web_service

<백엔드 디렉토리 구성>
1. app/main.py
    FastAPI 실행 시작점
2. api/routes/
    API 주소를 관리하는 디렉토리
3. services/
    가장 중요한 경로 추천, 지각확률 계산, 날씨/미세먼지 문구생성, 결과 저장 및 불러오기 기능을 수행하는 디렉토리
4. clients/
    외부 API 호출하는 코드를 보관하는 디렉토리
5. schemas/
    API 요청과 응답 데이터의 형식(자료형)을 정의하는 디렉토리
6. models/
    DB와 연결되는 객체를 보관하는 디렉토리
7. db/
    DB 연결 설정을 관리하는 디렉토리

<프론트엔드 디렉토리 구성>
1. 