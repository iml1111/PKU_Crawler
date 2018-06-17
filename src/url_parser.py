from urllib.request import FancyURLopener, HTTPError
from selenium import webdriver

class AppURLopener(FancyURLopener):     			 
   	version = "Mozilla/5.0"

def URLdriving(URL):
	print('URL parsing > ' + URL['url'])
	driver = webdriver.PhantomJS()
	driver.implicitly_wait(1)
	driver.get(URL['url'])

	return driver

def URLparser(URL):
	try:
		html = AppURLopener().open(URL)
	except HTTPError as e:
		print(e)
		print("[*] HTTP ERROR!")
		sys.exit(1)	

	return html