# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 14:53:13 2021

@author: ADMIN
"""

import pickle


def check_review(reviewText):
    file = open("pickle_model.pkl",'rb')
    recreated_model = pickle.load(file)
    
    vocab_file = open('features.pkl','rb')
    recreated_vocab =  pickle.load(vocab_file)
    
    from sklearn.feature_extraction.text import TfidfVectorizer
    recreated_vect = TfidfVectorizer(vocabulary = recreated_vocab)
    
    reviewText_vectorized = recreated_vect.fit_transform([reviewText])
    if (recreated_model.predict(reviewText_vectorized) == 0 ):
        return "negative review"
    else:
        return "positive review"
    
    
import pandas as pd
df = pd.read_csv("etsy_reviews_main_new.csv")

check_review("good")

import numpy as np
for i in range (0, 28210):
    review = df['review'][i]
    df['Positivity'] = np.where(str(check_review(review))== "positive review", 1, 0)
    
df.to_csv("etsy_reviews_main_seg.csv", index = False)


"""
for i in range(0, len(df['review'])+1):
    review = df['review'][i]
    df['positivity'] = check_review(review)
"""

