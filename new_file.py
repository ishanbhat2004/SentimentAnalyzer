# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 11:51:30 2021

@author: Riya
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
    
check_review("I am proud of you")


