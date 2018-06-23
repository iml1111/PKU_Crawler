from urllib.request import FancyURLopener, HTTPError
from selenium import webdriver

class AppURLopener(FancyURLopener):     			 
   	version = "Mozilla/5.0"

def URLdriving(URL):
	print('Driver : PhantomJS')
	driver = webdriver.PhantomJS("./phantomjs-2.1.1-windows/bin/phantomjs")
	driver.get(URL['url'])
	driver.implicitly_wait(1)

	return driver

def URLparser(URL):
	try:
		html = AppURLopener().open(URL)
	except HTTPError as e:
		print(e)
		print("[*] HTTP ERROR!")
		sys.exit(1)	

	return html