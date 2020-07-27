#!/bin/python3
# -*- coding: utf-8 -*

import requests
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
import re
from bs4 import BeautifulSoup
import random
import os

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, MessageAction
)

from dbModel import *
import json
import datetime

#app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['LINE_BOT_API_ID'])
handler = WebhookHandler(os.environ['WEBHOOK_HANDLER_ID'])

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
    if game_type != "wl" and game_type != "bl" and game_type != "wl_result" and game_type != "bl_result":
        buttons_template = TemplateSendMessage(
            alt_text='Buttons Template',
            template=ButtonsTemplate(
                title='發大財囉～～',
                text='點選一個開始產生幸運號碼！',
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
        # 踩雷: reply_token 只能用一次
        line_bot_api.reply_message(
            event.reply_token, buttons_template)   
        return
    elif (game_type == "wl"):
        game_category = "lotto38"
        game_name = "威力彩"
    elif (game_type == "bl"):
        game_category = "lotto649"
        game_name = "大樂透"
    elif (game_type == "wl_result"):
        game_category = "lotto38"
        game_name = "威力彩"        
    elif (game_type == "bl_result"):
        game_category = "lotto649"
        game_name = "大樂透"
    if event.source.type == "room":
        to_id = event.source.room_id
    else:
        to_id = event.source.user_id
    print event.source.type, to_id
    try:
        user_profile = line_bot_api.get_profile(to_id)
        print user_profile
        user_profile = str(user_profile).replace("'",'"')
        userInfo_dump = json.dumps(str(user_profile)) #, ensure_ascii=False, encoding='utf-8')
        print userInfo_dump
        userInfo = json.loads(str(userInfo_dump), encoding='utf-8')
        print userInfo
        for i in userInfo:
            print i
        print userInfo['displayName']
        print userInfo['pictureUrl']
    except LineBotApiError as e:
        print e
    # error handle
    if "_result" in game_type:
        #line_bot_api.push_message(to_id, TextSendMessage(text=game_name+"取得近期彩號中..."))
        msg = game_name + " 近期彩號:\n"
        url = "http://www.9800.com.tw/"+game_category
        msg += getResult(url, game_type)
    else:
        #line_bot_api.push_message(to_id, TextSendMessage(text=game_name+"幸運數字產生中..."))
        msg = game_name + " 幸運數字:\n"
        url = "http://www.9800.com.tw/"+game_category+"/statistics10.html"
        round_10 = str(getMagicNumber(url, game_type))
        msg += "近10期隨機: \n%s\n" % round_10
        url = "http://www.9800.com.tw/"+game_category+"/statistics.html"
        round_20 = str(getMagicNumber(url, game_type))
        msg += "近20期隨機: \n%s\n" % round_20
        url = "http://www.9800.com.tw/"+game_category+"/statistics50.html"
        round_50 = str(getMagicNumber(url, game_type))                    
        msg += "近50期隨機: \n%s\n" % round_50
        #insertdata
        numbers = round_10+",\n "+round_20+",\n "+round_50
        print('-----in----------')
        add_data = usermessage(
                id = to_id,
                user_name = userInfo['displayName'],
                user_image = userInfo['pictureUrl'],
                message = str(numbers),
                date = datetime.datetime.now()
            )
        db.session.add(add_data)
        db.session.commit()
        #db.close()
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=msg))
    
# 取得歷史中獎號碼
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
        wei_li.append(k)
    return wei_li

# 取得歷史中獎特別號
def getHistorySpecialNumber(url):
    res  = requests.get(url)
    soup = BeautifulSoup(res.text,'html.parser')

    special_ball = []
    for j in soup.find_all(style="color:blue; font-weight:bold"):
        special_ball.append(int(j.text))
    for l in range(1,9):
        special_ball.append(l)
    return special_ball

# 產生幸運號碼
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
        num_length = 6
        jp=[]
        n=0
        while n < num_length:
            m = random.choice(normal) 
            if m not in jp:
                jp.append(m)
                n += 1
        return sorted(jp)
    return

def getResult(url, game_type):
    html = urlopen(url).read()
    bs = BeautifulSoup(html, "lxml")
    table = bs.find(lambda tag: tag.has_attr('id') and tag['id']=="news_sort")
    rows = table.findAll(lambda tag: tag.name=='tr')
    res = ""
    for i in rows:
        res += "\n======================\n"
        if i.text != "":
            res += i.text.strip().replace('\n\n', '\n')
    return res.encode('utf-8')

if __name__ == '__main__':
    myPORT = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=myPORT)
