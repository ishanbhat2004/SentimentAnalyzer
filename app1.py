# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 09:39:07 2021

@author: ADMIN
"""

#Imports 
import webbrowser
import pandas as pd
import pickle
import numpy as np

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px

from wordcloud import WordCloud
import base64
import pickle

        
#Creating App Object and Title for the project 
project_name = None
app = dash.Dash(external_stylesheets=[dbc.themes.CYBORG], meta_tags=[{
           'view':'viewport','content':'width-device-width, initial-scale :1'}])


## Defining My Functions ##


#Functions for the UI
def open_browser():
    webbrowser.open_new('http://127.0.0.1:8050/')
    
def word_cloud():
    
    global vocab_new
    file = open("features1.pkl", 'rb') 
    vocab_new = pickle.load(file)
    
    mylist = []
    count = 1
    for i in vocab:
        if(count<=50):
            mylist.append(i)
            count += 1
    
    global df_new
    import pandas as pd
    df_new = pd.DataFrame (mylist, columns = ['words'])
    

    
    

#Function to read the data, pickle files, and create a list of reviews for the dropdown list
def load_model():
    global df
    df = pd.read_csv('etsy_new.csv')
    df['Positivity'] = np.where(df['Positivity'] == 1, 'Positive', 'Negative')

  
    global pickle_model
    file = open("pickle_model.pkl", 'rb') 
    pickle_model = pickle.load(file)

    global vocab
    file = open("features.pkl", 'rb') 
    vocab = pickle.load(file)
    
    global list_reviews
    list_reviews = []
    i = 0
    for review in df['review'].sample(5000):
        if(len(review)<= 40):
            list_reviews.append(review)
            i = i + 1
            if i == 200:
                break
    
    

def check_review(reviewText):
    transformer = TfidfTransformer()
    loaded_vec = CountVectorizer(decode_error="replace",vocabulary=vocab)
    vectorised_review = transformer.fit_transform(loaded_vec.fit_transform([reviewText]))
    return pickle_model.predict(vectorised_review)


def App_Ui():
    load_model()
    main_layout = dbc.Container([
        #1st Row with Heading
        dbc.Row([
               dbc.Col(html.H1(id = "something", children = "Sentiment Analysis with Insights",
                               className = 'text-center  text-warning  mb-4'),
                       width = 12)
            ], justify = "around"),
        
        #2nd row with pie chart and drop-down classifier
        dbc.Row([
            #Col for title and graph
            dbc.Col([ 
                dcc.Dropdown(
                    id = 'my_dropdown',
                    options = [
                        {'label':'Review Classification', 'value': 'Positivity'}
                        ],
                    value = 'Positivity',
                    multi = False,
                    ),
                dcc.Graph(id = "new_fig", figure = {})], width = {"size": 5, "offset":1}),
            
            #Coulmn for the dropdown and classification box
            dbc.Col([
                dcc.Dropdown(
            id = 'my_drop',
            options = [{'label': c,'value': c}
                       for c in (list_reviews)],
            multi = False,
            clearable = False, 
            className="drop-zone-dropdown", ),
            html.H1(id='result', children= None, className = 'text-center  text-warning  mb-4')
            ], width = {'size':5, 'offset': 1}, className = "drop-zone-dropdown", 
                style = {'height': '20px',
                         'font-size':'10px'},),
                
                ], justify = "around"),
        
        #3rd row for image and text-box
        dbc.Row([
            #Column for Wordcloud
            dbc.Col([
                 html.H5("Wordcloud of the frquetly used words", className = 'text-warning'),
                        html.Img(src=app.get_asset_url('WordCloud.png'))], width = {"size":5, "offset":1}),
            
            dbc.Col([
                dcc.Textarea(id='textarea_review', placeholder = 'Enter Your Review Here',
                                     style = {'width':'100%', 'height':100}),
                        html.H3(id = 'result_result', children = None, className = 'text-center  text-warning  mb-4'),
                        ], width = {'size':5, 'offset': 1}, className = "drop-zone-dropdown", 
                        style = {'height': '20px',
                                 'font-size':'10px'}, ),
            ], justify = "around")
        
        ])
    return main_layout

#App Callbacks
    
@app.callback(
    Output(component_id='new_fig', component_property='figure'),[
        Input('my_dropdown', 'value')])
def update_figure(value):
    load_model()
    dff = df
    piechart=px.pie(
        data_frame=dff,
        names = value,
        hole=0.3,
        )
    return (piechart)



#Callback for the Dropdown list
@app.callback(
    Output('result', 'children'),[
        Input('my_drop', 'value')])
def update_dropdown(value):
    response = check_review (value)
    print('response = ', response)

    if (response[0] == 0):
        result1 = 'Negative'
    elif  (response[0] == 1):
        result1 = 'Positive'
    else:
        result1 = 'Unknown'  
    return result1

    

#Callback for the text area
@app.callback(
    Output('result_result', 'children'),[
        Input('textarea_review','value')])
def update_textarea(value):
    response = check_review (value)
    print('response = ', response)

    if (response[0] == 0):
        result1 = 'Negative'
    elif  (response[0] == 1):
        result1 = 'Positive'
    else:
        result1 = 'Unknown'  
    return result1
    
def main():
    open_browser()
    
    global app
    global project_name
    global df
    global pickle_model
    global vocab
    global list_reviews
    
    project_name = "Sentiment Analysis with Insights"
    app.title = project_name
    
    app.layout = App_Ui()
    app.run_server()
    

    
    
#Calling the main function
if __name__ == '__main__':
    main()

    
        
    