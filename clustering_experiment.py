#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# En este codigo lo que hago es buscar el mejor modelo para evaluar textos
# dada una nota por experto humano

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.cluster import MeanShift
import pickle

# Read test set (beware pandas parser throws some errors on some csv, investigate...)
dataset = pd.read_excel("./textos_niveles_escolares_features.xlsx")

# Features considered for clustering experiment
features_clustering = [
    "closed_class_words",
    "lemma_ttr",
    "egrid_--",
    "egraph_lc_pacc",
    "egrid_x-",
    "egraph_lc_pu",
    "avg_imageability",
    "function_ttr",
    "pronoun_noun_ratio",
    "egrid_-x",
]

X = dataset[features_clustering]

scaler = MinMaxScaler()

X_scaled = scaler.fit_transform(X)

clusters = KMeans(n_clusters=2, max_iter=1000).fit(X)

dataset["cluster_label"] = clusters.labels_

ms_clusters = MeanShift().fit(X)
print ("Found {} clusters".format(len(set(ms_clusters.labels_))))

writer = pd.ExcelWriter("clustering_data.xlsx")
dataset.to_excel(writer, "hoja1")
writer.save()
