#!/usr/bin/env python
#-*- coding:utf-8 -*-

import tornado.web


class IndexHandler(tornado.web.RequestHandler):

    '''
    主页处理类
    '''

    def get(self):
        self.write("Index")

