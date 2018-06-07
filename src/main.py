"""	      PKU_Crawler		"""
"""	     	BY IML  		"""
"""	shin10256|gmail.com   	"""	
"""	shino1025.blog.me    	"""
"""	github.com/iml1111   	"""

import iml_global
from url_list import List
from crawl_select import Crawling

#for Debug
target = "PK_univ"
URL = List[0:4]   

if __name__ == '__main__':

	for url in URL:
		Crawling(target, url)
		