#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# En este codigo lo que hago es buscar el mejor modelo para evaluar textos
# dada una nota por experto humano

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import SpectralClustering
import pickle

# Read test set (beware pandas parser throws some errors on some csv, investigate...)
dataset = pd.read_csv("./trunajod_indices_textos.csv")

# Features considered for clustering experiment
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

clusters = SpectralClustering(n_clusters=2).fit(X)

dataset["cluster_label"] = clusters.labels_

writer = pd.ExcelWriter("spectral_clustering_data.xlsx")
dataset.to_excel(writer, "hoja1")
writer.save()
