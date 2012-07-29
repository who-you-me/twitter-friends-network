# -*- coding: utf-8 -*-
#
# Copyright 2012 Hisao Soyama <hisao.soyama@gmail.com>
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

import cPickle as pickle
import json
import os
import urllib
import tweepy
from twToken import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# nodes.pklがなければAPIにアクセスしてfriendsを取得
# idをkey, screen_nameをvalueとする辞書にして保存
if not os.path.exists('./nodes.pkl'):
    ids = api.friends_ids()
    
    nodes = {}
    while ids:
        print len(ids)
        for node in api.lookup_users(user_ids=ids[:100]):
            nodes[node.id] = node.screen_name
        ids = ids[100:]
    
    pickle.dump(nodes, open('./nodes.pkl', 'w'))
else:
    nodes = pickle.load(open('./nodes.pkl'))

# 訪問済みnodeはvisitedに格納
if not os.path.exists('./visited.pkl'):
    visited = []
else:
    visited = pickle.load(open('./visited.pkl'))

# edgesはedges.pklに保存
if not os.path.exists('./edges.pkl'):
    edges = {}
else:
    edges = pickle.load(open('./edges.pkl'))

# 未訪問nodesのみ取り出す
sources = list(set(nodes.keys()) - set(visited))

try:
    for i, source in enumerate(sources):
        print i+1, len(sources), source
        dests = api.friends_ids(user_id=source)
        edges[source] = dests
        visited.append(source)
    print '取得完了しました。'
except Exception, E:
    print E
    print 'API切れの可能性があります。'
    print 'しばらく待ってから再実行してください。'
finally:
    # 異常終了時もedgesとvisitedは永続化
    pickle.dump(visited, open('./visited.pkl', 'w'))
    pickle.dump(edges, open('./edges.pkl', 'w'))
