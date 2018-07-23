
def tagging(URL, title):
	tag_list = []
	url = URL['info'].split('_')
	title = title.upper()

	if url[1] == "main":
		
		# 부경대 메인 공지사항
		if url[2] == "notice":
			tag_list.append("공지")

			if title.find("식단표") != -1:
				tag_list.append("주간식단표")

			if title.find("수강") != -1 or title.find("K-MOOC") != -1\
				or title.find("강좌") != -1:
				tag_list.append("수강")

			if title.find("장학") != -1:
				tag_list.append("장학생")

			if title.find("스터디") != -1 or title.find("공부") != -1\
			or title.find("모임") != -1:
				tag_list.append("스터디&모임")

		# 부경대 메인 자유게시판
		elif url[2] == "freeboard":
			tag_list.append("기타")

			if title.find("스터디") != -1 or title.find("공부") != -1\
			or title.find("모임") != -1:
				tag_list.append("스터디&모임")

			if title.find("알바") != -1 or title.find("아르바이트") != -1:
				tag_list.append("알바")

			if title.find("봉사") != -1:
				tag_list.append("봉사")

		# 부경대 메인 열린장터
		elif url[2] == "openmarket":
			tag_list.append("거래")
			return {"tag":tag_list}

		# 부경대 메인 동아리
		elif url[2] == "circle":
			tag_list.append("스터디&모임")

		# 부경대 메인 자취하숙
		elif url[2] == "boarding":
			tag_list.append("자취&하숙")
			return {"tag":tag_list}

		# 부경대 메인 알바
		elif url[2] == "parttimejob":
			tag_list.append("알바")

		# 부경대 메인 분실물센터
		elif url[2] == "lost":
			tag_list.append("분실물")
			return {"tag":tag_list}

		# 공용 부가 태그
		if title.find("과외") != -1 \
			or ((title.find("강사") != -1 or title.find("선생님") != -1)\
			and title.find("특강") == -1):
			tag_list.append("과외")

		if title.find("봉사") != -1 or url[2] == "volunteer":
			tag_list.append("봉사")

		if title.find("IT") != -1 or title.find("컴공") != -1\
			or (title.find("컴퓨터") != -1 and url[2] == "circle"):
			tag_list.append("IT")

		if title.find("토익") != -1 or title.find("토플") != -1\
			or title.find("TOEIC") != -1 or title.find("TOEFL") != -1\
			or title.find("외국인") != -1 or title.find("영어회화") != -1:
			tag_list.append("영어")

		if title.find("취업") != -1\
			or title.find("채용") != -1 or title.find("조교") != -1\
			or title.find("공채") != -1:
			tag_list.append("취업")

		if title.find("행사") != -1 or title.find("참가") != -1\
			or title.find("쇼") != -1 or title.find("프로그램") != -1:
			tag_list.append("행사")

		if title.find("특강") != -1:
			tag_list.append("특강")

		if title.find("멘토") != -1 or title.find("멘티") != -1:
			tag_list.append("멘토링")

		if title.find("인문학") != -1:
			tag_list.append("인문학")


	return {"tag":tag_list}