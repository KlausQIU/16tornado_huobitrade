#!/usr/bin/env python
# coding:utf-8

import tornado.web
import application


url = [(r"^/(favicon\.ico)", tornado.web.StaticFileHandler,
         dict(path=application.settings['static_path']))]
url += [(r"^/", "handlers.huobi.LoginHandler")]
url += [(r"^/main","handlers.huobi.HuobiHandler")]
url += [(r"^/login", "handlers.huobi.LoginHandler")]
url += [(r"^/account", "handlers.huobi.HuobiHandler")]
url += [(r"^/trade", "handlers.huobi.TradeHandler")]
url += [(r"^/entrust", "handlers.huobi.entrustHandler")]
url += [(r"^/logout", "handlers.huobi.LogoutHandler")]
url += [(r"^/grid", "handlers.huobi.gridHandler")]
url += [(r"^/tradeStrategy", "handlers.huobi.tradeStrategyHandler")]
url += [(r"^/HuobiLtc", "handlers.huobi.HuobiLtcHandler")]
url += [(r"^/api/accountInfo", "handlers.ApiHandler.accountInfo")]
url += [(r"^/api/Profit", "handlers.ApiHandler.ProfitHandler")]
url += [(r"^/api/entrust", "handlers.ApiHandler.entrustInfo")]
url += [(r"^/api/entrustCancel", "handlers.ApiHandler.entrustCancel")]
url += [(r"^/api/tradeSetting", "handlers.ApiHandler.tradeSetting")]
url += [(r"^/api/tradeSetInfo", "handlers.ApiHandler.tradeSetInfo")]
url += [(r"^/api/APIInfo", "handlers.ApiHandler.APIInfo")]
url += [(r"^/api/dealMessage", "handlers.ApiHandler.dealMessage")]
url += [(r"^/api/avatarInfo", "handlers.ApiHandler.avatarInfo")]
url += [(r"^/api/gridSetApi", "handlers.ApiHandler.gridSetApi")]
url += [(r"^/api/tradePennySet", "handlers.ApiHandler.tradePennySetHandler")]
url += [(r"^/api/tradeOrderSet", "handlers.ApiHandler.tradeOrderSetHandler")]
url += [(r"^/api/tradePennyShow", "handlers.ApiHandler.tradePennyShow")]
url += [(r"^/api/dealOrders", "handlers.ApiHandler.dealOrders")]
# url += [(r"^/api/btcData", "handlers.ApiHandler.btcDataHandler")]
url += [(r"^/api/handlerltc", "handlers.ApiHandler.handlerltcHandler")]
url += [(r"^/api/PublicDealMessage", "handlers.ApiHandler.PublicDealMessage")]
url += [(r"^/api/DrawProfit", "handlers.ApiHandler.DrawProfit")]
url += [(r"^/api/HuobiLtcTrade", "handlers.ApiHandler.HuobiLtcTrade")]



