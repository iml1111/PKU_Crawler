import pymongo 
import os
import datetime
# 디버깅을 위한 코드, 추후에 전체 수정 필요
t = datetime.datetime.now()
filter_list = ["페미","냄져","한남"]

#확장 필요
db_name = 'pookle'
ip = 'localhost'
port = 27017

def db_manage(mode, coll_name = None, doc = None, is_first = None):
	db = db_access()
	if coll_name != None and mode != "renewal_date":
		coll = db[coll_name]
	else:
		coll = db['recent_date']
	

	if mode == "add":
		print('DB_insert the [ ' + coll_name + ' ] with dedups.')
		for i in doc:
			cnt = 0
			for j in coll.find({'title':i['title']},\
									{'_id':0,'title':1}).\
										sort([("date", -1)]):
				if i['title'] == j['title']:
					cnt = 1
					break

				for i in filter_list:
					if i[title].find(i) == -1:
						cnt = 1
						break

			if cnt == 0:
				# i 변수가 하나의 게시물
				# 여기다가 추가하고픈 게시물의 원하는 칼럼 붙여넣으면 됨 
				# ex) i.update({"추가할 항목":"추가할 값"})
				coll.insert(i)
			else:
				continue


	elif mode == "renewal_date":
		if is_first == True:
			# 몽고쉘에서는 나왔음!
			db['recent_date'].insert(doc)
		else:
			db['recent_date'].update({"name":coll_name}, doc)


	elif mode == "get_recent":
		return db['recent_date'].find_one({"name":coll_name})


	elif mode == "view":
		for col in db.collection_names():
			if db[col].count() != 0:
				print(col + " count: " + str(db[col].count()))

			if col == 'recent_date':
				for i in db[col].find():
					print(i)
			else:
				for i in db[col].find({},{'_id':0,'date':1,'title':1}\
											).sort([("date", -1)]):
					print(i)

	elif mode == "all_remove":
		for col in db.collection_names():
			if db[col].count() != 0:
				db[col].remove({})


def db_access():
	client = pymongo.MongoClient(ip,port)
	db = client[db_name]
	return db

	
	
	 	

	 



