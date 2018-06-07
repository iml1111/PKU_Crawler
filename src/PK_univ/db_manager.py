from pymongo import MongoClient 
import os
import datetime

t = datetime.datetime.now()

db_name = 'uni_board'
ip = 'localhost'
port = 27017

def db_manage(mode, coll_name = None, doc = None):
	db = db_access()
	if coll_name != None:
		coll = db[coll_name]
	
	if mode == "add":
		coll.insert(doc)
	elif mode == "view":
		for col in db.collection_names():
			if db[col].count() != 0:
				print(col + " count: " + str(db[col].count()))
				db[col].remove({})

def db_access():
	client = MongoClient(ip,port)
	db = client[db_name]
	return db

	
	
	 	

	 



