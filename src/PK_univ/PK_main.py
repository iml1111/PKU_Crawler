from url_parser import URLparser
from bs4 import BeautifulSoup
from db_manager import db_manage

start_datetime = "2018-06-21 00:00"

def parsing(driver, URL):
	page = 1
	while True:
		print('this page is\t| '+ URL['info'] + ' |\t' + str(page - 1))
		bs0bj = BeautifulSoup(driver.page_source, "html.parser")
		bs0bj = bs0bj.find("table",{"class":"bbs-list"})	
		db_docs = list_parse(bs0bj, URL)
		print('# this post of page is ' + str(len(db_docs)))
			
		if len(db_docs) == 0:
			break
		else:
			db_manage("add", URL['info'], db_docs)
			page += 1
			driver.execute_script("goPage(" + str(page) + ")")

	db_manage("view")


def list_parse(bs0bj, URL):
	db_docs = []
	post_list = bs0bj.findAll("tr")
	domain = URL['url'].split('/')[0] + '//' + URL['url'].split('/')[2]

	for post in post_list:
		obj = post.find("td",{"class":"no"})
		if obj != None and obj.get_text() != "":
			db_record = {}
			obj = post.find("td",{"class":"title"})
			db_record.update({"title":obj.get_text().strip()})
			obj = obj.find("a").attrs['href']
			db_record.update(content_parse(domain, domain + obj))
			obj = post.find("td",{"class":"author"})
			db_record.update({"author":obj.get_text().strip()})
			obj = post.find("td",{"class":"count"})
			db_record.update({"count":int(obj.get_text().strip())})

			print(db_record['date'])
			if db_record['date'] >= start_datetime:
				db_docs.append(db_record)
			else:
				break

	return db_docs


def content_parse(domain, url):
	html = URLparser(url)
	bs0bj = BeautifulSoup(html.read(), "html.parser")
	db_record = {}

	obj = bs0bj.find(text="작성일")
	db_record.update({"date":obj.findNext('td').get_text().strip()})
	obj = bs0bj.find(text ="이메일")
	if obj != None:
		db_record.update({"email":obj.findNext('td').get_text().strip()})
	obj = bs0bj.find("img",{'alt':"첨부 파일"})
	if not obj:
		db_record.update({"file_is":0})
		db_record.update({"file_link":"None"})
	else:
		db_record.update({"file_is":1})
		db_record.update({"file_link":(domain \
			+ obj.findNext('a').attrs['href']).strip()})
	obj = bs0bj.find("div",{'class':"bbs-body"})
	db_record.update({"post":str(obj)})

	return db_record



	
