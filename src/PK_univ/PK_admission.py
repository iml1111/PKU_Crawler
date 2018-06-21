from url_parser import URLparser
from bs4 import BeautifulSoup
from db_manager import db_manage

start_datetime = "2018-06-21 00:00"

def parsing(driver, URL):
	page = 1
	while True:
		print('this page is\t| '+ URL['info'] +' |\t' + str(page - 1))
		bs0bj = BeautifulSoup(driver.page_source, "html.parser")
		bs0bj = bs0bj.find("div",{"class":"tableArea"})
		bs0bj = bs0bj.find("table")	
		db_docs = list_parse(bs0bj, URL)
		print(len(db_docs))
			
		if len(db_docs) == 0:
			break
		else:
			db_manage("add", URL['info'], db_docs)
			page += 1
			driver.execute_script("goPage(" + str(page) + ")")

	db_manage("view")