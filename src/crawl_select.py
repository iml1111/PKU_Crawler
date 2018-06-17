from bs4 import BeautifulSoup
from url_parser import URLdriving
import PK_main

def Crawling(target,URL):
	driver = URLdriving(URL)

	if target == 'PK_univ':
		PK_main.parsing(driver, URL)

	
	