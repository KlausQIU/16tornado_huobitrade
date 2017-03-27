#!/usr/bin/env python
# coding:utf-8

import tornado.web
import os
import sys
import time
from datetime import datetime
import db as dbL
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
from strategy import personalHandler as pH



def ProfitDataCollection():
    while True:
        print 'enter ProfitDataColleciton'
        db = dbL.db_control()
        users = db.select('user')
        print users
        for user in users:
            if len(user[4]) == 32 and len(user[5]) == 32:
                now = datetime.now()
                print 'now:',now.strftime('%Y%m%d-%H:%M')
                str_time = now.strftime('%M')
                timeRun = [0,15,30,45,60,0]
                if int(str_time) in timeRun:
                    personalH = pH.personalHandler(user[4].encode('utf-8'),user[5].encode('utf-8'))
                    profitData = db.select('profitData',uid=user[1])
                    setting = db.select('SETTING',UID=user[1])
                    count = max([item[0] for item in profitData])+1 if profitData else 0
                    profit = personalH.profit
                    if profit == 0:
                        return
                    db.insert('profitData',count,time.strftime('%Y%m%d%H%M%S'),setting[0][0],setting[0][0],profit)
                else:
                    for n in timeRun:
                        if timeRun[timeRun.index(n)-1] < int(str_time) < n:
                            print u'休息时间'
                            print (n-int(str_time))*60
                            time.sleep((n-int(str_time))*60)
                            personalH = pH.personalHandler(user[4].encode('utf-8'),user[5].encode('utf-8'))
                            profitData = db.select('profitData',uid=user[1])
                            setting = db.select('SETTING',UID=user[1])
                            count = max([item[0] for item in profitData])+1 if profitData else 0
                            profit = personalH.profit
                            if profit == 0:
                                return
                            db.insert('profitData',count,time.strftime('%Y%m%d%H%M%S',time.localtime()),setting[0][0],setting[0][0],profit)
            else:
                pass
        time.sleep(60)
        
if __name__ == '__main__':
    while True:
        ProfitDataCollection()
        time.sleep(60)