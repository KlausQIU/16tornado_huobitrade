'use strict';

var PublicDealUrl = 'ws://'+window.location.host+'/api/PublicDealMessage'
function PublicDealMessage(){
    var PublicDealws = new WebSocket(PublicDealUrl);
    PublicDealws.onopen = function(){
        PublicDealws.send('JS PublicDealWs Open')
    }
    PublicDealws.onmessage = function(event){
        var PublicData = JSON.parse(event.data);
        var item = PublicData.PublicDealMessage
        var html = ''
        var ltcdata = PublicData.ltc;
        var newLtcprice = $(".ltcprice").text()
        newLtcprice = newLtcprice.substring(1)
        var btcdata = PublicData.btc;
        var newBtcprice = $(".btcprice").text()
        newBtcprice = newBtcprice.substring(1)
        html += '<li class="add_style tradeMessage" id="dealnext">'+item.time+'&nbsp;&nbsp;'+item.type+'&nbsp;&nbsp;&nbsp;&nbsp;'+item.price+'&nbsp;&nbsp;&nbsp;&nbsp;'+item.amount+'</li>';
        $("#dealnext").before(html);
        $(".loading").remove();
        $(".add_style:not(:first-child)").removeClass('add_style')
        if($(".tradeMessage").size() >= 13){
            $(".tradeMessage:last").remove()
        }
        if(newLtcprice < ltcdata){
              ltcprice.html("￥"+ltcdata+"  <span class='fa fa-up  fa-4x fa-arrow-up'></span>").fadeOut('slow');
              ltcprice.css("color","#05e4a1")
              ltcprice.html("￥"+ltcdata+"  <span class='fa fa-up  fa-4x fa-arrow-up'></span>").fadeIn('slow');
            }else if(newLtcprice > ltcdata){
              ltcprice.html("￥"+ltcdata+"  <span class='fa fa-down  fa-4x fa-arrow-down'></span>").fadeOut('slow');
              ltcprice.css("color","#f64a83")
              ltcprice.html("￥"+ltcdata+"  <span class='fa fa-down  fa-4x fa-arrow-down'></span>").fadeIn('slow');
            }else{
              ltcprice.html("￥"+ltcdata).fadeOut('slow');
              ltcprice.css("color","#00aced")
              ltcprice.html("￥"+ltcdata).fadeIn('slow');
            }
    if(newBtcprice < btcdata){
      btcprice.html("￥"+btcdata+"  <span class='fa fa-up  fa-4x fa-arrow-up'></span>").fadeOut('slow');
      btcprice.css("color","#05e4a1")
      btcprice.html("￥"+btcdata+"  <span class='fa fa-up  fa-4x fa-arrow-up'></span>").fadeIn('slow');
    }else if(newBtcprice > btcdata){
      btcprice.html("￥"+btcdata+"  <span class='fa fa-down  fa-4x fa-arrow-down'></span>").fadeOut('slow');
      btcprice.css("color","#f64a83")
      btcprice.html("￥"+btcdata+"  <span class='fa fa-down  fa-4x fa-arrow-down'></span>").fadeIn('slow');
    }else{
      btcprice.html("￥"+btcdata).fadeOut('slow');
      btcprice.css("color","#00aced")
      btcprice.html("￥"+btcdata).fadeIn('slow');
    }
    $('.tradeVol').html(PublicData.ltcTradeVol)
    }
    }
$(function(){
PublicDealMessage()
});

  