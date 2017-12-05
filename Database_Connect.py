import pymysql
import logging
logging.basicConfig(filename='info.log', filemode="w", level=logging.DEBUG)

class MyDataBase:
    global db,cursor
    #creat a database
    #the db must conect the database
    #databaseName is the name of your database
    def creat_database(self,databaseName):
        try:
            self.cursor.execute("CREATE DATABASE {0} DEFAULT CHARACTER SET utf8mb4".format(databaseName))
        except Exception as e:
            print('creating tables error，error information：{0}'.format(e))

    #creat table
    #the db must conect the database ,and must bind the database where you will create a table
    #tableName is the name of your table
    def creat_table(self,tableName):
        sql = 'CREATE TABLE IF NOT EXISTS {0} (' \
              'id INT(10) NOT NULL AUTO_INCREMENT,' \
              'name VARCHAR(255) NOT NULL,title VARCHAR(255),' \
              'content TEXT,time VARCHAR(255),' \
              'source VARCHAR(255),url VARCHAR(255), ' \
              'PRIMARY KEY(id))'.format(tableName)
        self.cursor.execute(sql)


    #insert data to database
    #the db must conect the database ,and must bind the database where you will create a table
    #the variable name & data is the data
    def insert(self,table,name,item):
        sql = 'INSERT INTO {0}(name, title, content, time, source, url) ' \
              'values(%s, %s, %s, %s, %s, %s)'.format(table)
        try:
            self.cursor.execute(sql, (name, item[0], item[1], item[2], item[3], item[4]))
            self.db.commit()
        except Exception as e:
            db.rollback()
            logging.info('insert error information：{0}'.format(e))
            print('insert error information：{0}'.format(e))

    #query function
    def query(self,sql = ''):
       try:
           self.cursor.execute(sql)
       except Exception as e:
           db.rollback()
           logging.info('select error information：{0}'.format(e))
           print('query error information：{0}'.format(e))

    #modify function
    def  modify(self,sql = ' '):
        try :
            self.cursor.execute(sql) #执行sql
            self.db.commit() #提交修改
        except Exception as e:
            db.rollback()
            logging.info('select error information：{0}'.format(e))
            print('modify error information：{0}'.format(e))

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()



    # get the version of mysql,this can be used to check
    # whether connecting the database seccessfully
    #the db must conect the database
    #the excute and fetch must belong to the same cursor
    def version_test(self):
        self.cursor.execute('SELECT VERSION()')
        data = self.cursor.fetchone()
        print('Database version:', data)
        return data

    def connect(self,myhost,myuser,mypassword,myport,mydb,mycharset):
        self.db = pymysql.connect(host=myhost,user=myuser, password=mypassword, port=myport,db=mydb,charset=mycharset)
        self.cursor = self.db.cursor()

    def close(self):
        self.db.close()
