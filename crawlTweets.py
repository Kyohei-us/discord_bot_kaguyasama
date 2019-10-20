import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
import time, datetime

import os
from dotenv import load_dotenv
load_dotenv()
CONSUMER_KEY = os.environ.get('API_KEY')
CONSUMER_SECRET = os.environ.get('API_SECRET_KEY')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

import json #標準のjsonモジュールとconfig.pyの読み込み
from requests_oauthlib import OAuth1Session #OAuthのライブラリの読み込み

CK = CONSUMER_KEY
CS = CONSUMER_SECRET
AT = ACCESS_TOKEN
ATS = ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS) #認証処理

def letscrawl(tweets, keywordFromOutside):
    keyword = keywordFromOutside

    url = "https://api.twitter.com/1.1/search/tweets.json?q=" + keyword + "&result_type=mixed&count=10" #タイムライン取得エンドポイント

    params ={'count' : 5} #取得数
    res = twitter.get(url, params = params)

    limit = res.headers['x-rate-limit-remaining']
    reset = res.headers['x-rate-limit-reset']
    sec = int(int(reset) - time.mktime(datetime.datetime.now().timetuple()))
    tweets.append("limit is {}.\nreset is {}.\nIn second, {}".format(limit, reset, sec))
    print(limit + " is limit")

    if res.status_code == 200: #正常通信出来た場合
        timelines = json.loads(res.text) #レスポンスからタイムラインリストを取得
        for line in timelines['statuses']: #タイムラインリストをループ処理
            #print(line['text'])
            #print("--------------------------------------")
            tweets.append('--------------------------\n{}:\n\nprofile image is :\n{}\n\n{}\n--------------------------'.format(line['user']['name'],line['user']['profile_image_url_https'],line['text']))
            #print(line['user']['name']+':\n:'+line['text'])
            #print(line['created_at'])
            #print('*******************************************')
    else: #正常通信出来なかった場合
        print("Failed: %d" % res.status_code)

    return tweets

def seeLists(tweets):

    url = "https://api.twitter.com/1.1/lists/statuses.json?slug=main&owner_screen_name=UniversityKenCA&count=10"

    params ={'count' : 5} #取得数
    res = twitter.get(url, params = params)

    limit = res.headers['x-rate-limit-remaining']
    reset = res.headers['x-rate-limit-reset']
    sec = int(int(reset) - time.mktime(datetime.datetime.now().timetuple()))
    tweets.append("limit is {}.\nreset is {}.\nIn second, {}".format(limit, reset, sec))
    print(limit + " is limit")

    if res.status_code == 200: #正常通信出来た場合
        timelines = json.loads(res.text) #レスポンスからタイムラインリストを取得
        for line in timelines: #タイムラインリストをループ処理
            #print(line['text'])
            #print("--------------------------------------")
            tweets.append('{}\n\n{}\n--------------------------'.format(line['user']['name'],line['text']))
            #print(line['user']['name']+':\n:'+line['text'])
            #print(line['created_at'])
            #print('*******************************************')
    else: #正常通信出来なかった場合
        print("Failed: %d" % res.status_code)

    return tweets
