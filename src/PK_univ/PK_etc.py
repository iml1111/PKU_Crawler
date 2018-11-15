from db_manager import db_manage
from recent_date import get_today

today = get_today()

list = [

{"url":"http://dormitory.pknu.ac.kr/03_notice/notice01.php",
	"title":"학생생활관 오늘의 식단",
	"post":"식사는 카드인식 후 가능하며, 자율배식으로 합니다.\
	식사예절 준수, 용모, 복장을 단정히 하고 건강을 위해 끼니를 거르지 않고\
	규칙적으로 식사하도록 합시다.",
	"date":today,
	'tag':["기숙사","사이트"]},

{"url":"http://lms.pknu.ac.kr/ilos/main/main_form.acl",
	"title":"부경대학교 - LMS",
	"post":"학사일정 및 강의관련 공지사항 등을 확인하실 수 있습니다.",
	"date":today,
	'tag':["기타","사이트"]},

{"url":"https://ebook.pknu.ac.kr/FxLibrary/",
	"title":"부경대학교 전자책 도서관",
	"post":"여러 분야에 관련된 책을 대여할 수 있습니다.",
	"date":today,
	'tag':["기타","사이트"]},

{"url":"http://lms.pknu.ac.kr/ilos/main/main_form.acl",
	"title":"부경대학교 학사일정",
	"post":"부산광역시 남구 용소로 45(608-737)본관 503호 기초교양교육원 TEL. 051-629-6947 FAX. 051-629-6949",
	"date":today,
	'tag':["기타","사이트"]},

{"url":"http://cms.pknu.ac.kr/counseling/main.do",
	"title":"부경대학교 학생상담센터",
	"post":"인생의 든든한 동반자 부경대학교 학생상담센터 부산광역시 남구 용소로 45, 부경대학교 대연캠퍼스 동원 장보고관 3층 학생상담센터 (대연동) TEL:(051)629-6763~5 FAX:(051)629-6766",
	"date":today,
	'tag':["기타","사이트"]},

{"url":"http://cms.pknu.ac.kr/counseling/main.do",
	"title":"부경대학교 자료실",
	"post":"필요한 자료를 올리고 다운받아가세요. 여러분이 올려주시는 자료는 많은 도움이 됩니다.",
	"date":today,
	'tag':["기타","사이트"]},

{"url":"http://cms.pknu.ac.kr/duem/main.do",
	"title":"부경대학교 글로벌자율전공학부",
	"post":"부산광역시 남구 용소로 45(대연동 부경대학교대연캠퍼스) 웅비관 3층 1318호 TEL:051-629-5650~1 FAX:051-629-5651",
	"date":today,
	'tag':["글로벌자율전공학부","사이트"]},

{"url":"http://cms.pknu.ac.kr/korean/main.do",
	"title":"부경대학교 국어국문학과",
	"post":"부산광역시 남구 용소로 45(대연동 부경대학교대연캠퍼스) 인문사회과학대학 국어국문학과 TEL:051)629-5405 FAX:051)629-5408",
	"date":today,
	'tag':["국어국문학과","사이트"]},

{"url":"http://ce.pknu.ac.kr/main/main.php",
	"title":"부경대학교 컴퓨터공학과",
	"post":"부산광역시 남구 용소로 45 부경대학교 대연캠퍼스 누리관(A13) 2223호 TEL 051-629-6260(대학원),   6261(학과),   7805(SST, SCSC) │ FAX 051-629-6264",
	"date":today,
	'tag':["컴퓨터공학과","사이트"]},

{"url":"http://cms.pknu.ac.kr/japanese/main.do",
	"title":"부경대학교 일어일문학부",
	"post":"부산광역시 남구 용소로 45, 인문사회경영관(C25) 일어일문학부(1412호) (대연동) TEL: 051-629-5390 FAX: 051-629-5393",
	"date":today,
	'tag':["일어일문학부","사이트"]}
]

def crawling():
	db_manage("add","PK_etc",list)

