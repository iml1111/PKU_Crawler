from url_parser import URLparser
from url_parser import URLdriving
from bs4 import BeautifulSoup
from db_manager import db_manage
from PK_global import PK_job_start

start_datetime = PK_job_start
recent_date = None

def parsing(driver, URL, is_first):
	page = 1
	while True:
		global recent_date #renwal date을 위한 갱신

		print('this page is\t| '+ URL['info'] +' |\t' + str(page - 1))
		bs0bj = BeautifulSoup(driver.page_source, "html.parser")
		bs0bj = bs0bj.find("ul",{"id":"board_list"})

		if is_first == True:    # first 크롤링일 경우 or renewal 크롤링일 경우
			db_docs = list_parse(bs0bj, URL)
		else:
			latest_datetime = db_manage("get_recent", URL['info'])
			db_docs = list_parse(bs0bj, URL, latest_datetime)

		print('# this post of page is ' + str(len(db_docs)))

		if page == 1 and len(db_docs) >= 1: # 최근 날짜 갱신 
			recent_date = {"name":URL['info'],"title":db_docs[0]['title']\
											,"recent_date":db_docs[0]['date']}
	
		if len(db_docs) == 0:
			break
		else:
			db_manage("add", URL['info'], db_docs)
			page += 1
			driver.get(URL['url'] + "&pageIndex=" + str(page))

	if recent_date != None: #최근 날짜가 갱신되었다면 db에도 갱신
		db_manage("renewal_date", URL['info'], recent_date, is_first = is_first)
	recent_date = None

	if is_first == True:
		db_manage("view")


def list_parse(bs0bj, URL, latest_datetime = None):
	db_docs = []
	post_list = bs0bj.findAll("li")
	domain = URL['url'].split('/')[0] + '//' + URL['url'].split('/')[2]

	for post in post_list:
		if post.find('span').find('img') is not None:
			continue
			
		obj = post.find("a")
		db_record = {}
		db_record.update(content_parse(domain, domain + obj.attrs["href"]))
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


def content_parse(domain,url):
	html = URLparser(url)
	bs0bj = BeautifulSoup(html.read(), "html.parser")
	bs0bj =bs0bj.find("div",{"id":"board_view"})
	db_record = {}
	db_record.update({"url":url})

	obj = bs0bj.find("h3")
	db_record.update({"title":obj.get_text().strip()})
	obj = obj.find_next("p")
	db_record.update({"date":obj.find("strong").get_text().strip()})
	obj = obj.find_next("p")
	db_record.update({"author":obj.find("strong").get_text().strip()})
	obj = bs0bj.find("div",{"class":"board_stance"})
	db_record.update({"post":str(obj)})
	'''
	cnt = 1
	while obj.find_next("p") is not None:
		obj = obj.find_next("p")
		db_record.update({"file_link_" + str(cnt) :\
							# jsscript;;; href 링크가 없음 
						 obj.find("a")}).attrs['href']
		cnt += 1
	'''
	return db_record