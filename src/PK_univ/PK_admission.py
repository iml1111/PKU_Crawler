from url_parser import URLparser
from url_parser import URLdriving
from bs4 import BeautifulSoup
from db_manager import db_manage

start_datetime = "2018.02.22 00:00:00"

def parsing(driver, URL):
	page = 1
	while True:
		print('this page is\t| '+ URL['info'] +' |\t' + str(page - 1))
		bs0bj = BeautifulSoup(driver.page_source, "html.parser")
		bs0bj = bs0bj.find("div",{"class":"tableArea"}).find("tbody")

		db_docs = list_parse(bs0bj, URL)
		print(len(db_docs))
			
		if len(db_docs) == 0:
			break
		else:
			db_manage("add", URL['info'], db_docs)
			page += 1
			driver.get(URL['url'] + "&page=" + str(page))

	db_manage("view")


def list_parse(bs0bj, URL):
	db_docs = []
	post_list = bs0bj.findAll("tr")
	domain = URL['url'].split('?')[0]

	for post in post_list:
		obj = post.find("td")
		if obj.get_text().strip() == "공지": continue
		db_record = {}

		obj = obj.find_next("td")
		db_record.update({"class":obj.get_text().strip()})
		obj = obj.find_next("td",{"class":"al"})
		db_record.update({"title":obj.get_text().strip()})

		bj = obj.find("a").find_next("a").attrs['href']
		db_record.update(content_parse(domain, domain + bj))

		print(db_record['date'])
		if db_record['date'] >= start_datetime:
			db_docs.append(db_record)
		else:
			break

	return db_docs


def content_parse(domain, url):
	html = URLparser(url)
	bs0bj = BeautifulSoup(html.read(), "html.parser")
	bs0bj =bs0bj.find("div",{"class":"tableArea"}).find("table",{"class":"viewTable"})
	db_record = {}
	db_record.update({"url":url})

	obj = bs0bj.find("thead").find("tr")
	obj = bs0bj.find_next("tr")
	bj = obj.find("td").find_next("td")
	db_record.update({"author":bj.get_text().strip()})

	bj = bj.find_next("td")
	db_record.update({"date":bj.get_text().strip()})

	obj = obj.find_next("tr").find_next("tr").find("td")
	if obj.get_text().strip() == "":
		db_record.update({"file_is":0})
	else:
		db_record.update({"file_is":1})
		db_record.update({"file_link":domain + obj.find("a").attrs['href'].strip()})

	obj = bs0bj.find("tbody").find("tr")
	db_record.update({"post":str(obj)})

	return db_record



		
