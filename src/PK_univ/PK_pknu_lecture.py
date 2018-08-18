from url_parser import URLparser
from bs4 import BeautifulSoup
from db_manager import db_manage
from tag import tagging

def parsing(driver, URL, is_first):
	page = 1
	while True:
		print('this page is\t| '+ URL['info'] + ' |\t' + str(page - 1))
		bs0bj = BeautifulSoup(driver.page_source, "html.parser")
		bs0bj = bs0bj.find("ul",{"class":"list-body"})

		# renewal 크롤링 없음
		db_docs = list_parse(bs0bj, URL, page)
		print('\n# this post of page is \n' + str(len(db_docs)))
		if len(db_docs) == 0:
			break
		else:
			db_manage("add", URL['info'], db_docs)
			page += 1
			driver.get(URL['url'] + "&page=" + str(page - 1))
			print(URL['url'] + "&page=" + str(page - 1))

	db_manage("view")


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
		db_record.update({"post":"해당 페이지에 로그인 후 확인하실 수 있습니다."})
		db_record.update(tagging(URL, db_record['title']))

		print(db_record['title'])
		db_docs.append(db_record)

	return db_docs