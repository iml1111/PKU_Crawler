from url_parser import URLparser
from bs4 import BeautifulSoup
from db_manager import db_manage
from PK_global import PK_start_start
from tag import tagging
from post_wash import post_wash

start_datetime = PK_start_start
recent_date = None

def parsing(driver, URL, is_first):
	page = 1
	print("start_date:" + start_datetime)
	while True:
		global recent_date

		print('this page is\t| '+ URL['info'] + ' |\t' + str(page - 1))
		bs0bj = BeautifulSoup(driver.page_source, "html.parser")
		bs0bj = bs0bj.find("table",{"class":"list_tbl tbl_w_type_2"}).find("tbody")

		# first 크롤링일 경우 그냥 진행
		if is_first == True:
			db_docs = list_parse(driver, bs0bj, URL, page)

		# renewal 모드일 경우. DB에서 가장 최신 게시물의 정보를 가져옴.
		else:
			lastet_datetime = db_manage("get_recent", URL['info'])
			db_docs = list_parse(driver, bs0bj, URL, page, lastet_datetime)

		print('\n# this post of page is \n' + str(len(db_docs)))

		# 맨 첫 번째 페이지를 파싱했고, 해당 페이지에서 글을 가져온 경우
		# 해당 글을 최신 날짜를 딕셔너리로 저장
		if page == 1 and len(db_docs) >= 1:
			recent_doc = db_docs[0]
			for doc in db_docs[1:]:
				if(recent_doc['date'] <= doc['date']):
					recent_doc = doc
			recent_date = {"name":URL['info'], "title":recent_doc['title']\
							, "recent_date":recent_doc['date']}

		if len(db_docs) == 0:
			break
		else:
			db_manage("add", URL['info'], db_docs)
			page += 1
			driver.get(URL['url'] + "?page_no=" + str(page - 1))
			print(URL['url'] + "?page_no=" + str(page - 1))

	# 최근 날짜가 갱신되었다면 db에도 갱신
	if recent_date != None:
		db_manage("renewal_date", URL['info'], recent_date, is_first = is_first)
	recent_date = None

	if is_first == True:
		db_manage("view")


def list_parse(driver, bs0bj, URL, page, latest_datetime = None):
	db_docs = []
	post_list = bs0bj.findAll("tr")
	domain = URL['url'].split('/')[0] + '//' + URL['url'].split('/')[2]

	for post in post_list:
		db_record = {}

		obj = post.find("a").attrs['href']
		if URL['info'] == 'PK_start_notice':
			url = "http://startup.pknu.ac.kr/html2015/06comm/01_view.do?idx=" + obj.split("#")[1]
		elif URL['info'] == 'PK_start_free':
			url = "http://startup.pknu.ac.kr/html2015/06comm/06_view.do?idx=" + obj.split("#")[1]
		db_record.update(content_parse(url))
		
		# 태그 생성
		db_record.update(tagging(URL, db_record['title']))

		print(db_record['date'])
		# first 파싱이고 해당 글의 시간 조건이 맞을 때
		if db_record['date'] >= start_datetime and \
								latest_datetime == None:
			db_docs.append(db_record)
		#renewal 파싱이고 해당 글의 갱신 조건이 맞을 때
		elif latest_datetime != None and \
				db_record['date'] >= latest_datetime['recent_date'] and \
					db_record['title'] != latest_datetime['title']:
			db_docs.append(db_record)		
		else:
			continue

	return db_docs


def content_parse(url):
	html = URLparser(url)
	bs0bj = BeautifulSoup(html.read(), "html.parser")
	db_record = {}
	db_record.update({"url":url})

	obj = bs0bj.find("span",{"class":"view_subj_core"})
	obj = obj.get_text().strip()
	db_record.update({"title":obj})

	obj = bs0bj.find("span",{"class":"view_subj_date"})
	obj = obj.get_text().strip()
	db_record.update({"date":obj})

	obj = bs0bj.find("div",{"class":"view_txt_container"})
	obj = obj.get_text().strip()
	db_record.update({"post":post_wash(str(obj))})
	
	return db_record