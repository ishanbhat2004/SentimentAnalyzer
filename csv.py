# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 13:52:13 2021

@author: ADMIN
"""

import os
import pandas as pd
from selenium import webdriver
#import options
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.firefox.options import Options as Options1
from selenium.common.exceptions import ElementNotInteractableException as EI
from time import sleep

 
WORKING_DIR = os.getcwd()
#def etsy_data_scrapper(headless: bool, browserType: str):
def etsy_data_scrapper(headless : bool, browserType: str):
    df = pd.DataFrame(columns=["review"])
    for i in range(1,121):
        if browserType.lower() == "chrome":
            options = Options()
            options.headless = headless
            browser = webdriver.Chrome(executable_path= r"C:/Webdrivers/chromedriver.exe", chrome_options = options)
        sleep(3)
        
        etsy_url = f"https://www.etsy.com/in-en/c/accessories?ref=pagination&explicit=1&page={i}"
        browser.get(etsy_url)
        print(f"start page:{i}")
        
        products = browser.find_elements_by_class_name("listing-link")
        print(len(products))
        
       # browser.find_elements_by_class_name("listing-link")[0].click()
        
        for prod in products:
            try:
              prod.click()
            except EI as e:
                print(e)
            if(len(browser.window_handles) > 1):
                   browser.switch_to.window(browser.window_handles[1])            
            sleep(3)
            try:
                review0 = browser.find_element_by_id("review-preview-toggle-0")
                df.loc[len(df.index)] = [review0.text.strip()]
            except Exception as e:
                print(e)
            try:
                review1 = browser.find_element_by_id("review-preview-toggle-1")
                df.loc[len(df.index)] = [review1.text.strip()]
            except Exception as e :
                print(e)
            try:
                review2 = browser.find_element_by_id("review-preview-toggle-2")
                df.loc[len(df.index)] = [review2.text.strip()]
            except Exception as e :
                print(e)
            try:
                review3 = browser.find_element_by_id("review-preview-toggle-3")
                df.loc[len(df.index)] = [review3.text.strip()]
            except Exception as e :
                print(e)
                
            sleep(3)
            
            if(len(browser.window_handles)>1):
                parent = browser.window_handles[0]
                chld = browser.window_handles[1]
                browser.switch_to.window(chld)
                browser.close()
                browser.switch_to.window(parent)
                #browser.close()
                
            print(df)
                
            
        print(f"Done page{i}")
        parent = browser.window_handles[0]
        browser.switch_to.window(parent)
        
        for handle in browser.window_handles:
            browser.switch_to.window(handle)
            browser.close()
    df.to_csv("etsy_reviews_main.csv", index = False)
    

etsy_data_scrapper(True, "Chrome")
            
            

                

                

