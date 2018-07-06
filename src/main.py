"""	      U&I_Crawler		"""
"""	     	BY IML  		"""
"""	shin10256|gmail.com   	"""	
"""	shino1025.blog.me    	"""
"""	github.com/iml1111   	"""
#1. 시간 조건 전역변수 파일로 옮기기
#2. 주석달기 및 영어 번역
import iml_global
from url_list import List
from crawl_select import Crawling
import time

#for Debug
target = "PK_univ"
URL = List[0:1] 

if __name__ == '__main__':
	print("HI! I'M IML.")
	print('First Crawling Start!')
	print('target: ' + target)
	
	for url in URL:
		print('< URL parsing Start! >\n' + str(url['url']))
		time.sleep(.6)
		Crawling(target, url, True)
		print('-------------------------------------')

	while(True):
		print('\n\nRenewal Crawling Start...\n\n')
		for url in URL:
			print('< URL parsing Renewal >\n' + str(url['url']))
			time.sleep(.6)
			Crawling(target, url, False)
			print('-------------------------------------')
		