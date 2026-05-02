# commute_web_service

<실행시 참고사항>
1. venv/bin/activate 또는 source venv/bin/activate 로 가상환경 진입
2. 터미널에 있는 경로 앞 '(venv)'이 생성됨을 확인 후 진행
3. uvicorn app.main:app --reload 오류시, ls 명령어로 안에 app 폴더가 보이는지 확인 (app.py X)


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