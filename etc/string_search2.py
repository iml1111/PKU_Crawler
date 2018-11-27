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

			coll_list = list(db[col].find({"$or":[{"title":{"$regex":element}},\
													{"tag":{"$elemMatch": {"$regex":element }}},\
													{"post":{"$regex":element}}\
													]}))
			for i in coll_list:
				if i['_id'] in obj_list:
					for j in result:
						if j['_id'] == i['_id']:
							if j['title'].find(element) != -1:
								j["count"] += 1
							if type(j['post']) is str and j['post'].find(element) != -1:
								j["count"] += 1
							for tag in j['tag']:
								if tag.find(element) != -1:
									j["count"] += 1
									break
							j['element'].add(element)
				else:
					obj_list.append(i['_id'])
					i.update({"count":0})
					if i['title'].find(element) != -1:
						i["count"] += 1
					if type(i['post']) is str and i['post'].find(element) != -1:
						i["count"] += 1
					for tag in i['tag']:
						if tag.find(element) != -1:
							i["count"] += 1
							break
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
