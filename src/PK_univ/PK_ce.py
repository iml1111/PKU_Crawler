from url_parser import URLparser
from url_parser import URLdriving
from bs4 import BeautifulSoup
from db_manager import db_manage

start_datetime = "2018-06-15"

def parsing(driver, URL):
	page = 1
	while True:
		print('this page is\t| '+ URL['info'] +' |\t' + str(page - 1))
		bs0bj = BeautifulSoup(driver.page_source, "html.parser")
		bs0bj = bs0bj.find("table",{"class":"tbl-type1"}).find("tbody")

		db_docs = list_parse(bs0bj, URL, page)
		print(len(db_docs))
			
		if len(db_docs) == 0:
			break
		else:
			db_manage("add", URL['info'], db_docs)
			page += 1
			driver.get(URL['url'] + "?page=" + str(page - 1))

	db_manage("view")


def list_parse(bs0bj, URL, page):
	db_docs = []
	post_list = bs0bj.findAll("tr")
	domain = URL['url'].split('/')[0] + '//' + URL['url'].split('/')[2]

	for post in post_list:
		if  page > 1 and post.find("td",{"class":"first"}).get_text() == "공지":
			continue
		db_record = {}

		obj = post.find("td",{"class":"txt-l"}).find("a")
		db_record.update(content_parse(domain, domain + obj.attrs["href"]))

		print(db_record['date'])
		if db_record['date'] >= start_datetime or \
											post.find("td",{"class":"first"}).get_text() == "공지":
			db_docs.append(db_record)
		else:
			break

	return db_docs

def content_parse(domain, url):
	html = URLparser(url)
	bs0bj = BeautifulSoup(html.read(), "html.parser")
	bs0bj =bs0bj.find("table").find("tbody")
	db_record = {}
	db_record.update({"url":url})

	obj = bs0bj.find("tr",{"class":"head"}).find("td",{"class":"first txt-l"})
	db_record.update({"title": obj.get_text().strip()})
	obj = obj.find_next("td")
	db_record.update({"author": obj.get_text().strip()})
	obj = obj.find_next("td")
	db_record.update({"date": obj.get_text().strip()})

	obj =bs0bj.find("tr",{"class":"head"}).find_next("tr")
	db_record.update({"post": str(obj)})

	# 자바스크립트 첨부파일 파싱 불가

	return db_record
