# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 19:26:18 2020

@author: Yo Mero
"""

# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 


import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix

def MachineLearning():
    # read in data
    file = "Dataset.csv"
    df = pd.read_csv(file, encoding='latin-1')
    
    # preview dataset
    #print(df.head())
    #print(df.describe())
    
    # view the relationships between variables; color code by species type
    #sns.pairplot(df.drop(labels=['NT'], axis=1), hue='Clasificación')
    
    # split data into training and test sets; set random state to 0 for reproducibility 
    X_train, X_test, y_train, y_test = train_test_split(df[['Polaridad', 'WordCloud', 
                                                            'Subjetividad']],
                                                        df['Clasificacion'], random_state=0)
    
    
    # see how data has been split
    print("\nX_train shape: {}\ny_train shape: {}".format(X_train.shape, y_train.shape))
    print("X_test shape: {}\ny_test shape: {}".format(X_test.shape, y_test.shape))
    
    # initialize the Estimator object
    knn = KNeighborsClassifier(n_neighbors=1)
    
    # fit the model to training set in order to predict classes
    knn.fit(X_train, y_train)
    
    # create a prediction array for our test set
    y_pred = knn.predict(X_test)
    ytest = pd.array(y_test,dtype=str)
    
    ytesto = confusion_matrix(ytest, y_pred, labels=["MP", "P", "NT", "N", "MN"])
    suma = 0
    for i in range(5):
        suma += ytesto[i][i]
        
    # based on the training dataset, our model predicts the following for the test set:
    #print(pd.concat([X_test, y_test, pd.Series(y_pred, name='Predicted', index=X_test.index)], 
    #          ignore_index=False, axis=1))
    
    # what is our score?
    print("\nMatriz de confusión: ")
    print(ytesto)
    print("\nCalificación Global: %0.3f"%(suma/len(y_pred)))
    print("Razón de Error: %0.3f"%(1-(suma/len(y_pred))))
    return suma/len(y_pred),ytesto
    
MachineLearning()
