# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 11:15:51 2021

@author: Ishan
"""

import pandas as pd
#reading the dataset
df = pd.read_csv('balanced_reviews.csv')

#initial Data Analysis
df.columns.tolist()
df.isnull().any(axis=0)
df.shape
df['overall'].value_counts()
df['reviewText'].head()

#Handling the missing values in the dataset
df.dropna(inplace = True)


#Removing the reviews which are neutral as per client specification
df = df[df['overall'] != 3]

#Adding a new column, which will be then be used for classification
import numpy as np
df['Positivity'] = np.where(df['overall'] > 3, 1, 0)

#Splitting the dataset into features and labels
features = df['reviewText']
labels = df['Positivity']

#Train Test Split
from sklearn.model_selection import train_test_split
features_train,features_test,labels_train,labels_test = train_test_split(features,labels,test_size=0.2,random_state=0)
"""
#Using Count Vectorizer
from sklearn.feature_extraction.text import CountVectorizer
Vect = CountVectorizer().fit(features_train)
len(Vect.get_feature_names()) #code to find the length of the created vocabulary

features_train_vectorize = Vect.transform(features_train)
features_train_vectorize = features_train_vectorize.toarray()"""

#
from sklearn.feature_extraction.text import TfidfVectorizer
Vect = TfidfVectorizer(min_df=5).fit(features_train)

features_train_vectorized = Vect.transform(features_train)


#logistic regression 
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(features_train_vectorized,labels_train)

predictions = model.predict(Vect.transform(features_test))

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(labels_test,predictions)

from sklearn.metrics import accuracy_score
accuracy_score(labels_test,predictions)

import pickle
file = open("pickle_model.pkl","wb")
pickle.dump(model,file)

file_vocab = open("features.pkl","wb")
pickle.dump(Vect.vocabulary_,file_vocab)