from url_parser import URLparser
from bs4 import BeautifulSoup
from db_manager import db_manage
from PK_global import PK_pknu_start
from tag import tagging

start_datetime = PK_pknu_start
recent_date = None

def parsing(driver, URL, is_first):
	page = 1
	print("start_date:" + PK_pknu_start)
	while True:
		global recent_date # renewal date를 위한 갱신

		print('this page is\t| '+ URL['info'] + ' |\t' + str(page - 1))
		bs0bj = BeautifulSoup(driver.page_source, "html.parser")
		bs0bj = bs0bj.find("ul",{"class":"list-body"})

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
			print(URL['url'] + "&page=" + str(page - 1))
	# 최근 날짜가 갱신되었다면 db에도 갱신
	if recent_date != None:
		db_manage("renewal_date", URL['info'], recent_date, is_first = is_first)
	recent_date = None

	if is_first == True:
		db_manage("view")


def list_parse(bs0bj, URL, page, lastet_datetime = None):
	db_docs = []
	post_list = bs0bj.findAll("li")
	domain = URL['url'].split('/')[0] + '//' + URL['url'].split('/')[2]

	#게시글 파싱 및 크롤링
	for post in post_list:
		# 1 페이지에만 나타나는 공지글 스킵
		if post.find("span",{"class":"wr-icon wr-notice"}) != None:
			continue
		db_record = {}

		obj = post.find("div",{"class":"wr-subject"}).find("a")
		db_record.update(content_parse(domain, obj.attrs["href"]))

		# 태그 생성
		if "class" in db_record.keys():
			db_record.update(tagging(URL, db_record['title'] + db_record['class']))
		else:
			db_record.update(tagging(URL, db_record['title']))

		print(db_record['date'])
		# first 파싱이고 해당 글의 시간 조건이 맞을 때
		if db_record['date'] >= start_datetime and \
							lastet_datetime == None:
			db_docs.append(db_record)
		#renewal 파싱이고 해당 글의 갱신 조건이 맞을 때
		elif lastet_datetime != None and\
				db_record['date'] >= lastet_datetime['recent_date'] and \
						db_record['title'] != lastet_datetime['title']:
			db_docs.append(db_record)
		else:
			break

	return db_docs

def content_parse(domain, url):
	html = URLparser(url)
	bs0bj = BeautifulSoup(html.read(), "html.parser")
	bs0bj = bs0bj.find("div",{"class":"view-wrap"})\
					.find("article",{"itemprop":"articleBody"})

	db_record = {}
	db_record.update({"url":url})

	obj = bs0bj.find("h1",{"itemprop":"headline"})
	db_record.update({"title": obj.get_text().strip()})

	if bs0bj.find("span",{"class":"hidden-xs"}) != None:
		obj = bs0bj.find("span",{"class":"hidden-xs"})
		if obj.get_text().strip() != "":
			db_record.update({"class":obj.get_text().strip()})

	obj = bs0bj.find("span",{"itemprop":"datePublished"})
	db_record.update({"date": obj.attrs["content"]})
	obj = bs0bj.find("div",{"itemprop":"description"})
	db_record.update({"post": post_wash(str(obj.get_text().strip()))})

	return db_record

def post_wash(text):
	data = ""
	for i in range(len(text)):
		if text[i] == '\n' or text[i] == '\r':
			continue
		if text[i] == '\\' and (text[i+1] == 'n' or text[i+1] == 'r'):
			continue
		elif (text[i] == 'n' or text[i] == 'r') or text[i-1] == '\\':
			continue
		data = data + text[i]

	return data