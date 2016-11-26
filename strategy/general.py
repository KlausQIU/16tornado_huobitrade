#!/usr/bin/env python
# coding:utf-8
# 
import sys
import os

def float_format(number):
    return float('%.2f'%number)


PublicData = 0

def judgeData(data): 
    global PublicData
    if PublicData == 0:
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


if __name__ == '__main__':
    print dealdata(5)
    print dealdata(6)
    print dealdata(6)