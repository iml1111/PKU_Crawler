import pymongo 
import random
import datetime

now = datetime.datetime.now() - datetime.timedelta(days = 90)
date = now.strftime("%Y-%m-%d %H:%M:%S")

db_name = 'pookle'
ip = 'localhost'
port = 27017

def View(db, itag, etag):
	from operator import itemgetter
	from random import shuffle
	result = []
	degree_list = []

	if "공지" in itag:
		is_main = True
	else:
		is_main = False

	for i in itag:
		if i.endswith("학과") == True or i.endswith("교육과") == True \
			or i.endswith("학부") == True:
			degree_list.append(i)

	for col in db.collection_names():
		if col.startswith("PK_") == False:
				continue
		#메인타임라인의 경우 타학과공지 제외
		if is_main == True:
			coll_list = list(db[col].find(
														{"$and":[
																{"tag":{ "$in": itag }},	
																{"$or":[
																	{"$and":[
																			{"tag": {"$not": {"$elemMatch":{"$regex":"학과$"}}}},
																			{"tag":{"$not": {"$elemMatch":{"$regex":"학부$"}}}},
																			{"tag":{"$not": {"$elemMatch":{"$regex":"교육과$"}}}}
																		]
																	},
																	{"tag": {"$in": degree_list}},
																	]
																},
																{"tag":{"$nin":etag }}
															]
														}))
		#서브타임라인의 경우 타학과 게시글 포함
		else: 
			coll_list = list(db[col].find(
														{"$and":[
																{"tag":{ "$in": itag }},	
																{"tag":{"$nin":etag }}
															]
														}))
		#3달이내의 글만 갖고옴
		for i in coll_list:
			if i['date'] >= date:
				result.append(i)
	'''
	timeline = []
	timeline[0] = sorted(result, key=itemgetter("fav_cnt","view","date"), reverse = True)
	timeline[1] = shuffle(result)

	fav_line = 0
	normal_line = 0
	result = []

	for i in range(len(List[0])):

		if i % 3 == 0:
			post = List[0][fav_line]
			fav_line += 1
		else: 
			post = List[1][normal_line]
			normal_line += 1
		
		is_dedup = False
		for j in result:
			if post['_id'] == j['_id']:
				is_dedup = True
				break

		if is_dedup == True:
			continue
		else:
			result.append(post)
	'''
	result = sorted(result, key=itemgetter("date"), reverse = True)
	return result


def db_access():
	client = pymongo.MongoClient(ip,port)
	db = client[db_name]
	return db

if __name__ == '__main__':

	include_tag = [
	#메인
	["기타","공지","거래","대나무숲","반짝정원","지식인","장학"],
	#진로
	["창업지원단","취업","창업","진로"],
	#스터디&모임
	['스터디&모임',"특강","세미나","봉사","동아리"],
	#알바&구인
	["조교","과외&강사","알바&구인"],
	#행사&대외활동
	["행사","봉사","공모전&대외활동","교육&설명회","멘토링"],
	]

	exclude_tag = []
	List =View(db_access(),include_tag[1], exclude_tag)
	print(date)
	for i in range(10):
		index = random.randrange(0,len(List))
		print(List[index]['title'])
		print(List[index]['tag'])
		print(List[index]['date'])
		print()
	print(len(List))

'''
timeline = []
timeline[0] = sorted(result, key=itemgetter("fav_cnt","view","date"), reverse = True)
timeline[1] = shuffle(result)

fav_line = 0
normal_line = 0
result = []

for i in range(len(List[0])):

	if i % 3 == 0:
		post = List[0][fav_line]
		fav_line += 1
	else: 
		post = List[1][normal_line]
		normal_line += 1
	
	is_dedup = False
	for j in result:
		if post['_id'] == j['_id']:
			is_dedup = True
			break

	if is_dedup == True:
		continue
	else:
		result.append(post)
'''