from bs4 import BeautifulSoup
from url_parser import URLdriving, URLparser
# 부경대 공지사항 목록
import PK_main 
import PK_ce
import PK_pknu
import PK_today
import PK_pknu_lecture
import PK_pknulogin
import PK_dorm
import PK_start
import PK_dcinside
import PK_coop
import PK_sh
import PK_duem

filterlist = ['main','today']

def Crawling(target, URL, is_first):
	select = URL['info'].split('_')[1]

	if select in filterlist:
		try:
			driver = URLdriving(URL)
		except Exception as e:
			print("Connect Error")
			return
	else:
		try:
			driver = URLparser(URL['url'])
		except Exception as e:
			print("Connect Error")
			return	
		

	if target == 'PK_univ':
		print('-------------------------------------')
		print('Selected <' + URL['info'] +'>')
		print('-------------------------------------')
		
		if select == 'main':
			PK_main.parsing(driver, URL, is_first)
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
		elif select == 'coop':
			PK_coop.parsing(driver, URL, is_first)
		elif select == 'sh':
			PK_sh.parsing(driver, URL, is_first)
		elif select == 'duem' or select == 'korean' or select == 'japan'\
		or select == 'job':
			PK_duem.parsing(driver, URL, is_first)
