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
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import pickle

# Read test set (beware pandas parser throws some errors on some csv, investigate...)
#dataset = pd.read_csv("./trunajod_indices_textos.csv")
dataset = pd.read_excel("./textos_niveles_escolares_features.xlsx")
# Finally we have a features-label dataset
X = dataset.drop(["id", "nivel", "grupo", "nchar"], axis=1)
#X = dataset[["nchar", "adv_ttr"]]
y = dataset['nivel']


##############################
# BASELINE                   #
##############################
from sklearn.dummy import DummyClassifier

parameters = {'strategy': ['stratified', 'most_frequent', 'prior', 'uniform']}
estimator = DummyClassifier()
clf = GridSearchCV(estimator, parameters, cv=5)
clf.fit(X, y)

print clf.best_estimator_
print clf.best_score_

##############################
# Random Forests             #
##############################

# Searching for the best parameters in the model
parameters = {'max_depth': xrange(1, 51), 'min_samples_split': xrange(2, 11)}
#parameters = {'max_depth': xrange(1, 51)}
estimator_rf = RandomForestClassifier()
clf = GridSearchCV(estimator_rf, parameters, cv=5)
clf.fit(X, y)

print clf.best_estimator_
print clf.best_score_

# The chosen model
rf = clf.best_estimator_

with open("random_forest_exp.pickle", "wb") as fp:
    pickle.dump(rf, fp, protocol=pickle.HIGHEST_PROTOCOL)
