# -*- coding: utf-8 -*-
"""RandomForest.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mKEn5b1YRktNeQsiUxz5aODpuBSEaO21
"""

# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

df2=pd.read_csv("../input/fraudaa/newdf2.csv")

ntese=pd.read_csv("../input/fraudaa/newtest.csv")
dte=pd.read_csv('../input/its-a-fraud/test.csv')

df2.drop(['Unnamed: 0'],axis=1,inplace=True)
ntese.drop(['Unnamed: 0'],axis=1,inplace=True)

X_test=ntese.copy()

#df2.drop(['TransactionID'],axis=1,inplace=True)
X_test.drop(['TransactionID'],axis=1,inplace=True)

X=df2.drop(['isFraud'],axis=1,inplace=False)
y=df2['isFraud']

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

#first try with the default paramter

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score

clf = RandomForestClassifier()
clf.fit(X_train,y_train)
y_trainpred=clf.predict_proba(X_train)
y_testpred = clf.predict_proba(X_test)

print('train auc with default parameter:',roc_auc_score(y_train,y_trainpred[:,1]))
print('cv auc with default parameter:',roc_auc_score(y_test,y_testpred[:,1]))

est=[500,700,900,1000]
dep=[3,5,7,9,11,13]
for i in est:
    for j in dep:
        print('n_estimator_val:',i,'depth_val:',j)
        clf = RandomForestClassifier(n_estimators=i,max_depth=j,class_weight='balanced',n_jobs=-1)
        clf.fit(X_train,y_train)
        y_trainpred=clf.predict_proba(X_train)
        y_testpred = clf.predict_proba(X_test)
        print('train:',roc_auc_score(y_train,y_trainpred[:,1]))
        print('test:',roc_auc_score(y_test,y_testpred[:,1]))
        print('==========================')

from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(n_estimators=1000,max_depth=13,class_weight='balanced',n_jobs=-1)
rf.fit(X,y)

X_test.shape

ypred=rf.predict(X_test)

from collections import Counter

Counter(ypred)

ntese['IsFraud']=ypred

neww=ntese[['TransactionID','IsFraud']]

dte = dte.merge(neww, how='outer',copy=False, on ='TransactionID' )

dte['IsFraud']

y_predd=dte['IsFraud']

Counter(y_predd)

y_predd.to_csv('y_predRF.csv')

output = pd.DataFrame({

"isFraud": y_predd
})

output.to_csv('my_submission.csv', index=False)
print("Your submission was successfully saved!")