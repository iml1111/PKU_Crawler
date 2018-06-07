from pymongo import MongoClient 
import os
import datetime

t = datetime.datetime.now()

db_name = 'uni_board'
ip = 'localhost'
port = 27017

def db_manage(mode, coll_name, doc = None):
	coll = db_access(coll_name)
	
	if mode == "add":
		coll.insert(doc)
	elif mode == "view":
		for doc in coll.find():
			print(doc)

def db_access(coll_name):
	client = MongoClient(ip,port)
	db = client[db_name]
	coll = db[coll_name]

	return coll

	
	
	 	

	 



