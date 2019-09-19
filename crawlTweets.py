import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary

CONSUMER_KEY = "RP2J9vbernYv0XOjjpm2HST2h"
CONSUMER_SECRET = "pQvjV4piscKWS0DtyZo6XVQIPyP7XafymvSkV736CmSaXCzgYs"
ACCESS_TOKEN = "1117174431850221568-6g9IerfbvLsz0a4ZJhBMGxaip0aj2k"
ACCESS_TOKEN_SECRET = "UwVHlvl8xDxNMLL8DpgxiZMLcFISzLgfdEEWsTRgdzNco"

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
    tweets.append(limit + " is limit")
    print(limit + " is limit")

    if res.status_code == 200: #正常通信出来た場合
        timelines = json.loads(res.text) #レスポンスからタイムラインリストを取得
        for line in timelines['statuses']: #タイムラインリストをループ処理
            #print(line['text'])
            #print("--------------------------------------")
            tweets.append("--------------------------")
            tweets.append(line['user']['name']+':\n\n{}:\n\n{}'.format(line['user']['profile_image_url_https'],line['text']))
            tweets.append("--------------------------")
            #print(line['user']['name']+':\n:'+line['text'])
            #print(line['created_at'])
            #print('*******************************************')
    else: #正常通信出来なかった場合
        print("Failed: %d" % res.status_code)

    return tweets
