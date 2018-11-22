from urllib.request import FancyURLopener, HTTPError
from selenium import webdriver

class AppURLopener(FancyURLopener):     			 
   	version = "Mozilla/5.0"

def URLdriving(URL):
	print('Driver : PhantomJS')
	driver = webdriver.PhantomJS("./phantomjs-2.1.1-windows/bin/phantomjs")
	
	try:
		driver.get(URL['url'])
	except:
		print("Connection Error")
		try:
			driver.get(URL['url'])
		except:
			return None

	driver.implicitly_wait(1)

	return driver

def URLparser(URL):
	try:
		html = AppURLopener().open(URL)
	except:
		print("Connection Error")
		try:
			html = AppURLopener().open(URL)
		except:
			return None

	return html