#!/bin/python3
# -*- coding: utf-8 -*

import requests
import re
from bs4 import BeautifulSoup
import random
import os

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, MessageAction
)

app = Flask(__name__)

line_bot_api = LineBotApi('PHuXH5SG5kB5c3cvAMX6BnGVI9RK4F/D+oOEgzdEONlnsl7IEd/GXlSyhuVcFPAItbz+leGrCNW/1gsRcDje/auILLF33vFYp+qHkd6zysU1aMDwf8RJDel7ZsgTx4+U65dqpvRjTztNUlT7Ql25FAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('81fc893049b942fe6e0ba189b58d212a')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    
    game_type = event.message.text.split(' ')[0]
    game_category = ""
    if game_type != "wl" and game_type != "bl":
        buttons_template = TemplateSendMessage(
            alt_text='Buttons Template',
            template=ButtonsTemplate(
                title='發大財囉～～',
                text='點選一個開始產生幸運號碼！',
                thumbnail_image_url='顯示在開頭的大圖片網址',
                actions=[
                    MessageAction(
                        label='威力彩',
                        text='wl'
                    ),
                    MessageAction(
                        label='大樂透',
                        text='bl'
                    )
                ]
            )
        )
        line_bot_api.reply_message(
            event.reply_token, buttons_template)   
        return
    elif (game_type == "wl"):
        game_category = "lotto38"
        game_name = "威力彩"
    elif (game_type == "bl"):
        game_category = "lotto649"
        game_name = "大樂透"
    if event.source.type == "room":
        to_id = event.source.room_id
    else:
        to_id = event.source.user_id
    print event.source.type, to_id
    line_bot_api.push_message(to_id, TextSendMessage(text=game_name+"幸運數字產生中..."))
    msg = game_name + " 幸運數字:\n"
    url = "http://www.9800.com.tw/"+game_category+"/statistics10.html"
    msg += "近10期隨機: %s\n" % str(getMagicNumber(url, game_type))
    url = "http://www.9800.com.tw/"+game_category+"/statistics.html"
    msg += "近20期隨機: %s\n" % str(getMagicNumber(url, game_type)) 
    url = "http://www.9800.com.tw/"+game_category+"/statistics50.html"
    msg += "近50期隨機: %s\n" % str(getMagicNumber(url, game_type))
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=msg))
    
def getHistoryNormalNumber(url, game_type):
    res  = requests.get(url)
    soup = BeautifulSoup(res.text,'html.parser')
    num_length = 0
    if game_type == "wl":
        num_length = 39
    if game_type == "bl":
        num_length = 49
        
    wei_li = []
    for i in soup.find_all(style="color:#FF0000; font-weight:bold"):
        wei_li.append(int(i.text))
    
    for k in range(1,num_length):
    #    print(str(k)+": " + "{:.0%}".format(wei_li.count(k)/float(len(wei_li))))
        wei_li.append(k)
    return wei_li

def getHistorySpecialNumber(url):
    res  = requests.get(url)
    soup = BeautifulSoup(res.text,'html.parser')

    special_ball = []
    for j in soup.find_all(style="color:blue; font-weight:bold"):
        special_ball.append(int(j.text))
    for l in range(1,9):
    #    print(str(l)+": " + "{:.0%}".format(special_ball.count(l)/float(len(special_ball))))
        special_ball.append(l)
    return special_ball

def getMagicNumber(url, game_type):
    normal = getHistoryNormalNumber(url, game_type)
    if game_type == "wl":
        num_length = 6
        s = getHistorySpecialNumber(url)
        jp=[]
        n=0
        while n < num_length:
            m = random.choice(normal) 
            if m not in jp:
                jp.append(m)
                n += 1
        return sorted(jp), random.choice(s)
    
    if game_type == "bl":
        num_length = 7
        jp=[]
        n=0
        while n < num_length:
            m = random.choice(normal) 
            if m not in jp:
                if n == 6:
                    s = m
                else:
                    jp.append(m)
                n += 1
        return sorted(jp), s
    return

if __name__ == '__main__':
    myPORT = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=myPORT)
