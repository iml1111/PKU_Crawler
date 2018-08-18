from url_parser import URLparser
from bs4 import BeautifulSoup
from db_manager import db_manage
from PK_global import PK_dorm_start
from tag import tagging
from post_wash import post_wash
import datetime

start_datetime = PK_dorm_start
recent_date = None
dt = datetime.datetime.now()
today = str(dt.year) + "-" + str(dt.month) + "-" + str(dt.day)

def parsing(driver, URL, is_first):
	page = 0
	print("start_date:" + PK_dorm_start)
	while True:
		global recent_date # renewal date를 위한 갱신

		print('this page is\t| '+ URL['info'] + ' |\t' + str(page - 1))
		bs0bj = BeautifulSoup(driver.page_source, "html.parser")
		bs0bj = bs0bj.find("table",{"class":"board_list"}).find("tbody")

		# first 크롤링일 경우 그냥 진행
		if is_first == True:
			db_docs = list_parse(bs0bj, URL, page)
			
		# renewal 모드일 경우. DB에서 가장 최신 게시물의 정보를 가져옴.
		else:
			lastet_datetime = db_manage("get_recent", URL['info'])
			db_docs = list_parse(bs0bj, URL, page, lastet_datetime)

		print('\n# this post of page is \n' + str(len(db_docs)))

		# 맨 첫 번째 페이지를 파싱했고, 해당 페이지에서 글을 가져온 경우
		# 해당 글을 최신 날짜를 딕셔너리로 저장
		if page == 1 and len(db_docs) >= 1:
			recent_date = {"name":URL['info'], "title":db_docs[0]['title']\
							, "recent_date":db_docs[0]['date']}

		if len(db_docs) == 0:
			break
		else:
			db_manage("add", URL['info'], db_docs)
			page += 1
			driver.get(URL['url'] + "?page=" + str(page - 1))
			print(URL['url'] + "?page=" + str(page - 1))
			
	# 최근 날짜가 갱신되었다면 db에도 갱신
	if recent_date != None:
		db_manage("renewal_date", URL['info'], recent_date, is_first = is_first)
	recent_date = None

	# 오늘의 식단표 url 추가
	obj = {"url":"http://dormitory.pknu.ac.kr/03_notice/notice01.php",\
	"title":"오늘의 식단",\
	"post":"식사는 카드인식 후 가능하며, 자율배식으로 합니다.\
	식사예절 준수, 용모, 복장을 단정히 하고 건강을 위해 끼니를 거르지 않고\
	규칙적으로 식사하도록 합시다.",\
	"date":today}
	db_manage("add", URL['info'], [obj])

	if is_first == True:
		db_manage("view")

def list_parse(bs0bj, URL, page, latest_datetime = None):
	db_docs = []
	post_list = bs0bj.findAll("tr")
	domain = URL['url'].split('/')[0] + '//' + URL['url'].split('/')[2]

	#게시글 파싱 및 크롤링
	for post in post_list:
		# 1 페이지에서만 필수 공지글을 가져오고 그다음부턴 스킵
		if page > 0 and post.find("td").get_text().strip() == "":
			continue

		db_record = {}
		db_record.update(content_parse(domain, domain \
							+ post.find("a").attrs["href"]))
		# 태그 생성
		db_record.update(tagging(URL, db_record['title']))

		print(db_record['date'])
		# first 파싱이고 해당 글의 시간 조건이 맞을 때
		if (db_record['date'] >= start_datetime or \
					post.find("td").get_text().strip() == "")\
											and \
											latest_datetime == None:
			db_docs.append(db_record)
		#renewal 파싱이고 해당 글의 갱신 조건이 맞을 때
		elif latest_datetime != None and \
				db_record['date'] >= latest_datetime['recent_date'] and \
					db_record['title'] != latest_datetime['title']:
			db_docs.append(db_record)
		else:
			break

	return db_docs


def content_parse(domain, url):
	html = URLparser(url)
	bs0bj = BeautifulSoup(html.read(), "html.parser")
	db_record = {}
	db_record.update({"url":url})

	bs0bj = bs0bj.find("table",{"class":"board_view"})
	obj = bs0bj.find("thead").get_text().strip()
	db_record.update({"title":obj})

	obj = bs0bj.find("tbody").find("tr").find("td").find_next("td").find_next("td")
	obj = obj.get_text().strip().split(" ")[2]
	db_record.update({"date":obj})

	obj = bs0bj.find("tbody").find("td",{"class":"tdc"})
	obj = obj.get_text().strip()
	db_record.update({"post":post_wash(str(obj))})

	return db_record
