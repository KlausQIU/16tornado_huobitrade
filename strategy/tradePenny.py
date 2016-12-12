#!/usr/bin/env python
# coding:utf-8
# 
from huobi.HuobiMain import * 
import json,urllib2
import sys
import os
append_path =  os.path.dirname(os.getcwd())
sys.path.append(append_path)
import urllib2,json,time,threading
from handlers.data_collection import db as d
from strategy.huobi import HuobiService
import operator
from strategy import parameter as p
from personalHandler import personalHandler as PH
__author__ = 'KlausQiu'


class tradePenny():

    def __init__(self,a_key,s_key):
        pass





if __name__ == '__main__':
    while True:
        #check sql  db.select('AllStrategy',uid=uid)
        #check setting db.select('SETTING',uid=uid)
        #run trade 
