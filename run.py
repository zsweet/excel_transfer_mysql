import os
import xlrd
from Database_Connect import insert
import pymysql
import logging

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


def getRow(nrows,ncols,table):
    data = []
    for i in range(1,nrows):
        rowdata=[]
        for col in range(0,5):
            col_data = table.row_values(i)[col]
            if(~isinstance(col_data,str)):
                col_data = str(col_data)
            rowdata.append(col_data)
        data.append(rowdata)  #某一行数据
    return data



def database_modify(name,data):
    db = pymysql.connect(host='localhost',user='root', password='123456', port=3306,db='tmp',charset="utf8mb4")
    cursor = db.cursor()
    for item in data:
        print('   {0}'.format(item))
        logging.info('   {0}'.format(item))
        insert(db,'tmp',name,item)
    db.close()


def main():
    rootdir = 'D:\Anaconda3\myproject\secrank_data_process\secrank_data'
    list = os.listdir(rootdir)  # the list of the folder's child folder and file
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])
        if os.path.isfile(path):
            data = read_file(path)
            #logging.info('transfering the {0} file>>>>>>>>{1}>>>>>>>'.format(i,list[i]))
            #print('transfering the {0} file>>>>>>>>{1}>>>>>>>'.format(i,list[i]))
            database_modify( list[i].split('.')[0] , data )

#single file test
def tmp():
    data = read_file('secrank_data/NetEye.xlsx')
    database_modify('NetEye.xlsx'.split('.')[0], data)


if __name__ == "__main__":
    #tmp()
    main()
