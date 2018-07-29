from url_parser import URLparser
from bs4 import BeautifulSoup
from db_manager import db_manage
from PK_global import PK_main_start
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