# -*- coding: utf-8 -*-
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

import os
import cPickle as pickle
import matplotlib.pyplot as plt
import networkx as nx

if not os.path.exists('./graph.pkl'):
    g = nx.DiGraph()
    
    nodes = pickle.load(open('./nodes.pkl'))
    edges = pickle.load(open('./edges.pkl'))
    sources = set(edges.keys())
    for source, dests in edges.iteritems():
        inDests = set(dests) & sources
        for dest in inDests:
            g.add_edge(nodes[source], nodes[dest])

    pickle.dump(g, open('graph.pkl', 'w'))
else:
    g = pickle.load(open('graph.pkl'))

# ノードの大きさを入次数に比例させる
node_size = {}
for node in g:
    node_size[node] = float(g.in_degree(node)) * 2 + 2

# 描画の際にはUndirected Graphに変換
g = nx.Graph(g)
nx.draw(g, nx.spring_layout(g), with_labels=False,
        node_size=[node_size[node] for node in g],
        node_color='red', width=0.1, alpha=0.7)
plt.savefig('./myNetwork.png', dpi=200)
plt.show()
