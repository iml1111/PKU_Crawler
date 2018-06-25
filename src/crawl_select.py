from bs4 import BeautifulSoup
from url_parser import URLdriving
# 부경대 공지사항 목록
import PK_main
import PK_admission
import PK_job
import PK_ce

def Crawling(target,URL):
	select = URL['info'].split('_')[1]
	driver = URLdriving(URL)

	if target == 'PK_univ':
		print('Selected <' + select +'>')
		print('-------------------------------------')
		
		if select == 'main':
			PK_main.parsing(driver, URL)
		elif select == 'admission':
			PK_admission.parsing(driver, URL)
		elif select == 'job':
			PK_job.parsing(driver, URL)
		elif select == 'ce':
			PK_ce.parsing(driver, URL)