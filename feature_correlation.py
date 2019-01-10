#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# En este codigo lo que hago es buscar el mejor modelo para evaluar textos
# dada una nota por experto humano

import pandas as pd
from sklearn.feature_selection import SelectFromModel
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline

# Read test set (beware pandas parser throws some errors on some csv, investigate...)
dataset = pd.read_csv("./trunajod_indices_textos.csv")

# Finally we have a features-label dataset
X = dataset.drop(["id", "nivel"], axis=1)
y = dataset['nivel']

clf = Pipeline([
  ('feature_selection', SelectFromModel(LinearSVC(penalty="l1", loss="l2", dual=False))),
  ('classification', RandomForestClassifier())
])

clf.fit(X, y)
print clf.score(X,y)

rf = RandomForestClassifier()
rf.fit(X,y)
print rf.score(X,y)

