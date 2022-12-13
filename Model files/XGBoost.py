# -*- coding: utf-8 -*-
"""xgboostt (1).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-FIvdEaXcm5XgBGerZPtHyYT5jnSSYzC
"""

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns 
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, auc, roc_auc_score
from sklearn.model_selection import train_test_split
from collections import Counter


import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))



newdf=pd.read_csv('../input/fraudaa/newdf2.csv')

newtest=pd.read_csv('../input/fraudaa/newtest.csv')

dte=pd.read_csv("../input/its-a-fraud/test.csv")

X_train=newdf.drop(['isFraud','TransactionID'],axis=1,inplace=False)
y_train=newdf['isFraud']

X_test=newtest.copy()

X_test=newtest.drop(['TransactionID'],axis=1,inplace=False)

from sklearn.model_selection import RandomizedSearchCV 
from xgboost import XGBClassifier
xgb = XGBClassifier()


param_grid = {
"learning_rate"    : [0.05,0.1, 0.3] ,
 "max_depth"        : [ 12, 15]
}

rs_clf = RandomizedSearchCV(xgb, param_grid, n_iter=6, n_jobs=-1, verbose=20,cv=2, scoring='roc_auc', random_state=42)

rs_clf.fit(X_train,y_train)

print(rs_clf.best_params_)

from xgboost import XGBClassifier
xgb = XGBClassifier(random_state = 42, n_jobs = -1,max_depth=15,scale_pos_weight=75,learning_rate=0.3)
xgb.fit(X_train, y_train)

y_pred = xgb.predict(X_test)

Counter(y_pred)

newtest['IsFraud']=y_pred

neww=newtest[['TransactionID','IsFraud']]

dte = dte.merge(neww, how='outer',copy=False, on ='TransactionID' )

dte.shape

yp=dte['IsFraud']

Counter(yp)

yp.to_csv('ypred32.csv')

