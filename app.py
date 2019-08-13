#!/bin/python3

import requests
import re
from bs4 import BeautifulSoup
import random

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
    url="http://www.9800.com.tw/lotto38/statistics.html"
    print "20: %s" % str(getMagicNumber(url))
    url="http://www.9800.com.tw/lotto38/statistics10.html"
    print "10: %s" % str(getMagicNumber(url))
    url="http://www.9800.com.tw/lotto38/statistics50.html"
    print "50: %s " % str(getMagicNumber(url))
