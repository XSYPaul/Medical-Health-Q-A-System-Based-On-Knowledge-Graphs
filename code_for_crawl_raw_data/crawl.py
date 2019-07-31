#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 25 16:06:09 2019

@author: xiongshanyu
"""

import random
import time
import data_spyder
import pymongo
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

client = pymongo.MongoClient('localhost',27017)
db = client['disease']

basic = db['basic']     # completed
cause = db['cause']     # completed
prevent = db['prevent']   # completed
complication = db['complication']  # completed
symptom = db['symptom']    # completed
inspect = db['inspect']
diagnosis = db['diagnosis']
treatment = db['treatment']
nursing = db['nursing']
drug = db['drug']      # completed
food = db['food']      # completed

header={'referer':'http://jib.xywy.com/', 
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'Accept':'text/html;q=0.9,*/*;q=0.8',
    'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding':'gzip',
    'Connection':'close',}

def crawl_page(target, page_from, page_to, header):
    
    count = 0
    
    if target == 'basic_info':
        
        for page in range(page_from,page_to):
            url = 'http://jib.xywy.com/il_sii/gaishu/%s.htm'%page
            time.sleep(random.randint(1,3))   # have a break
            data = data_spyder.basic_info(url,header,page)
            count += 1
            basic.insert_one(data)
            print(page)
            
    elif target == 'cause_info':
        for page in range(page_from,page_to):
            url = 'http://jib.xywy.com/il_sii/cause/%s.htm'%page
            time.sleep(random.randint(1,3))   # have a break
            data = data_spyder.cause_info(url,header,page)
            count += 1
            cause.insert_one(data)
            print(page)
            
    elif target == 'prevention_info':
        for page in range(page_from,page_to):
            url = 'http://jib.xywy.com/il_sii/prevent/%s.htm'%page
            time.sleep(random.randint(1,3))   # have a break
            data = data_spyder.prevention_info(url,header,page)
            count += 1
            prevent.insert_one(data)
            print(page)
            
    elif target == 'complication_info':
        for page in range(page_from,page_to):
            url = 'http://jib.xywy.com/il_sii/neopathy/%s.htm'%page
#            time.sleep(random.randint(1,3))   # have a break
            data = data_spyder.complication_info(url,header,page)
            count += 1
            complication.insert_one(data)
            print(page)

    elif target == 'symptom_info':
        for page in range(page_from,page_to):
            url = 'http://jib.xywy.com/il_sii/symptom/%s.htm'%page
#            time.sleep(random.randint(1,3))   # have a break
            data = data_spyder.symptom_info(url,header,page)
            count += 1
            symptom.insert_one(data)
            print(page)
    
    elif target == 'inspection_info':
        for page in range(page_from,page_to):
            url = 'http://jib.xywy.com/il_sii/inspect/%s.htm'%page
            time.sleep(random.randint(1,3))   # have a break
            data = data_spyder.inspection_info(url,header,page)
            count += 1
            inspect.insert_one(data)
            print(page)
    
    elif target == 'diagnosis_info':
        for page in range(page_from,page_to):
            url = 'http://jib.xywy.com/il_sii/diagnosis/%s.htm'%page
            time.sleep(random.randint(1,3))   # have a break
            data = data_spyder.diagnosis_info(url,header,page)
            count += 1
            diagnosis.insert_one(data)
            print(page)
            
    elif target == 'treatment_info':
        for page in range(page_from,page_to):
            url = 'http://jib.xywy.com/il_sii/treat/%s.htm'%page
            time.sleep(random.randint(1,3))   # have a break
            data = data_spyder.treatment_info(url,header,page)
            count += 1
            treatment.insert_one(data)
            print(page)
            
    elif target == 'nursing_info':
        for page in range(page_from,page_to):
            url = 'http://jib.xywy.com/il_sii/nursing/%s.htm'%page
            time.sleep(random.randint(1,3))   # have a break
            data = data_spyder.nursing_info(url,header,page)
            count += 1
            nursing.insert_one(data)
            print(page)
    
    elif target == 'drug_info' :
        for page in range(page_from,page_to):
            url = 'http://jib.xywy.com/il_sii/drug/%s.htm'%page
            time.sleep(random.randint(1,3))
            data = data_spyder.drug_info(url, header, page)
            count += 1
            drug.insert_one(data)
            print(page)
    
    elif target == 'food_info' :
        for page in range(page_from,page_to):
            url = 'http://jib.xywy.com/il_sii/food/%s.htm'%page
            time.sleep(random.randint(1,3))
            data = data_spyder.food_info(url, header, page)
            count += 1
            food.insert_one(data)
            print(page)
            
    else:
        a=1
        
    return count


crawl = crawl_page('symptom_info',4874,11000,header)

