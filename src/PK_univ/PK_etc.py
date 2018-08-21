from db_manager import db_manage
import datetime

dt = datetime.datetime.now()
today = str(dt.year) + "-" + str(dt.month) + "-" + str(dt.day)

list = [

{"url":"http://dormitory.pknu.ac.kr/03_notice/notice01.php",
	"title":"오늘의 식단",
	"post":"식사는 카드인식 후 가능하며, 자율배식으로 합니다.\
	식사예절 준수, 용모, 복장을 단정히 하고 건강을 위해 끼니를 거르지 않고\
	규칙적으로 식사하도록 합시다.",
	"date":today,
	'tag':["기숙사"]}
]

def crawling():
	db_manage("add","PK_etc",list)

