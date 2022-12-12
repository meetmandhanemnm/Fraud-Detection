# -*- coding: utf-8 -*-
"""DecisionTree.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1c_z3Mscg2TxjKddnrlLL9e-Df8rgDsMa
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

dtr=pd.read_csv('../input/preprocessed/newdf2.csv')
dte=pd.read_csv('../input/preprocessed/newtest.csv')

test=pd.read_csv('../input/its-a-fraud/test.csv')

dtr.drop(['Unnamed: 0'],axis=1,inplace=True)
dte.drop(['Unnamed: 0'],axis=1,inplace=True)

X_train=dtr.drop(['isFraud'],axis=1,inplace=False)
y_train=dtr['isFraud']

X_full=X_train
y_full=y_train

X_test=dte.copy()

"""Using default parameters"""

from sklearn.tree import DecisionTreeClassifier

clf = DecisionTreeClassifier()
clf.fit(X_train,y_train)

output = clf.predict(X_test)

from collections import Counter
Counter(output)

dte['isFraud']=output
neww=dte[['TransactionID','isFraud']]
test = test.merge(neww, how='outer',copy=False, on ='TransactionID' )
output1 = test['isFraud']
output1.columns=['Id','isFraud']
output1=pd.DataFrame(output1)
output1.to_csv('output.csv',index=True,index_label='Id')

"""Using class_weighht="balanced"
"""

clf1 = DecisionTreeClassifier(class_weight="balanced")
clf1.fit(X_train,y_train)

output1 = clf1.predict(X_test)

from collections import Counter
Counter(output1)

dte['isFraud']=output1
neww=dte[['TransactionID','isFraud']]
test = test.merge(neww, how='outer',copy=False, on ='TransactionID' )
output2 = test['isFraud']
output2.columns=['Id','isFraud']
output2=pd.DataFrame(output1)
output2.to_csv('output.csv',index=True,index_label='Id')



from sklearn.model_selection import train_test_split 
from sklearn.metrics import roc_auc_score

x_train,x_test,y_train,y_test = train_test_split(X_train,y_train,test_size=0.33, random_state=42)

max_depth = [3,5,7,9,11,13,15]
max_features = ['auto','sqrt','log2']

for depth in max_depth:
    for feature in max_features:
        print('*******max_depth=',depth,', max_feature=',feature)
        clf = DecisionTreeClassifier(max_depth=depth,max_features=feature)
        clf.fit(x_train,y_train)
        y_train_pred=clf.predict_proba(x_train)
        y_test_pred = clf.predict_proba(x_test)
        print('train auc:',roc_auc_score(y_train,y_train_pred[:,1]))
        print('test auc:',roc_auc_score(y_test,y_test_pred[:,1]))
        print('======================================================')

"""With max_depth=13  max_feature=log2"""

clf1 = DecisionTreeClassifier(max_depth=13,max_features='log2')
clf1.fit(X_full,y_full)

dte.drop('isFraud',axis=1,inplace=True)

y_test1_pred = clf1.predict(dte)

Counter(y_test1_pred)

dte['isFraud']=y_test1_pred
neww=dte[['TransactionID','isFraud']]
test = test.merge(neww, how='outer',copy=False, on ='TransactionID' )
output2 = dte['isFraud']
output2.columns=['Id','isFraud']
output2=pd.DataFrame(output2)
output2.to_csv('output2.csv',index=True,index_label='Id')

"""Score=0.55847"""

clf1 = DecisionTreeClassifier(max_depth=9,max_features='auto')
clf1.fit(X_full,y_full)

dte.drop('isFraud',axis=1,inplace=True)

y_test1_pred = clf1.predict(dte)

Counter(y_test1_pred)

dte['isFraud']=y_test1_pred
neww=dte[['TransactionID','isFraud']]
test = test.merge(neww, how='outer',copy=False, on ='TransactionID' )
output2 = dte['isFraud']
output2.columns=['Id','isFraud']
output2=pd.DataFrame(output2)
output2.to_csv('output3.csv',index=True,index_label='Id')

"""Score=0.6215"""

