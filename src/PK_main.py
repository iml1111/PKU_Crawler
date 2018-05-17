from bs4 import BeautifulSoup

PK_domain = "http://www.pknu.ac.kr"

def parsing(bs0bj):
	bs0bj = bs0bj.find("table",{"class":"bbs-list"})
	summary = bs0bj.attrs['summary']
	list_parse(bs0bj)


def list_parse(bs0bj):
	post_list = bs0bj.findAll("tr")

	for post in post_list:
		obj = post.find("td",{"class":"no"})
		if obj != None and obj.get_text() != "":
			print(obj.get_text())

			obj = post.find("td",{"class":"title"})
			print(obj.get_text().strip())

			obj = obj.find("a").attrs['href']
			print(obj)

			obj = post.find("td",{"class":"author"})
			print(obj.get_text())

			obj = post.find("td",{"class":"file"})
			if obj.get_text() == "-":
				print(False)
			else:
				print(True)

			obj = post.find("td",{"class":"date"})
			print(obj.get_text())

			obj = post.find("td",{"class":"count"})
			print(obj.get_text())


def content_parse():
	pass
