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
import numpy as np
import matplotlib.pyplot as plt

# Read test set (beware pandas parser throws some errors on some csv, investigate...)
dataset = pd.read_excel("./textos_niveles_escolares_features.xlsx")

# Finally we have a features-label dataset
X = dataset.drop(["id", "nivel", "grupo", "nchar"], axis=1)
#X = dataset[["nchar", "adv_ttr"]]
y = dataset['grupo']

with open("./random_forest_exp.pickle", "rb") as fp:
    rf = pickle.load(fp)

importances = rf.feature_importances_
std = np.std([tree.feature_importances_ for tree in rf.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]

# Print the feature ranking
print("Feature ranking:")

for f in range(X.shape[1]):
    print("%d. feature %s (%f)" % (f + 1, X.columns[indices[f]], importances[indices[f]]))

# Plot the feature importances of the rf
plt.figure()
plt.title("Importancia Relativa de Predictores")
plt.barh(range(X.shape[1]), importances[indices],
       color="r", yerr=std[indices], align="center")
plt.yticks(range(X.shape[1]), X.columns[indices])
plt.ylim([-1, X.shape[1]])
plt.xlabel("Importancia del Predictor")
plt.show()


