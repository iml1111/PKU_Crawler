from pydblite.sqlite import Database, Table
import os
import datetime

t = datetime.datetime.now()
db_list_path = ".\\DB_list\\"
'''
왜 안되지? 
con_table = ('no','INTEAGER'),('title','TEXT'),('email','TEXT'),\
('file_is','INTEAGER'),('file_link','TEXT'),('post','TEXT'),\
('author','TEXT'),('date','TEXT'),('count','INTEAGER'),
'''

class Table_iml(Table):
    def insert(self, args):
        ks = args.keys()
        sql = "INSERT INTO %s" % self.name
        sql += "(%s) VALUES (%s)"
        sql = sql % (', '.join(ks), ','.join(['?' for k in ks]))
       
        self.cursor.execute(sql, list(args.values()))
        return self.cursor.lastrowid


def db_manage(mode = None, db_name = None, record = None):
	if mode == "add":
		add_record(db_name, record)


def add_record(db_name = None, record = None):
	db_path = db_list_path + db_name + str(t.month) + str(t.day) + ".db"
	db = Database(db_path)
	table = Table_iml("post", db)
	table.create(('no','INTEAGER'),('title','TEXT'),('email','TEXT'),\
				('file_is','INTEAGER'),('file_link','TEXT'),('post','TEXT'),\
				('author','TEXT'),('date','TEXT'),('count','INTEAGER'), mode ="open")
	table.open()
	table.insert(record)
	db.commit()
	db.close()
	
	
	 	

	 



