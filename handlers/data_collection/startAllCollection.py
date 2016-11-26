# !/usr/bin/env python
# -*- coding:utf-8 -*-
# 
__author__ = 'klausQiu'

import publicData
import profitData
import privateData
import urllib2,json,time,threading



def threading_run(target,args):
    if target:
        t = threading.Thread(target=target,args=args)
        threads.append(t)

if __name__ == '__main__':
    threads = []
    threading_run(publicData.main,())
    threading_run(profitData.ProfitDataCollection,())
    threading_run(privateData.main,()) 
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()
