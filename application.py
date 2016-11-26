#!/usr/bin/env python
# coding:utf-8

import tornado.web
import os


# get cookie_secret
# import base64
# import uuid
# print base64.b64encode(uuid.uuid4().bytes+uuid.uuid4().bytes)

settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    xsrf_cookies=False,
    cookie_secret="RYxFqFQyRCiCZ/nxFfTMCrbqZpRZ5UW9tQ86fKvrfIw=",
    login_url="/login",
    debug=True,
    autoreload=False
)