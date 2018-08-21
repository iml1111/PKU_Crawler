from bs4 import BeautifulSoup
from url_parser import URLdriving, URLparser
# 부경대 공지사항 목록
import PK_main 
import PK_job
import PK_ce
import PK_pknu
import PK_today
import PK_pknu_lecture
import PK_pknulogin
import PK_dorm
import PK_start
import PK_dcinside

def Crawling(target, URL, is_first):
	select = URL['info'].split('_')[1]

	if  select == 'dcinside':
		driver = URLparser(URL['url'])
	else:
		driver = URLdriving(URL)

	if target == 'PK_univ':
		print('-------------------------------------')
		print('Selected <' + select +'>')
		print('-------------------------------------')
		
		if select == 'main':
			PK_main.parsing(driver, URL, is_first)
		elif select == 'job':
			PK_job.parsing(driver, URL, is_first)
		elif select == 'ce':
			PK_ce.parsing(driver, URL, is_first)
		elif select == 'pknu':
			PK_pknu.parsing(driver, URL, is_first)
		elif select == 'today':
			PK_today.parsing(driver, URL, is_first)
		elif select == 'pknulec' and is_first == True:
			PK_pknu_lecture.parsing(driver, URL, is_first)
		elif select == 'pknulogin':
			PK_pknulogin.parsing(driver, URL, is_first)
		elif select == 'dorm':
			PK_dorm.parsing(driver, URL, is_first)
		elif select == 'start':
			PK_start.parsing(driver, URL, is_first)
		elif select == 'dcinside':
			PK_dcinside.parsing(driver, URL, is_first)
