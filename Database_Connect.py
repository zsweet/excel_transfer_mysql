import pymysql
import logging
logging.basicConfig(filename='info.log', filemode="w", level=logging.DEBUG)

#creat a database
#the db must conect the database
#databaseName is the name of your database
def creat_database(db,databaseName):
    cursor = db.cursor
    try:
        cursor.execute("CREATE DATABASE {0} DEFAULT CHARACTER SET utf8mb4".format(databaseName))
    except Exception as e:
        print('creating tables error，error information：{0}'.format(e))

#creat table
#the db must conect the database ,and must bind the database where you will create a table
#tableName is the name of your table
def creat_table(db,tableName):
    cursor = db.cursor()
    sql = 'CREATE TABLE IF NOT EXISTS {0} (id INT(10) NOT NULL AUTO_INCREMENT,name VARCHAR(255) NOT NULL,title VARCHAR(255),content TEXT,time TIMESTAMP,source VARCHAR(255),url VARCHAR(255), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,updated_at TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,deleted_at TIMESTAMP,PRIMARY KEY(id))'.format(tableName)
    cursor.execute(sql)


#insert data to database
#the db must conect the database ,and must bind the database where you will create a table
#the variable name & data is the data
def insert(db,table,name,item):
    cursor = db.cursor()
    sql = 'INSERT INTO {0}(name, title, content, time, source, url) values(\'{1}\', \'{2}\',\'{3}\', \'{4}\', \'{5}\', \'{6}\')'.format(table,name, item[0], item[1], item[2], item[3], item[4])
   # print(sql)
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        logging.info('error information：{0}'.format(e))
        print('error information：{0}'.format(e))

# get the version of mysql,this can be used to check
# whether connecting the database seccessfully
#the db must conect the database
#the excute and fetch must belong to the same cursor
def version_test(db):
    cursor = db.cursor()
    cursor.execute('SELECT VERSION()')
    data = cursor.fetchone()
    print('Database version:', data)
    return data

def connect(myhost='localhost',myuser='root',mypassword='123456',myport=3306,mydb='secrank',mycharset="utf8"):
    db = pymysql.connect(host=myhost,user=myuser, password=mypassword, port=myport,db=mydb,charset=mycharset)
    return db

def main():
    db = connect('localhost','root', '123456', 3306,'secrank',"utf8mb4")
    data = version_test(db)
    logging.info(data)
    creat_table(db,'company_news')
   #  cursor = db.cursor()
   #  sql = 'INSERT INTO company_news(name, time,deleted_at) ' \
   #        'values(\'NetEye\', \'2017-01-13 21:35:23\',null)'
   #  print(sql)
   #  cursor.execute(sql)
    db.commit()
    db.close()

if __name__ == '__main__':
    main()
