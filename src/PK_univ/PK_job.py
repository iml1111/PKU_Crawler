from url_parser import URLparser
from url_parser import URLdriving
from bs4 import BeautifulSoup
from db_manager import db_manage

start_datetime = "2018-02-22"

def parsing(driver, URL):
	page = 1
	while True:
		print('this page is\t| '+ URL['info'] +' |\t' + str(page - 1))
		bs0bj = BeautifulSoup(driver.page_source, "html.parser")
		bs0bj = bs0bj.find("ul",{"id":"board_list"})

		db_docs = list_parse(bs0bj, URL)
		print(len(db_docs))
			
		if len(db_docs) == 0:
			break
		else:
			db_manage("add", URL['info'], db_docs)
			page += 1
			driver.get(URL['url'] + "&pageIndex=" + str(page))

	db_manage("view")


def list_parse(bs0bj, URL):
	db_docs = []
	post_list = bs0bj.findAll("li")
	domain = URL['url'].split('?')[0]

	for post in post_list:
		obj = post.find("a")
		db_record = {}

		db_record.update(content_parse(domain, domain + obj.attrs["href"]))

		print(db_record['date'])
		if db_record['date'] >= start_datetime:
			db_docs.append(db_record)
		else:
			break

	return db_docs


def content_parse(domain,url):
	html = URLparser(url)
	bs0bj = BeautifulSoup(html.read(), "html.parser")
	bs0bj =bs0bj.find("div",{"id":"board_view"})

	obj = bs0bj.find("h3")
	print(obj.get_text().strip())