def calculate_lateness_probability(weather=None, is_holiday=False, is_rush_hour=False):
	probability = 0
	reasons = []

	if weather == "rain":
		probability += 5
		reasons.append("비: +5%")

	if weather == "snow":
        	probability += 15
        	reasons.append("눈: +15%")

    	if is_holiday:
        	probability += 10
        	reasons.append("공휴일: +10%")

    	if is_rush_hour:
        	probability += 10
        	reasons.append("출근/퇴근시간: +10%")

    	if probability > 100:
        	probability = 100

    	return {
        	"lateness_probability": probability,
        	"reasons": reasons
    	}
