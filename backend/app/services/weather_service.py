def create_guide_message(weather=None, fine_dust=None):
	messages = []

	if weather == "rain":
		messages.append("우산을 챙기세요.")

	if weather == "snow":
		messages.append("눈이 오니 이동 시간을 여유 있게 잡으세요.")

	if fine_dust == "bad":
		messages.append("미세먼지가 나쁘니 마스크를 착용하세요.")

	if not messages:
		messages.append("특별한 안내 사항 없음")

	return messages
