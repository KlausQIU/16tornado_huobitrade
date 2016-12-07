# !/usr/bin/env python
# -*- coding:utf-8 -*-
# 
import sqlite3
import os
import sys
import time

def intailze(func):
    def init(self,*args,**kw):
        self.cx = sqlite3.connect(r'C:\Klaus\System\17DB\16tornado_huobitrade\huobi.db')
        self.cursor = self.cx.cursor()
        return func(self,*args,**kw)
        self.close()
    return init

class db_control():
    def __init__(self):
        pass

    @intailze
    def pragma(self,tableName):
        try:
            sql = 'PRAGMA table_info('+tableName+')'
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            self.cx.commit()
            self.cursor.close()
            self.cx.close()
            return result
        except BaseException as e:
            print u'Error:',e

    @intailze
    def creatTable(self,tableName,*args):
        sql = 'create table '
        sql += tableName
        field = ''
        for value in args:
            if value == args[-1]:
                field += value
            else:
                field += value+','
        field = '(' + field + ')' 
        sql += field
        try:
            self.cursor.execute(sql)
            self.cx.commit()
            print u'new table %s has been build'%tableName
            self.cursor.close()
            self.cx.close()
        except BaseException as e:
            print u'Error:',e

    @intailze
    def insert(self,tableName,*args):
        sql = 'insert into '+tableName+' values('
        field = ''
        for index in range(0,len(args)-1):
            if type(args[index]) != int or type(args[index]) != float :
                field += "'%s'"%args[index]+',' 
            else:
                field += '%s'%args[index]+','
        field += "'%s'"%args[len(args)-1]
        field = field + ')' 
        sql += field
        try:
            self.cursor.execute(sql)
            self.cx.commit()
            print u'new data %s has been insert'%args
            self.cursor.close()
            self.cx.close()
        except BaseException as e:
            print u'Error:',e

    @intailze
    def select(self,tableName,*args,**kw):
        sql = 'select '
        if args:
            for value in args:
                sql += value if value == args[-1] else value+','
            sql += 'from '+ tableName
        else:
            sql += '* from '+tableName
        if kw:
            for key in kw:
                sql += ' where %s'%key + '=' + '"%s"'%kw[key]
        result = self.cursor.execute(sql)
        rowlist = []
        for row in result:
            if len(row) == 0:
                return []
            rowlist.append(list(row))
        return rowlist
        
    @intailze
    def delete(self,tableName,**kw):
        sql = "DELETE from "+tableName +' where '
        if kw:
            print len(kw)
            if len(kw) == 1:
                for key in kw:
                    sql += key + '=' + ('%s' if type(kw[key]) == int else '"%s"')%kw[key] 
            else:
                for key in kw:
                    sql += key + '=' + ('%s' if type(kw[key]) == int else '"%s"')%kw[key] + ' and '
                sql = sql[:-4]
            try:   
                self.cursor.execute(sql)
                self.cx.commit()
                print u'delete success'
                self.cursor.close()
                self.cx.close()
            except:
                print u'delete fail'
        else:
            sql = 'drop table '+tableName
            try: 
                self.cursor.execute(sql)
                self.cx.commit()
                self.cursor.close()
                self.cx.close()
                print u'delete %s success'%tableName
            except:
                print u'delete %s fail'%tableName

    @intailze
    def update(self,tableName,updateRow,selectRow):
        sql = 'update '+tableName+' set '
        for key in updateRow:
            sql += key + '=' + ('%s' if type(updateRow[key]) == int else '"%s"')%updateRow[key] + ','
        sql = sql[:-1]
        sql += ' where '
        for key in selectRow:
            sql += key + '=' + ('%s' if type(selectRow[key]) == int else '"%s"')%selectRow[key] + ' and '
        sql = sql[:-4]
        print sql
        try:   
            self.cursor.execute(sql)
            self.cx.commit()
            print u'update success'
            return {'msg':'success'}
            self.cursor.close()
            self.cx.close()
        except BaseException as e:
            print u'update fail',e
            return {'msg':['fail',e]}

    @intailze
    def alert(self,tableName,updateRow):
        sql = 'ALTER TABLE '+tableName+' ADD COLUMN '
        for key in updateRow:
            sql = sql + key + ' '+ updateRow[key]
        print sql
        try:   
            self.cursor.execute(sql)
            self.cx.commit()
            print u'update success'
            return {'msg':'success'}
            self.cursor.close()
            self.cx.close()
        except BaseException as e:
            print u'update fail',e
            return {'msg':['fail',e]}

    @intailze
    def run(self,sql):
        try:   
            result = self.cursor.execute(sql)
            self.cx.commit()
            print u'run success'
            rowlist = []
            for row in result:
                if len(row) == 0:
                    return []
                rowlist.append(list(row))
            self.cursor.close()
            self.cx.close()
            return rowlist if rowlist else {'msg':'success'}
        except BaseException as e:
            print u'run fail',e
            return {'msg':['fail',e]}

    def close(self):
        try:
            self.cursor.close()
            self.cx.close()
        except:
            print u'close Error'


