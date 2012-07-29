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

import cPickle as pickle
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

def sorted_map(map):
    ms = sorted(map.iteritems(), key=lambda (k, v): (-v, k))
    return ms

g = pickle.load(open('graph.pkl'))

d = g.degree()
ind = g.in_degree()
outd = g.out_degree()
c = nx.closeness_centrality(g)
b = nx.betweenness_centrality(g)
e = nx.eigenvector_centrality(g)

table = [(node, [d[node], ind[node], outd[node], c[node], b[node], e[node]])
         for node in g.nodes()]

columns = ['degree', 'in_degree', 'out_degree', 'closeness',
           'betweenness', 'eigenvector']
table = pd.DataFrame.from_items(table, orient='index', columns=columns)
table.to_csv('centralities.csv')
