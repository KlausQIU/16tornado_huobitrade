'use strict';

$(function(){
var HuobiLtcTradeUrl = 'ws://'+window.location.host+'/api/HuobiLtcTrade';
var HuobiLtcTradews = new WebSocket(HuobiLtcTradeUrl)
$(".SellHuobiLtc,.BuyHuobiLtc").click(HuobiLtcTrade);
/***
HuobiLtcTradews.onmessage = function(event){
    var data = JSON.parse(event.data);
    $("span.availableLtc").text(data.available_ltc_display)
    $("input[name='SellPrice']").val(data.tradePrice);
    $("input[name='SellCount']").val(data.available_ltc_display);
    $("span[name='SellTradeMoney']").text(parseFloat(data.tradePrice)+'  CNY')
    
    $("span.availableCny").text(data.available_cny_display)
    $("input[name='BuyPrice']").val(data.tradePrice);
    $("input[name='BuyCount']").val(1);
    $("span[name='BuyTradeMoney']").text(parseFloat(data.tradePrice)+'  CNY')
}
***/



function HuobiLtcTrade(){
    var ws = new WebSocket(HuobiLtcTradeUrl)
    var SellCount,SellPrice,tradeMoney,BuyCount,BuyPrice,marketBuyCount,marketSellCount
    var type = this.name
    ws.onopen = function(){
        console.log(type)
        SellPrice = $("input[name='SellPrice']").val()
        SellCount = $("input[name='SellCount']").val()
        BuyPrice = $("input[name='BuyPrice']").val()
        BuyCount = $("input[name='BuyCount']").val()
        marketBuyCount = $("input[name='marketBuyCount']").val()
        marketSellCount = $("input[name='marketSellCount']").val()
        if(type == 'SellHuobiLtc'){
        var data = {"Price":SellPrice,"Count":SellCount,"type":type}
        tradeMoney = parseFloat(SellCount)*parseFloat(SellPrice)
        }else if(type == 'BuyHuobiLtc'){
        var data = {"Price":BuyPrice,"Count":BuyCount,"type":type}
        tradeMoney = parseFloat(BuyCount)*parseFloat(BuyPrice)
        }
        else if(type == 'BuyMarketLtc'){
        var data = {"Count":marketBuyCount,"type":type}
        tradeMoney = parseFloat(marketBuyCount)*parseFloat(BuyPrice)
        }
        else if(type == 'SellMarketLtc'){
        var data = {"Count":marketSellCount,"type":type}
        tradeMoney = parseFloat(marketSellCount)*parseFloat(BuyPrice)
        }
        ws.send(JSON.stringify(data));
    }
    ws.onmessage = function(event){
        var dataR = JSON.parse(event.data);
        var ltcCount = parseFloat($("span.availableLtc").text())
        var availableCny = parseFloat($("span.availableCny").text())
        console.log(dataR)
        if(dataR.msg=="success" && dataR.type == "SellHuobiLtc"){
        $("span.availableLtc").text(ltcCount-SellCount)

        swal({
            title:"委托成功",
            text:"卖出价格: "+SellPrice+" 卖出数量: "+SellCount,
            timer:1000,
            type:"success",
            showConfirmButton:false
            }
            );
        //swal("委托成功", "卖出价格: "+SellPrice+" 卖出数量: "+SellCount, "success")
        
        }else if(dataR.msg=="success" && dataR.type =="BuyHuobiLtc"){
            $("span.availableCny").text((availableCny-tradeMoney).toFixed(2))
        swal("委托成功", "买入价格: "+BuyPrice+" 买入数量: "+BuyCount, "success")
        }else if(dataR.msg =='fail'){
            swal("卖出失败","自己找原因","error")
        }
        ws.close()
    }
}
})