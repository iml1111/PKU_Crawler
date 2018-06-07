from url_parser import URLparser
from bs4 import BeautifulSoup
from db_manager import db_manage

PK_domain = "http://www.pknu.ac.kr"

def parsing(bs0bj, name):
	bs0bj = bs0bj.find("table",{"class":"bbs-list"})
	summary = bs0bj.attrs['summary']
	
	db_docs = list_parse(bs0bj)
	db_manage("add", name, db_docs)
	db_manage("view", name)
	print(summary)

def list_parse(bs0bj):
	count = 1
	db_docs = []

	post_list = bs0bj.findAll("tr")
	post_list.reverse()

	for post in post_list:
		obj = post.find("td",{"class":"no"})
		if obj != None and obj.get_text() != "":
			db_record = {}
			db_record.update({"no":str(count)})
			count += 1
			obj = post.find("td",{"class":"title"})
			db_record.update({"title":obj.get_text().strip()})
			obj = obj.find("a").attrs['href']
			db_record.update(content_parse(PK_domain + obj))
			obj = post.find("td",{"class":"author"})
			db_record.update({"author":obj.get_text().strip()})
			obj = post.find("td",{"class":"date"})
			db_record.update({"date":obj.get_text().strip()})
			obj = post.find("td",{"class":"count"})
			db_record.update({"count":int(obj.get_text().strip())})

			db_docs.append(db_record)

	return db_docs

def content_parse(url):
	html = URLparser(url)
	bs0bj = BeautifulSoup(html.read(), "html.parser")
	db_record = {}
	
	obj = bs0bj.find(text ="이메일")
	db_record.update({"email":obj.findNext('td').get_text().strip()})
	obj = bs0bj.find("img",{'alt':"첨부 파일"})
	if not obj:
		db_record.update({"file_is":0})
		db_record.update({"file_link":"None"})
	else:
		db_record.update({"file_is":1})
		db_record.update({"file_link":(PK_domain \
			+ obj.findNext('a').attrs['href']).strip()})
	obj = bs0bj.find("div",{'class':"bbs-body"})
	db_record.update({"post":str(obj)})

	return db_record



	
