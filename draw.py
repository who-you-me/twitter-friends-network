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

# ネットワーク描画

import matplotlib.pyplot as plt
import MySQLdb
import networkx as nx

con = MySQLdb.connect(user=USRE, passwd=PASSWD, db='twitterNetwork', charset='UTF8')
cur = con.cursor()

# TwitterはDirected Graph
g = nx.DiGraph()

# idとscreen_name対応付けた辞書
cur.execute("SELECT target, screen_name FROM myFriends")
ids = {}
for id in cur.fetchall():
    ids[id[0]] = id[1]

# friends同士の関係のみを取り出してグラフに追加
cur.execute("SELECT * FROM friends")
for edge in cur.fetchall():
    if edge[1] in ids:
        g.add_edge(ids[edge[0]], ids[edge[1]])

# ノードの大きさを入次数に比例させる
node_size = {}
for v in g:
    node_size[v] = float(g.in_degree(v)) * 2 + 2

# 入次数いくつ以上だとscreen_name表示…みたいな処理
"""
labels = {}
for name in ids.values():
    if node_size[name] > 1000:
        labels[name] = name
    else:
        labels[name] = ''
"""

# 描画の際にはUndirected Graphに変換
g = nx.Graph(g)
nx.draw(g, pos=nx.spring_layout(g), with_labels=False, node_size=[node_size[v] for v in g],
        node_color='red', width=0.1, alpha=0.7)
plt.show()