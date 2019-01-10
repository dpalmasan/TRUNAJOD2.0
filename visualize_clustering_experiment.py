#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.manifold import MDS
from sklearn.metrics import euclidean_distances
from matplotlib import pyplot as plt
import pickle


dataset = pd.read_excel("./clustering_data.xlsx")

features_clustering = [
    "function_ttr", 
    "egrid_x-", 
    "egrid_o-", 
    "lemma_ttr", 
    "cause_dm", 
    "egrid_s-",
    "avg_imageability",
    "pronoun_noun_ratio",
    "egrid_-x",
    "content_ttr",
    "lexical_overlap",
    "egrid_sx",
    "egrid_xx",
    "egrid_-s",
    "avg_arousal"
]

X = dataset[features_clustering]

scaler = MinMaxScaler()

X_scaled = scaler.fit_transform(X)
similarities = euclidean_distances(X_scaled)
mds = MDS(n_components=2, max_iter=3000, eps=1e-9,
                   dissimilarity="precomputed", n_jobs=1)

pos = mds.fit(similarities).embedding_

# Adding x and y coordinates to dataset
dataset["xcoord"] = pos[:,0]
dataset["ycoord"] = pos[:,1]

class7b = dataset.loc[dataset["cluster_label_nivel"] == "7b"]
class3m = dataset.loc[dataset["cluster_label_nivel"] == "3m"]

colors_dict = {"7b": 'yellow', "3m": 'magenta'}
groups_dict =  {"7b": "7b", "3m": "3m"}
colors = dataset['cluster_label_nivel'].apply(lambda x: colors_dict[x])
classes = dataset['cluster_label_nivel'].apply(lambda x: groups_dict[x])

plt.figure()
for (i, cla) in enumerate(set(classes)):
    xc = [p for (j,p) in enumerate(dataset["xcoord"]) if classes[j]==cla]
    yc = [p for (j,p) in enumerate(dataset["ycoord"]) if classes[j]==cla]
    tx = [p for (j,p) in enumerate(dataset['nivel']) if classes[j] == cla]
    cols = [c for (j,c) in enumerate(colors) if classes[j]==cla]
    plt.scatter(xc,yc,c=cols,label=cla)
    for i, txt in enumerate(tx):
        plt.annotate(txt, (xc[i], yc[i]))

plt.legend(loc=2)
plt.title(u'Visualización clustering textos nivel escolar')
plt.xlabel('Coordenada x (MDS)')
plt.ylabel('Coordenada y (MDS)')
plt.show()

