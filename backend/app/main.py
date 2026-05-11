from fastapi import FastAPI
from services.saved_route_service import save_log, get_logs

app = FastAPI()

@app.get("/")
def read_root() :
    return {"Hello" : "OpenSource"}

@app.post("/logs")
def create_log(data: dict):

	user_input = data.get("user_input")
	result = data.get("result")

	saved_log = save_log(user_input, result)

	return {
		"message": "로그 저장 완료",
		"log": saved_log
	}

@app.get("/log")
def read_logs()"

	return {
		"logs": getlogs()
	}

