#!/bin/python3

import requests
import re
from bs4 import BeautifulSoup
import random

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
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
    url="http://www.9800.com.tw/lotto38/statistics.html"
    msg += "20: %s\n" % str(getMagicNumber(url)) 
    url="http://www.9800.com.tw/lotto38/statistics10.html"
    msg += "10: %s\n" % str(getMagicNumber(url))
    url="http://www.9800.com.tw/lotto38/statistics50.html"
    msg += "50: %s\n" % str(getMagicNumber(url))
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=msg))

def getHistoryNormalNumber(url):
    res  = requests.get(url)
    soup = BeautifulSoup(res.text,'html.parser')
    
    wei_li = []
    for i in soup.find_all(style="color:#FF0000; font-weight:bold"):
        wei_li.append(int(i.text))
    
    for k in range(1,39):
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

def getMagicNumber(url):
    normal = getHistoryNormalNumber(url)
    s = getHistorySpecialNumber(url)

    jp=[]
    n=0
    while n < 7:
        m = random.choice(normal) 
        if m not in jp:
            jp.append(m)
            n += 1
    return sorted(jp), random.choice(s)

if __name__ == '__main__':
    const PORT = process.env.PORT || 3000;
    app.run(debug=options.debug, port=PORT;
)
