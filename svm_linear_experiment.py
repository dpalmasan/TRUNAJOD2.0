#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# En este codigo lo que hago es buscar el mejor modelo para evaluar textos
# dada una nota por experto humano

from sklearn.metrics.pairwise import linear_kernel
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
import pickle

# Read test set (beware pandas parser throws some errors on some csv, investigate...)
dataset = pd.read_csv("./trunajod_indices_textos.csv")

# Finally we have a features-label dataset
X = dataset.drop(["id", "nivel"], axis=1)
y = dataset['nivel']

scaler = MinMaxScaler()

X_scaled = scaler.fit_transform(X)

##############################
# SVM with linear kernel     #
##############################

estimator_svm = svm.SVC()

# Searching for the best parameters in the model
parameters = {'kernel': ('linear',), 'C': [0.1, 0.5, 1, 5, 10, 50, 100]}
clf = GridSearchCV(estimator_svm, parameters, cv=5)
clf.fit(X_scaled, y)

print clf.best_estimator_
print clf.best_score_

# The chosen model
svc = clf.best_estimator_
