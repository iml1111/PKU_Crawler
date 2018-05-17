from urllib.request import FancyURLopener, HTTPError
import re
import sys
import os

from url_list import List

class AppURLopener(FancyURLopener):     			 
   	version = "Mozilla/5.0"

def URLparser(URL):
	try:
		html = AppURLopener().open(URL)
	except HTTPError as e:
		print(e)
		print("[*] HTTP ERROR!")
		sys.exit(1)

if __name__ == '__main__':
	for i in List:
		print(i['url'])
		print(i['info'])