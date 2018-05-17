from urllib.request import FancyURLopener, HTTPError

class AppURLopener(FancyURLopener):     			 
   	version = "Mozilla/5.0"

def URLparser(URL):
	try:
		html = AppURLopener().open(URL)
	except HTTPError as e:
		print(e)
		print("[*] HTTP ERROR!")
		sys.exit(1)
		
	return html