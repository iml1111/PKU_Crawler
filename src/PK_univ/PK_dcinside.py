from url_parser import URLparser
from bs4 import BeautifulSoup
from db_manager import db_manage
from PK_global import PK_dcinside_start
from tag import tagging
from post_wash import post_wash
import time

start_datetime = PK_dcinside_start
recent_date = None

def parsing(driver, URL, is_first):
	page = 1
	print("start_date:" + start_datetime)
	while True:
		global recent_date

		print('this page is\t| '+ URL['info'] + ' |\t' + str(page - 1))
		bs0bj = BeautifulSoup(driver.page_source, "html.parser")
		bs0bj = bs0bj.find("tbody",{"class":"list_tbody"})

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
			driver.get(URL['url'] + "&page=" + str(page - 1))
			time.sleep(3)
			print(URL['url'] + "&page=" + str(page - 1))

	# 최근 날짜가 갱신되었다면 db에도 갱신
	if recent_date != None:
		db_manage("renewal_date", URL['info'], recent_date, is_first = is_first)
	recent_date = None

	if is_first == True:
		db_manage("view")


def list_parse(bs0bj, URL, page, latest_datetime = None):
	db_docs = []
	post_list = bs0bj.findAll("tr")
	domain = URL['url'].split('/')[0] + '//' + URL['url'].split('/')[2]

	for post in post_list[1:]:
		db_record = {}
		
		obj = post.find("a").attrs['href']
		db_record.update(content_parse(domain + obj))
		# 태그 생성
		db_record.update(tagging(URL, db_record['title']))

		print(db_record['date'])
		# first 파싱이고 해당 글의 시간 조건이 맞을 때
		if ( db_record['date'] >= start_datetime or  \
				post.find("td",{"class":"t_notice"}).get_text() == "공지" ) and \
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


def content_parse(url):
	html = URLparser(url)
	time.sleep(1)
	bs0bj = BeautifulSoup(html.read(), "html.parser")
	db_record = {}
	db_record.update({"url":url})

	obj = bs0bj.find("dl",{"class":"wt_subject"}).find("dd").get_text().strip()
	db_record.update({"title":obj})

	obj = bs0bj.find("div",{"class":"w_top_right"}).find("li")
	obj = obj.get_text().strip()
	db_record.update({"date":obj})

	obj = bs0bj.find("div",{"class":"s_write"})
	obj = obj.get_text().strip()
	db_record.update({"post":post_wash(obj)})

	return db_record