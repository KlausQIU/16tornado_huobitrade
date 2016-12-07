#!/usr/bin/env python
# coding:utf-8
# 
import sys
import os

def float_format(number):
    return float('%.2f'%number)


PublicData = None
listJudgeData = None

def judgeData(data): 
    global PublicData
    if not PublicData:
        PublicData = data
        return data
    else:
        if data == PublicData:
            return None
        else:
            PublicData = data
            return data

def float_format(number):
    return float('%.2f'%number)



#列表的数据对比，输出listdata的不同值
def listJudge(listData):
    if type(listData) == list:
        if not listData:
            listJudgeData = listData
            return listJudgeData
        else:
            diff = list(set(listData).difference(set(listJudgeData)))
            listJudgeData = listData
            return diff if diff else None


if __name__ == '__main__':
    print dealdata(5)
    print dealdata(6)
    print dealdata(6)