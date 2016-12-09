#!/usr/bin/env python
# coding:utf-8
# 
import sys
import os

def float_format(number):
    return float('%.2f'%number)


PublicData = None
dlistJudgeData = None

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
def doubleListJudge(listData):
    global dlistJudgeData
    if type(listData) == list:
        if not dlistJudgeData:
            tupleData = []
            if type(listData[0]) == list:
                for i in listData:
                    tupleData.append(tuple(i))
            dlistJudgeData = tupleData if tupleData else listData
            return listData
        else:
            tupleData = []
            if type(listData[0]) == list:
                for i in listData:
                    tupleData.append(tuple(i))
            diff = list(set(tupleData).difference(set(dlistJudgeData)))
            dlistJudgeData = tupleData if tupleData else listData
            return diff if diff else None




if __name__ == '__main__':
    print dealdata(5)
    print dealdata(6)
    print dealdata(6)