import re
import string
import pymongo 
import os
import datetime
from operator import itemgetter

db_name = 'uni_board'
ip = 'localhost'
port = 27017

def Search(text):
	result = []
	obj_list = []
	text_list = text.split(" ")
	db = db_access()

	for element in text_list:

		for col in db.collection_names():

			if col == "recent_date":
				continue

			coll_list = list(db[col].find({"title":{"$regex":element}}))
			coll_list.extend(list(db[col].find({"tag":{"$elemMatch": {"$regex":element }}})))
			coll_list.extend(list( db[col].find({"post":{"$regex":element}})))

			for i in coll_list:
				if i['_id'] in obj_list:
					for j in result:
						if j['_id'] == i['_id']:
							j['count'] += 1
							j['element'].add(element)

				else:
					obj_list.append(i['_id'])
					i.update({"count":1})
					i.update({"element":set([element])})
					result.append(i)

	for i in result:
		i['count'] += len(i['element'])*3


	result = sorted(result, key=itemgetter('count'),reverse = True)
	return result

def db_access():
	client = pymongo.MongoClient(ip,port)
	db = client[db_name]
	return db

if __name__ == '__main__':

	n = input("Search: ")
	List = Search(n)
	print(List)
	print()
	print("This is Top4")
	print(List[0])
	print(List[1])
	print(List[2])
	print(List[3])
