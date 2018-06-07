from bs4 import BeautifulSoup
from url_parser import URLparser
import PK_main

def Crawling(target,URL):

	html = URLparser(URL['url'])
	bs0bj = BeautifulSoup(html.read(), "html.parser")

	if target == 'PK_univ':
		PK_main.parsing(bs0bj, URL['info'])

	
	