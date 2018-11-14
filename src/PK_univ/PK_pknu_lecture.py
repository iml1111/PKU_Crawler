from url_parser import URLparser
from bs4 import BeautifulSoup
from db_manager import db_manage
from tag import tagging
from recent_date import get_today
from recent_date import get_recent_date

today = get_today()
recent_date = None

def parsing(driver, URL, is_first):
	page = 1
	while True:
		global recent_date #renwal date을 위한 갱신
		print('this page is\t| '+ URL['info'] + ' |\t' + str(page - 1))
		bs0bj = BeautifulSoup(driver.page_source, "html.parser")
		bs0bj = bs0bj.find("ul",{"class":"list-body"})

		# first 크롤링일 경우 or renewal 크롤링일 경우
		if is_first == True: 
			db_docs = list_parse(bs0bj, URL, page)
		else:
			latest_datetime = db_manage("get_recent", URL['info'])
			db_docs = list_parse(bs0bj, URL, page, latest_datetime)

		print('\n# this post of page is \n' + str(len(db_docs)))

		# 최근 날짜 갱신 
		if page == 1 and len(db_docs) >= 1:
			recent_date = get_recent_date(URL, db_docs)

		if len(db_docs) == 0:
			break
		else:
			db_manage("add", URL['info'], db_docs)
			page += 1
			driver.get(URL['url'] + "&page=" + str(page - 1))

	#최근 날짜가 갱신되었다면 db에도 갱신
	if recent_date != None: 
		db_manage("renewal_date", URL['info'], recent_date, is_first = is_first)
	recent_date = None


def list_parse(bs0bj, URL, page):
	db_docs = []
	post_list = bs0bj.findAll("li")
	domain = URL['url'].split('/')[0] + '//' + URL['url'].split('/')[2]

	#게시글 파싱 및 크롤링
	for post in post_list:
		db_record = {}

		title = ""
		obj = post.find("div",{"class":"wr-subject"})
		title = obj.find("span").find_next("span").get_text().strip()
		[s.extract() for s in obj('span')]
		title += " " + obj.find("a").get_text().strip()

		db_record.update({"url":obj.find("a").attrs["href"]})
		db_record.update({"title":title})
		db_record.update({"post":0})
		db_record.update({"date":today})
		db_record.update(tagging(URL, db_record['title']))

		print(db_record['title'])
		db_docs.append(db_record)

	return db_docs