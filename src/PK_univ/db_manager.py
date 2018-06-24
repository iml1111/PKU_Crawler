import pymongo 
import os
import datetime
# 디버깅을 위한 코드, 추후에 전체 수정 필요
t = datetime.datetime.now()

db_name = 'uni_board'
ip = 'localhost'
port = 27017

def db_manage(mode, coll_name = None, doc = None):
	db = db_access()
	if coll_name != None:
		coll = db[coll_name]
	
	if mode == "add":
		print('DB_insert the [ ' + coll_name + ' ] with dedups.')
		#개선 필요한 중복 제거 알고리즘
		for i in doc:
			cnt = 0
			for j in coll.find():
				if i['title'] == j['title']:
					cnt = 1
					break
			if cnt == 0:
				coll.insert(i)
			else:
				continue			

	elif mode == "view":
		for col in db.collection_names():
			if db[col].count() != 0:
				print(col + " count: " + str(db[col].count()))
				
				for i in db[col].find({},{'_id':0,'date':1,'title':1}\
											).sort([("date", -1)]):
					print(i)
				'''
				for i in db[col].find():
					print(i)
				'''
				db[col].remove({})

def db_access():
	client = pymongo.MongoClient(ip,port)
	db = client[db_name]
	return db

	
	
	 	

	 



