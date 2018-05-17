"""	        PKU_Crwaler	"""
"""	     	  BY IML  	"""
"""	shin10256|gmail.com   	"""	
"""	shino1025.blog.me    	"""
"""	github.com/iml1111   	"""
from url_list import List
from crawl_select import Crawling
from url_parser import URLparser

URL = List[0]  #for Debug 

if __name__ == '__main__':
	
	html = URLparser(URL['url'])
	Crawling(html, URL['info'])
		