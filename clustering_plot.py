#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.manifold import MDS
from sklearn.metrics import euclidean_distances
from matplotlib import pyplot as plt
from collections import OrderedDict
import pickle



# Read test set (beware pandas parser throws some errors on some csv, investigate...)
dataset = pd.read_excel("./clustering_data.xlsx")

# Features considered for clustering experiment
features_clustering = [
    "lemma_ttr",
    "egrid_o-",
    "avg_concreteness",
    "egraph_lc_pu",
    "egrid_-s",
    "closed_class_words",
    "noun_syn_overlap",
]
X = dataset[features_clustering]

scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

cluster_results = pd.DataFrame()
cluster_results["id"] = dataset["id"]
cluster_results["xcoord"] = X_scaled[:, 0]
cluster_results["ycoord"] = X_scaled[:, 1]
cluster_results["nivel"] = dataset["nivel"]
cluster_results["cluster"] = dataset["interpretacion"]

colors = map(lambda x: "m" if x == "7b" else "y", dataset["interpretacion"])

for index, row in cluster_results.iterrows():
    x = row["xcoord"]
    y = row["ycoord"]
    txt = "({}, {})".format(row["id"], row["nivel"])
    cluster = row["cluster"]
    plt.scatter(x, y, c=colors[index], label=cluster)
    plt.annotate(txt, (x, y), fontsize=6)

handles, labels = plt.gca().get_legend_handles_labels()
by_label = OrderedDict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys(), loc=1)

plt.xlabel("Coordenada X")
plt.ylabel("Coordenada Y")
plt.title(u"Clústers Obtenidos")
plt.show()

