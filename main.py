#!/usr/bin/env python
# coding:utf-8

import tornado.ioloop
import tornado.options
import tornado.httpserver
import tornado.web
import tornado.process
from tornado.options import define, options
from tornado.tcpserver import TCPServer  
import tornado.netutil

from url import url
from application import settings
from handlers.data_collection.profitData import ProfitDataCollection
import threading
import multiprocessing
from apscheduler.schedulers.tornado import TornadoScheduler


define("port", default="7788", help="run on the given port", type=int)
#test

class Application(tornado.web.Application):

    def __init__(self):
        tornado.web.Application.__init__(self, url, **settings)


if __name__ == '__main__':
    import os
    import sys
    sys.path.append(os.getcwd())
    try:
        #ProfitDataCollection()
        #tornado.ioloop.PeriodicCallback(ProfitDataCollection, 900000).start()
        #windows
        tornado.options.parse_command_line()
        http_server = tornado.httpserver.HTTPServer(Application())
        http_server.listen(options.port)
        tornado.ioloop.IOLoop.instance().start()
        #linux
        # sockets = tornado.netutil.bind_sockets(7788)
        # tornado.process.fork_processes(0)
        # server = tornado.httpserver.HTTPServer(Application())
        # server.add_sockets(sockets)
        # tornado.ioloop.IOLoop.instance().start()
    except (KeyboardInterrupt, SystemExit):
        pass
    

#python C:\Klaus\System\16tornado_huobitrade\main.py