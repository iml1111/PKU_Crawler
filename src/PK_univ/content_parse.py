from bs4 import BeautifulSoup

def text_parsing(bs0bj, domain, re = 0):
	children = bs0bj.findChildren(recursive = False)
	content = ""

	if not children:
		return ""

	for tag in children:
		if tag.get('src') != None:
			content += ("\n<태그>: " + tag.name + "\n")
			content += ("src: " + domain + tag.attrs['src'] + "\n")
			content += ("</태그>\n" + "\n")

		if tag.get('href') != None:
			content += ("\n<태그>: " + tag.name + "\n")
			content += ("src: " + domain + tag.attrs['href'] + "\n")
			content += ("태그 내용:", tag.get_text() + "\n")
			content += ("</태그>\n" + "\n")

		texts = tag.get_text()
		if texts != None and re == 0:
			content += (texts + "\n")

		return content + text_parsing(tag, domain, 1)