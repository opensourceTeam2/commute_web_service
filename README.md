# commute_web_service

<실행 방법>
1. python venv 가상환경 실행, 터미널에 있는 경로 앞 '(venv)'이 생성됨을 확인 후 진행
2. pip install -r requirements.txt로 필요한 패키지 다운로드
3. uvicorn app.main:app --reload (Backend 실행)
4. npm start (Frontend 실행)


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
## 참고한 오픈소스

- Repository: marqbeniamin/argon-design-system-react
- License: MIT License
- Usage: React 기반 페이지 구조를 참고하여 통학 경로 추천 서비스 홈 화면으로 수정함

1. scr/index.js
- 주소 연결 + 로그인 제한 (로그인하지 않은 사용자가 네비게이션바의 기능을 사용할 시, 로그인 페이지로 연결함)

2. src/components/Navbars/DemoNavbar.js
- 상단 메뉴 [통학도우미(메인), 통학도우미 실행(메인기능), 설정(사용자 입력창), 로그(통학도우미 실행 기록 조회), 로그인(회원 정보 기입)]

3. src/views/examples/Login.js
- 로그인 화면 (사용자 아이디와 비번만 받음)

4. src/views/examples/Settings.js
- 설정 페이지(/settings) 정류장, 버스번호, 수업시작 시간 입력

5. src/views/examples/Commute.js
- 통학 도우미 실행 페이지 (결과 출력창) (API와 연결 예정)

6. src/views/Logs.js
- 로그 페이지

7. src/views/examples/Landing.js
- 메인화면 페이지

## 참고한 API
1. 