import sys
import re

def alpha(text, cnt):
	alp = "QWERTYUIOPASDFGHJKLZXCVBNM"
	ck = 0
	if cnt == 0:
		title = text[0:3]
	else:
		title = text[cnt-1:cnt+3]

	for i in title:
		if i in alp:
			ck += 1
	return ck


def tagging(URL, title):
	tag_list = []
	url = URL['info'].split('_')
	title = title.upper()

	### 부경대 메인 홈페이지
	if url[1] == "main":
		tag_main(url, title, tag_list)
		if url[2] == "openmarket" or url[2] == "boarding"\
		or url[2] == "lost":
			return {"tag":tag_list}

	### 부경대 인재개발원 (공모전 및 교육 제외)
	elif url[1] == 'job' \
	and (url[2] != 'competition' and url[2] != 'education'):
		tag_job(url, title, tag_list)

	#부경대 인재 공모전/대외활동
	elif url[1] == 'job' and url[2] == 'competition':
		tag_list.append("공모전&대외활동")
		if title.find("[스펙업]") != -1:
			tag_list.append("스펙업")

	#부경대 인재 교육 및 설명회
	elif url[1] == 'job' and url[2] == 'education':
		tag_list.append("교육&설명회")

	#부경대 컴퓨터공학과 홈페이지
	elif url[1] == "ce":
		tag_ce(url, title, tag_list)

	elif url[1] == "pknu":
		tag_pknu(url, title, tag_list)

	elif url[1] == "today":
		tag_list.append("부경투데이")

	elif url[1] == "pknulogin":
		if url[2] == 'market':
			tag_list.append("거래")

	elif url[1] == "dorm":
		tag_list.append("기숙사")
		if url[2] == 'notice':
			tag_list.append("공지")

	elif url[1] == 'start':
		tag_list.append("창업지원단")
		if url[2] == 'notice':
			tag_list.append("공지")
		elif url[2] == 'free':
			tag_list.append("기타")

	elif url[1] == "dcinside":
		tag_list.append("디시인사이드")
		tag_list.append("기타")

	elif url[1] == "coop":
		tag_list.append("생협소식")
		tag_list.append("공지")

	elif url[1] == "sh":
		tag_list.append("산학협력단")
		tag_list.append("공지")

	if url[2] == "lecture":
		tag_list.append("강의평가")
		tag_list.append(title.split(" ")[0])
		

	###### 공용 부가 태그 ######
	tag_public(url, title, tag_list)

	return {"tag":list(set(tag_list))}

########################################################################

### 부경대 메인 홈페이지
def tag_main(url,title,tag_list):
	if url[2] == "notice":
		tag_list.append("공지")

		if title.find("식단표") != -1:
			tag_list.append("주간식단표")

	# 부경대 메인 자유게시판
	elif url[2] == "freeboard":
		tag_list.append("기타")

	# 부경대 메인 열린장터
	elif url[2] == "openmarket":
		tag_list.append("거래")

		# 부경대 메인 자취하숙
	elif url[2] == "boarding":
		tag_list.append("자취&하숙")

	# 부경대 메인 분실물센터
	elif url[2] == "lost":
		tag_list.append("분실물")

	# 부경대 메인 알바
	if url[2] == "parttimejob" or title.find("알바") != -1 \
	or title.find("아르바이트") != -1:
		tag_list.append("알바&구인")

	# 부경대 메인 봉사
	elif url[2] == "volunteer":
		tag_list.append("봉사")

	# 부경대 메인 동아리
	if url[2] == "circle" or title.find("스터디") != -1 \
	or title.find("공부") != -1 or title.find("모임") != -1:
		tag_list.append("스터디&모임")


