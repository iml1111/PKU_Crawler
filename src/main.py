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
URL = List[0]   

if __name__ == '__main__':
	Crawling(target, URL)
		