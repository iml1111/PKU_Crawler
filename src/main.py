"""	      PKU_Crawler		"""
"""	     	BY IML  		"""
"""	shin10256|gmail.com   	"""	
"""	shino1025.blog.me    	"""
"""	github.com/iml1111   	"""

import iml_global
from url_list import List
from crawl_select import Crawling
import time

#for Debug
target = "PK_univ"
URL = List[:]   

if __name__ == '__main__':
	print("HI! I'M IML.")
	print('Crawling Start!')
	time.sleep(.7)
	
	for url in URL:
		print('target: ' + target)
		time.sleep(.6)
		print('< URL parsing Start! >\n' + str(url['url']))
		time.sleep(.6)
		Crawling(target, url)
		print('-------------------------------------')

	print('Thank you!')
		