### 부경대 인재개발원 (공모전 및 교육 제외)
def tag_job(url, title, tag_list):
	tag_list.append("취업")
	#부경대 인재 일반채용
	if url[2] == 'normal':
		tag_list.append("일반채용")
		if title.find("인크루트") != -1:
			tag_list.append("인크루트")
	#부경대 인재 추천채용
	elif url[2] == "recommend":
		tag_list.append("추천채용")
	#부경대 인재 해외취업
	elif url[2] == "overseas":
		tag_list.append("해외취업")

		if title.find("말레이시아") != -1 or\
		title.find("MALAYSIA") != -1:
			tag_list.append("말레이시아")

		if title.find("미국") != -1:
			tag_list.append("미국")

		if title.find("베트남") != -1:
			tag_list.append("베트남")

		if title.find("싱가폴") != -1:
			tag_list.append("싱가폴")

		if title.find("인도") != -1 and\
		title.find("인도네시아") == -1:
			tag_list.append("인도")

		if title.find("인도네시아") != -1:
			tag_list.append("인도네시아")

		if title.find("태국") != -1:
			tag_list.append("태국")

		if title.find("일본") != -1 \
		or title.find("후쿠오카") != -1\
		or title.find("나리타") != -1\
		or title.find("나고야") != -1:
			tag_list.append("일본")

	###### 취업 공용 태그 ######
	if title.find("연구") != -1:
		tag_list.append("연구직")

	if title.find("인턴") != -1:
		tag_list.append("인턴")

	if title.find("정규") != -1:
		tag_list.append("정규직")
				
	if title.find("계약직") != -1:
		tag_list.append("계약직")

	if title.find("공무") != -1:
		tag_list.append("공무직")

	if title.find("건축") != -1 or title.find("건설") != -1:
		tag_list.append("건축설계")

	if title.find("호텔") != -1:
		tag_list.append("호텔")

	if title.find("기획") != -1:
		tag_list.append("기획")

	if title.find("홍보") != -1:
		tag_list.append("홍보")



###### 공용 부가 태그 ######
def tag_public(url, title, tag_list):
	if title.find("토익") != -1 or title.find("토플") != -1\
	or title.find("TOEIC") != -1 or title.find("TOEFL") != -1\
	or title.find("영어회화") != -1 or title.find("영문학") != -1\
	or title.find("영어공부") != -1 or title.find("영어스터디") != -1:
		tag_list.append("영어")

	if title.find("HSK") != -1 or title.find("JPT") != -1\
	or title.find("JLPT") != -1\
	or (title.find("회화") != -1 and title.find("영어회화") == -1):
		tag_list.append("외국어")

	if title.find("취업") != -1 or title.find("인턴") != -1\
	or title.find("채용") != -1\
	or title.find("공채") != -1 or title.find("일자리") != -1\
	and (url[1] != 'job' or url[2] == 'competition')\
	or title.find("직원") != -1 or title.find("취업") != -1:
		tag_list.append("취업")

	if title.find("창업") != -1:
		tag_list.append("창업")

	if title.find("장학") != -1:
		tag_list.append("장학")

	if title.find("경영학") != -1:
		tag_list.append("경영학")

	if title.find("행사") != -1 or title.find("참가") != -1\
		or title.find("쇼") != -1 or title.find("프로그램") != -1\
		or title.find("대회") != -1\
		or (url[1] == 'job' and url[2] == 'competition')\
		or title.find("캠프") != -1 or title.find("축제") != -1\
		or title.find("박람회") != -1 or title.find("콘서트") != -1\
		or title.find("공모전") != -1:
		tag_list.append("행사")

	if title.find("공모") != -1 or title.find("대외활동") != -1:
		tag_list.append("공모전&대외활동")

	if title.find("특강") != -1:
		tag_list.append("특강")

	if title.find("수강") != -1 or title.find("K-MOOC") != -1\
	or title.find("강좌") != -1:
		tag_list.append("수강")

	if title.find("세미나") != -1:
		tag_list.append("세미나")

	if title.find("멘토") != -1 or title.find("멘티") != -1:
		tag_list.append("멘토링")

	if title.find("인문") != -1:
		tag_list.append("인문학")

	if title.find("모집") != -1:
		tag_list.append("모집")

	if title.find("스포츠") != -1 or title.find("레포츠") != -1\
	or title.find("축구") != -1 or title.find("운동") != -1\
	or title.find("농구") != -1 or title.find("야구") != -1\
	or title.find("족구") != -1  or title.find("수영") != -1\
	or title.find("테니스") != -1 or title.find("배드민턴") != -1:
		tag_list.append("스포츠")

	if title.find("조교") != -1 and title.find("보조교사") == -1:
		tag_list.append("조교")

	if title.find("디자인") != -1 and title.find("디자이너") != -1:
		tag_list.append("디자인")

	if title.find("봉사") != -1:
		tag_list.append("봉사")

	if title.find("진로") != -1 or title.find("인재") != -1\
	or title.find("직업") != -1:
		tag_list.append("진로")

	if title.find("이공계") != -1:
		tag_list.append("이공계")

	if title.find("동아리") != -1:
		tag_list.append("동아리")

	if title.find("과외") != -1 \
	or ((title.find("강사") != -1 or title.find("선생님") != -1)\
	and title.find("특강") == -1 and title.find("채용") == -1\
	and title.find("선발") == -1):
		tag_list.append("과외&강사")

	if (title.find("IT") != -1 and \
	alpha(title, title.find("IT")) == 2)\
	or title.find("더존비즈온") != -1\
	or title.find("그래픽") != -1\
	or title.find("개발자") != -1\
	or title.find("안드로이드") != -1\
	or title.find("소프트웨어") != -1\
	or title.find("KAKAO") != -1\
	or title.find("NHN") != -1\
	or title.find("인공지능") != -1\
	or (title.find("네이버") != -1 and title.find("네이버스") == -1)\
	or (title.find("SW") != -1 \
	and alpha(title, title.find("SW")) == 2)\
	or title.find("DATA") != -1\
	or title.find("알고리즘") != -1\
	or title.find("S/W") != -1\
	or (title.find("VR") != -1 \
	and alpha(title, title.find("VR")) == 2)\
	or title.find("프로그래머") != -1 :
		tag_list.append("IT&컴퓨터")

	if title.find("행긱") != -1 or title.find("행긱") != -1 or\
	title.find("기숙사") != -1 or title.find("긱사") != -1 or\
	title.find("행복기숙사") != -1 or title.find("세종관") != -1 or\
	title.find("세종1관") != -1 or title.find("세종2관") != -1 or\
	title.find("생활관") != -1:
		tag_list.append("기숙사")

	if title.find("원룸") != -1 or title.find("자취") != -1 or\
	title.find("자췻방") != -1 or title.find("하숙") != -1:
		tag_list.append("자취&하숙")

	if title.find("학식") != -1:
		tag_list.append("학식")

	if title.find("알바") != -1 \
	or title.find("아르바이트") != -1:
		tag_list.append("알바&구인")


