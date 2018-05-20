from pydblite.sqlite import Database, Table
import os
import datetime

t = datetime.datetime.now()
db_list_path = "DB_list\\"
'''
튜플 언패킹 ???
con_table = ('title','TEXT'),('email','TEXT'),('file_is','TEXT'),\
				('file_link','TEXT'),('post','TEXT'),('author','TEXT'),\
				('date','TEXT'),('count','TEXT')
'''


def db_manage(mode = None, db_name = None, record = None):
	
	if mode == "add":
		add_record(db_name, record)


def add_record(db_name = None, record = None):

	db_path = db_list_path + db_name + str(t.month) + str(t.day) + ".db"
	db = Database(db_path)
	table = Table("post", db)
	table.create(('title','TEXT'),('email','TEXT'),('file_is','INTEAGER'),\
				('file_link','TEXT'),('post','TEXT'),('author','TEXT'),\
				('date','TEXT'),('count','INTEAGER'),mode ="open")
	table.open()
	print(record.values())
	table.insert(record.values())
	table.close()
	
	 	

	 



