import json
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("logs.json")

def save_log(user_input, result):
	log = {
		"time": datetime.now().strftime("%Y-%m-%d %H: %M: %S"),
		"user_input": user_input,
		"result": result
	}

	if LOG_FILE.exists():
		with open(LOG_FILE, "r", encoding = "utf-8") as f:
			logs = json.load(f)
	else:
		logs = []

	logs.append(log)

	with open(LOG_FILE, "w", encoding="utf-8") as f:
		json.dump(logs, f, ensure_ascii=False, indent=4)

	return log

def get_logs():
	if LOG_FILE.exists():
		with open(LOG_FILE, "r", encoding="utf-8") as f:
			return json.load(f)
	return []
