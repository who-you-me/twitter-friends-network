# coding: utf-8
#
#
# Copyright 2011 Hisao Soyama <hisao.soyama@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# myFriendsテーブルからfriendsのidを取り出し，screen_nameを取得

import json
import urllib

import MySQLdb
import oauth2 as oauth

con = MySQLdb.connect(user=USER, passwd=PASSWD, db='twitterNetwork', charset='UTF8')
cur = con.cursor()

# id取り出す
cur.execute("SELECT target FROM myFriends")
ids = [id[0] for id in cur.fetchall()]

# Oauthクライアントを作成
consumer = oauth.Consumer(key=YOUR_APP_KEY, secret=YOUR_APP_SECRET)
token = oauth.Token(key=YOUR_TOKEN_KEY, secret=YOUR_TOKEN_SECRET)
client = oauth.Client(consumer, token)

# エンドポイントURL
url = 'http://api.twitter.com/1/users/lookup.json'

while ids:
    # idを100個取り出しカンマで結合する
    params = {'user_id': ','.join([str(id) for id in ids[:100]])}
    del ids[:100]
    
    # OauthクライアントからAPIに接続．contentを取り出す
    res = client.request(url+'?'+urllib.urlencode(params), 'GET')
    content = json.loads(res[1])
    
    # screen_nameをmyFrinedsテーブルに入れる
    for c in content:
        print c['id'], c['screen_name']
        sql = "UPDATE myFriends SET screen_name = '%s' WHERE target = %d" % (c['screen_name'], c['id'])
        cur.execute(sql)
    con.commit()
