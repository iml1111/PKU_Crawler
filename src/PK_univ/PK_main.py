from url_parser import URLparser
from bs4 import BeautifulSoup
from db_manager import db_manage
from PK_global import PK_main_start
from tag import tagging
from post_wash import post_wash

start_datetime = PK_main_start
recent_date = None

def parsing(driver, URL, is_first):
	page = 1
	print("start_date:" + PK_main_start)
	while True:
		global recent_date #renwal date을 위한 갱신

		print('this page is\t| '+ URL['info'] + ' |\t' + str(page - 1))
		bs0bj = BeautifulSoup(driver.page_source, "html.parser")
		bs0bj = bs0bj.find("table",{"class":"bbs-list"})
		 # first 크롤링일 경우 그냥 진행
		if is_first == True:  
			db_docs = list_parse(bs0bj, URL)
		# renewal 모드일 경우. DB에서 가장 최신 게시물의 정보를 가져옴.
		else:
			latest_datetime = db_manage("get_recent", URL['info'])
			db_docs = list_parse(bs0bj, URL, latest_datetime)

		print('# this post of page is ' + str(len(db_docs)))

		# 맨 첫 번째 페이지를 파싱했고, 해당 페이지에서 글을 가져온 경우
		# 해당 글을 최신 날짜를 딕셔너리로 저장
		if page == 1 and len(db_docs) >= 1: 
			recent_date = {"name":URL['info'],"title":db_docs[0]['title']\
											,"recent_date":db_docs[0]['date']}

		#해당 페이지에서 글을 가져온 경우 db에 add
		if len(db_docs) == 0: 
			break
		else:
			db_manage("add", URL['info'], db_docs)
			page += 1
			driver.execute_script("goPage(" + str(page) + ")")

	#최신 날짜가 갱신되었다면 DB에 넣음
	if recent_date != None: 
		db_manage("renewal_date", URL['info'], recent_date, is_first = is_first)

	# global 변수으로 넣은 최신 날짜 정보 초기화
	recent_date = None

	if is_first == True:
		db_manage("view")


def list_parse(bs0bj, URL, latest_datetime = None):
	db_docs = []
	post_list = bs0bj.findAll("tr")
	domain = URL['url'].split('/')[0] + '//' + URL['url'].split('/')[2]

	# 게시글 파싱 및 크롤링
	for post in post_list:
		obj = post.find("td",{"class":"no"})
		if obj != None and obj.get_text() != "":
			db_record = {}
			
			obj = post.find("td",{"class":"title"})
			obj = obj.find("a").attrs['href']
			
			# 게시물 내에 정보 파싱
			db_record.update(content_parse(domain, domain + obj))

			obj = post.find("td",{"class":"author"})
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
				break

	return db_docs


def content_parse(domain, url):
	html = URLparser(url)
	bs0bj = BeautifulSoup(html.read(), "html.parser")
	db_record = {}
	db_record.update({"url":url})

	obj = bs0bj.find(text="제목")
	db_record.update({"title":obj.findNext('td').get_text().strip()})
	obj = bs0bj.find(text="작성일")
	db_record.update({"date":obj.findNext('td').get_text().strip()})

	obj = bs0bj.find("div",{'class':"bbs-body"})
	db_record.update({"post":post_wash(str(obj.get_text().strip()))})

	return db_record

		