if __name__ == '__main__':
    db = db_control()
    #db.creatTable('profitData','NO INTEGER','Time BLOB','id integer','uid integer','Profit BLOB')
    #db.creatTable('fibonacciGrid','id integer','uid integer','position')
    #db.creatTable('user','id integer primary key','uid integer','name varchar(10) UNIQUE','password TEXT','access_key text UNIQUE','secret_key text UNIQUE')
    #db.creatTable('huobi','id integer primary key','uid integer','name varchar(10) UNIQUE','password TEXT','access_key text UNIQUE','secret_key text UNIQUE')
    #db.creatTable('AllStrategy','uid integer','Grid BLOB','TradePenny BLOB')
    #db.creatTable('TradePenny','uid integer','BuyOrSell BLOB','Coin Blob','Amount BLOB','Price BLOB','Status Blob')
    #db.creatTable('publicData','Time BLOB','DEALDATA BLOB','TICKERLTC BLOB','TICKERBTC BLOB','LTCTRADEVOL BLOB')
    #db.creatTable('privateData','uid BLOB','Time BLOB','NET_ASSET BLOB','PROFITRATE BLOB','TOTAL BLOB','BOMBPRICE BLOB')
    #db.creatTable('ltcData','Time BLOB','xBxisData BLOB','ltcData BLOB')
    #{u'status': 2, u'order_time': 1481013283, u'order_amount': u'1.0000', u'last_processed_time': 1481013836, u'order_price': u'24.47', u'type': 2, u'id': 385718198, u'processed_amount': u'1.0000'}
    # db.creatTable('dealOrder','uid BLOB','time BLOB','order_id integer','order_time BLOB','last_processed_time BLOB','order_amount BLOB','order_price BLOB','type BLOB')
    # updateRow = {'access_key':'','secret_key':''}
    # selectRow = {'id':1}
    # db.update('user',updateRow,selectRow)
    c = db.select('dealOrder',uid=0)
    print c[-5:]
    # for d in c:
    #     if float(d[4]):
    #         print d
    #         print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(float(d[4])))
    # db.delete('dealOrder',uid='0')
    result = db.run('SELECT * FROM dealOrder WHERE uid="0" order by "last_processed_time" asc limit 0,10')
    print result
    
    #db.insert('AllStrategy',0,'false','false')
    #db.delete('profitData',Profit=u'1150.87')
    #print min(item[4] for item in db.select('profitData'))
    # updateRow = {'PriceDict':'BLOB'}
    # d = db.alert('SETTING', updateRow)
    # print d
    # #sqlRun = 'PRAGMA table_info([SETTING])'
    # d = db.pragma('tradePenny')
    # print d
    # updateRow = {'order_id':'BLOB'}
    # db.alert('tradePenny',updateRow)
    # print db.select('SETTING',uid=1)
    #db.insert('user',0,0,'Moon','qiu','7ffd4f94-63d605e6-d5f400fb-a6ba0','d5d52f33-dcbd2167-5c6b7b0f-f5676')
    # db.insert('tradePenny',0,'Sell','LTC',1,27.61,0,u'测试一个')
    #print db.select('tradePenny')