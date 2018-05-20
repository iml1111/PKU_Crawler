from bs4 import BeautifulSoup
from url_parser import URLparser
import PK_main

def PK_crawling(bs0bj, url_info):

	if url_info == 'PK_main_notice':
		PK_main.parsing(bs0bj)

def Crawling(target,URL):

	html = URLparser(URL['url'])
	bs0bj = BeautifulSoup(html.read(), "html.parser")

	if target == 'PK_univ':
		PK_crawling(bs0bj, URL['info'])

	
	