from bs4 import BeautifulSoup
import PK_main

def Crawling(html,url_info):

	bs0bj = BeautifulSoup(html.read(), "html.parser")

	if url_info == 'PK_main_notice':
		PK_main.parsing(bs0bj)