#### 부경대 컴퓨터공학과 홈페이지
def tag_ce(url, title, tag_list):
	tag_list.append("컴퓨터공학과")
	tag_list.append("IT&컴퓨터")

	## 부경대 컴공 공지 
	if url[2] == "notice":
		tag_list.append("공지")

		if title.find("상담") != -1:
			tag_list.append("상담")

	## 부경대 컴공 채용정보
	if url[2] == 'jobinfo':
		tag_list.append("취업")

	## 부경대 컴공 삼성 SW 인력사업
	if url[2] == 'samsungsw':
		tag_list.append("삼성S/W")

		if title.find("SCSC"):
			tag_list.append("SCSC")

	## 부경대 컴공 대학원
	if url[2] == 'graduate':
		tag_list.append("대학원")

	# 컴퓨터 공학과 공통 태그
	if title.find("알고리즘") != -1:
		tag_list.append("알고리즘")

	if title.find("필독") != -1:
		tag_list.append("필독")

	if title.find("교육") != -1:
		tag_list.append("교육")


# 부경대 커뮤니티(pknu.in)
def tag_pknu(url, title, tag_list):
	tag_list.append("pknu.in")

	if url[2] == 'bamboo':
		tag_list.append("대나무숲")

	elif url[2] == 'moim':
		tag_list.append("스터디&모임")

	elif url[2] == 'public':
		tag_list.append("홍보")

	elif url[2] == 'lost':
		tag_list.append("분실물")

	elif url[2] == 'free':
		tag_list.append("기타")

	elif url[2] == 'twinkle':
		tag_list.append("반짝정원")

	elif url[2] == 'kin':
		tag_list.append("부경지식인")