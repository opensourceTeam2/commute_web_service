from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.services.route_service import recommend_commute_routes
from app.clients.extra.playlist import recommend_playlist
from app.clients.extra.points import calculate_points
from app.clients.extra.badges import update_badges
from app.clients.weather import get_weather
from app.db import database


app = FastAPI()


# 미니게임
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# React 프론트엔드에서 FastAPI 백엔드로 요청할 수 있게 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CommuteCalculateRequest(BaseModel):
    startLocation: str
    classStartTime: str
    loginId: Optional[str] = None


class RegisterRequest(BaseModel):
    loginId: str
    password: str
    nickname: Optional[str] = None


class LoginRequest(BaseModel):
    loginId: str
    password: str


@app.get("/")
def read_root():
    return {
        "message": "Commute Web Service Backend"
    }


@app.post("/api/auth/register")
def register(request: RegisterRequest):
    if request.loginId.strip() == "" or request.password.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="아이디와 비밀번호를 모두 입력해주세요."
        )

    if len(request.password) < 4:
        raise HTTPException(
            status_code=400,
            detail="비밀번호는 4자 이상 입력해주세요."
        )

    try:
        user = database.register_user(
            login_id=request.loginId,
            password=request.password,
            nickname=request.nickname
        )

        return {
            "success": True,
            "message": "회원가입이 완료되었습니다.",
            "user": user
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@app.post("/api/auth/login")
def login(request: LoginRequest):
    user = database.login_user(
        login_id=request.loginId,
        password=request.password
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="아이디 또는 비밀번호가 올바르지 않습니다."
        )

    return {
        "success": True,
        "message": "로그인 성공",
        "user": user
    }


@app.get("/api/auth/me")
def me(login_id: str):
    user = database.get_user_profile(login_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="사용자를 찾을 수 없습니다."
        )

    return user


@app.post("/api/commute/calculate")
def calculate_commute(request: CommuteCalculateRequest):
    print("\n========== 통학 경로 계산 요청 시작 ==========")
    print("출발 위치:", request.startLocation)
    print("수업 시작 시간:", request.classStartTime)

    try:
        result = recommend_commute_routes(
            start_location=request.startLocation,
            class_start_time=request.classStartTime,
        )

        database.add_log(
            login_id=request.loginId,
            checked_at=datetime.now().strftime("%Y.%m.%d. %H:%M:%S"),
            start_location=request.startLocation,
            class_start_time=request.classStartTime,
            route_summary=result["routes"][0]["routeSummary"],
            total_minutes=result["routes"][0]["totalMinutes"],
            late_probability=result["routes"][0]["lateProbability"]
        )

        return {
            "loginId": request.loginId,
            "startLocation": request.startLocation,
            "startPlace": result["startPlace"],
            "destination": "단국대학교 죽전캠퍼스",
            "destinationPlace": result["destinationPlace"],
            "classStartTime": request.classStartTime,
            "checkedAt": datetime.now().strftime("%Y.%m.%d. %H:%M:%S"),
            "routes": result["routes"],
        }

    except ValueError as error:
        print("400 에러 원인:", str(error))

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:
        import traceback

        print("500 에러 원인:", str(error))
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"통학 계산 중 오류가 발생했습니다: {error}",
        )


@app.get("/game")
def game():
    return FileResponse("app/templates/game.html")


@app.get("/playlist")
def playlist(late_probability: int):
    # 용인 좌표
    nx = 62
    ny = 123

    weather_result = get_weather(nx, ny)

    rain_type = "없음"

    if weather_result and len(weather_result) > 0:
        rain_type = weather_result[0]["rain_type"]

    current_hour = datetime.now().hour

    playlist_result = recommend_playlist(
        rain_type=rain_type,
        late_probability=late_probability,
        current_hour=current_hour
    )

    return {
        "playlist": playlist_result
    }


@app.get("/points")
def points(
    login_id: str,
    late_probability: int,
    commute_minutes: int,
    class_start_time: str
):
    database.create_user(login_id)
    database.validate_semester(login_id)

    # 용인 좌표
    nx = 62
    ny = 123

    weather_result = get_weather(nx, ny)

    if weather_result and len(weather_result) > 0:
        rain_type = weather_result[0]["rain_type"]
    else:
        rain_type = "없음"

    current_hour = datetime.now().hour

    now = datetime.now()

    current_minutes = (
        now.hour * 60 + now.minute
    )

    period, time_str = class_start_time.split()
    hour, minute = map(
        int,
        time_str.split(":")
    )

    if period == "오후" and hour != 12:
        hour += 12

    if period == "오전" and hour == 12:
        hour = 0

    class_minutes = (
        hour * 60 + minute
    )

    is_on_time = (
        current_minutes <= class_minutes
    )

    is_rush_hour = (
        7 <= current_hour < 9 or
        17 <= current_hour < 19
    )

    result = calculate_points(
        late_probability=late_probability,
        rain_type=rain_type,
        is_rush_hour=is_rush_hour,
        is_arrived=is_on_time
    )

    database.add_points(
        login_id,
        result["earned_points"]
    )

    badge_data = database.get_badges(login_id)

    if badge_data is None:
        badge_data = {
            "easy_success_count": 0,
            "hard_success_count": 0,
            "rain_success_count": 0,
            "early_morning_count": 0,
            "long_distance_count": 0
        }

    badge_result = update_badges(
        login_id=login_id,
        badge_data=badge_data,
        late_probability=late_probability,
        rain_type=rain_type,
        current_hour=current_hour,
        commute_minutes=commute_minutes,
        is_on_time=is_on_time
    )

    return {
        "point_result": result,
        "badge_result": badge_result
    }


@app.get("/badge")
def badge(login_id: str):
    database.validate_semester(login_id)

    total_points = database.get_points(login_id)
    badge_data = database.get_badges(login_id)

    if badge_data is None:
        badge_data = {
            "easy_success_count": 0,
            "hard_success_count": 0,
            "rain_success_count": 0,
            "early_morning_count": 0,
            "long_distance_count": 0
        }

    badge_list = []

    if badge_data["easy_success_count"] >= 30:
        badge_list.append("여유로운 통학의 신")

    if badge_data["hard_success_count"] >= 10:
        badge_list.append("아슬아슬 마스터")

    if badge_data["rain_success_count"] >= 10:
        badge_list.append("비를 뚫는 자")

    if badge_data["early_morning_count"] >= 20:
        badge_list.append("새벽 통학생")

    if badge_data["long_distance_count"] >= 20:
        badge_list.append("강철 체력")

    return {
        **badge_data,
        "total_points": total_points,
        "badge_list": badge_list,
        "badge_count": len(badge_list),
    }


@app.get("/logs")
def logs(login_id: str):
    database.validate_semester(login_id)

    return database.get_logs(login_id)


@app.post("/buy-theme")
def buy_theme(
    login_id: str,
    theme_name: str
):
    result = database.buy_theme(
        login_id,
        theme_name
    )

    return result


@app.post("/apply-theme")
def apply_theme(
    login_id: str,
    theme_name: str
):
    return database.apply_theme(
        login_id,
        theme_name
    )


@app.get("/themes")
def get_themes(login_id: str):
    return database.get_themes(login_id)


@app.get("/semester")
def semester():
    return {
        "semester": database.get_current_semester()
    }