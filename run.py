import os
from datetime import date,datetime,time
import xlrd
from Database_Connect import insert
import pymysql
import logging
import pandas

logging.basicConfig(filename='info.log', filemode="w", level=logging.DEBUG)


def open_file(filename='xxx.xlsx'):
    try:
        data = xlrd.open_workbook(filename)
        return data
    except Exception as e :
        print(e)


def read_file(filename):
    data = open_file(filename)
    table = data.sheets()[0]
    nrows = table.nrows #行数
    ncols = table.ncols #列数

    #print('行：{0}    列：{1}'.format(nrows,ncols))
    data = getRow(nrows, ncols,table)


    return data

def getStandardTime(table,i):
   # print(table.name,i)
   try:
        tmp = xlrd.xldate.xldate_as_datetime(table.cell(i, 2).value, 1)
        month = tmp.month
        day = tmp.day
        year = tmp.year - 4
        if day == 1 and month == 1:
            year -= 1
            month = 12
            day = 1
        elif month == 3 and day == 1:
            month = 2
            if (year % 4):
                day = 28
            else:
                day = 29
        elif day == 1:
            month -= 1
            if (month in [1, 3, 5, 7, 8, 10, 12]):
                day = 31
            else:
                day = 30
        else:
            day -= 1
        # print(year,month,day)
        return datetime(year, month, day, hour=tmp.hour, minute=tmp.minute, second=tmp.second)
   except Exception as e:
        print(e)
        logging.info('   {0}'.format(e))
        return datetime(2015, 2, 6, hour=0, minute=0, second=0)

def getRow(nrows,ncols,table):
    data = []
    for i in range(1,nrows):
        rowdata=[]
        #data.append(table.row_values(i)[2])

       # tmptime = pandas.Timestamp("{0}-{1}-{2} {3}".format(tmp.year-4,tmp.month,tmp.day-1))
       # print(tmp, '>', year,'-', month, '-', day, ' ', tmp.time())
        #print('sss->>>>>>>>{0}'.format(tmp))
        for col in range(0,5):
            col_data = table.row_values(i)[col]
            print(col_data,type(col_data),col_data=='')
            if(~isinstance(col_data,str)):
                col_data = str(col_data)
            if(col==2):
                col_data=getStandardTime(table,i)
            rowdata.append(col_data)
        data.append(rowdata)  #某一行数据
    return data



def database_modify(name,data):
    db = pymysql.connect(host='localhost',user='root', password='123456', port=3306,db='secrank',charset="utf8mb4")
    cursor = db.cursor()
    count=1;
    for item in data:
        print('{0}   {1}'.format(count,item))
        #logging.info('   {0}'.format(item))
        insert(db,'company_news',name,item)
        count+=1
    db.close()


def main():
    rootdir = 'D:\Anaconda3\myproject\excel_transfer_mysql\secrank_data'
    list = os.listdir(rootdir)  # the list of the folder's child folder and file
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])
        print(list[i])
        if os.path.isfile(path):
            data = read_file(path)
            print('>>>>>>>>>>>>>>>',list[i].split('.')[0])
            #logging.info('transfering the {0} file>>>>>>>>{1}>>>>>>>'.format(i,list[i]))
            #print('transfering the {0} file>>>>>>>>{1}>>>>>>>'.format(i,list[i]))
            database_modify( list[i].split('.')[0] , data )

#single file test
def tmp():
    data = read_file('secrank_data/NetEye.xlsx')
    print(data)

    database_modify('NetEye.xlsx'.split('.')[0], data)


if __name__ == "__main__":
    #tmp()
    main()
