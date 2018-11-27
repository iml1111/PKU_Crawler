import pymongo 

db_name = 'pookle'
ip = 'localhost'
port = 27017

def Search(db, text):
	from operator import itemgetter
	result = []
	obj_list = []
	text_list = text.split(" ")

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
		i['count'] += len(i['element'])*5

	result = sorted(result, key=itemgetter('count','date'),reverse = True)
	return result

def db_access():
	client = pymongo.MongoClient(ip,port)
	db = client[db_name]
	return db

if __name__ == '__main__':

	n = input("Search: ")
	List = Search(db_access(),n)
	print(List)
	print()
	if len(List) >= 4:
		print("This is Top4")
		print(List[0])
		print(List[1])
		print(List[2])
		print(List[3])
