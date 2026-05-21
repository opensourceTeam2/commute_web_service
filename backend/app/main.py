from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.services.route_service import recommend_commute_routes


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


@app.get("/")
def read_root():
    return {"message": "Commute Web Service Backend"}


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

        return {
            "loginId": request.loginId,
            "startLocation": request.startLocation,
            "startPlace": result["startPlace"],
            "destination": "단국대학교 죽전캠퍼스",
            "destinationPlace": result["destinationPlace"],
            "classStartTime": request.classStartTime,
            "checkedAt": datetime.now().strftime("%Y. %m. %d. %H:%M:%S"),
            "routes": result["routes"],
        }

    except ValueError as error:
        print("400 에러 원인:", str(error))
        raise HTTPException(status_code=400, detail=str(error))

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