#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 25 09:09:46 2019

@author: xiongshanyu
"""

from bs4 import BeautifulSoup
import requests

def basic_info(url,header,page_num):
    basic = {                      # use dictionary to store a disease
            "page_num": -1,
            "name": None,
            "description":None,
            "assurance":None,
            "sick_ratio":None,
            "person":None,
            "infection":None,
            "complication":None,
            "department":None,
            "treatment":None,
            "period":None,
            "cure_ratio":None,
            "drug":None,
            "price":None,
        }
    try:
        web_data = requests.get(url,headers = header)    
        soup = BeautifulSoup(web_data.text,'lxml')  # parsing webpage
        name = soup.select('div.jib-articl-con.jib-lh-articl > strong')   # get disease name
        description = soup.select('div.jib-articl-con.jib-lh-articl > p')   # disease description
        basic_info = soup.select('.mt20 .txt-right')     # disease berif information
        judge = soup.select('.mt20 .txt-left')    # tag for berif information



        if len(name[0].get_text()[:-5])>0:    # if this webpage is null
            basic['page_num'] = page_num
            basic['name'] = name[0].get_text()[:-5]        # disease name 
            basic['description'] = description[0].get_text().strip()     # disease description 
            for i in range(len(judge)):     # according to tag, place info to certain position
                if judge[i].get_text().strip()[:-1] == '医保疾病':
                    basic['assurance'] = [basic_info[i].get_text().strip().split()]
                elif judge[i].get_text().strip()[:-1] == '患病比例':
                    basic['sick_ratio'] = [basic_info[i].get_text().strip().split()]
                elif judge[i].get_text().strip()[:-1] == '易感人群':
                    basic['person'] = [basic_info[i].get_text().strip().split()]
                elif judge[i].get_text().strip()[:-1] == '传染方式':
                    basic['infection'] = [basic_info[i].get_text().strip().split()]
                elif judge[i].get_text().strip()[:-1] == '并发症':
                    basic['complication'] = [basic_info[i].get_text().strip().split()]
                elif judge[i].get_text().strip()[:-1] == '就诊科室':
                    basic['department'] = [basic_info[i].get_text().strip().split()]
                elif judge[i].get_text().strip()[:-1] == '治疗方式':
                    basic['treatment'] = [basic_info[i].get_text().strip().split()]
                elif judge[i].get_text().strip()[:-1] == '治疗周期':
                    basic['period'] = [basic_info[i].get_text().strip().split()]
                elif judge[i].get_text().strip()[:-1] == '治愈率':
                    basic['cure_ratio'] = [basic_info[i].get_text().strip().split()]
                elif judge[i].get_text().strip()[:-1] == '常用药品':
                    basic['drug'] = [basic_info[i].get_text()]
                elif judge[i].get_text().strip()[:-1] == '治疗费用':
                    basic['price'] = [basic_info[i].get_text().strip().split()]
                else:
                    a = 1
    except:
        a = 2
        

    return basic


def cause_info (url , header,page_num):   
    cause = {             #initialize dictionary
        'page_num':-1,    
        'name': None,
        'cause': None
    }
    try:
        web_data = requests.get(url,headers = header)
        soup = BeautifulSoup(web_data.text,'lxml')
        info = soup.select ('div.jib-articl.fr.f14.jib-lh-articl') 
        name = soup.select('div.jib-articl.fr.f14.jib-lh-articl > strong')[0].get_text().strip()[0:-2]    # get disease name

        if len(name) > 0:   # if this is a null webpage
            cause['page_num'] = page_num
            cause['name'] = name
            cause['cause'] = [info[0].get_text().strip().split()[1:]]
    except:
        a = 1
        
    return cause


def prevention_info (url,header,page_num):
    prevention = {            # initialize prevention dictionary
        'page_num':-1,
        'name': None,
        'prevention': None
    }
    try:
        
        web_data = requests.get(url,headers = header)
        soup = BeautifulSoup(web_data.text,'lxml')
        info = soup.select ('div.jib-articl.fr.f14.jib-lh-articl')
        name = soup.select('div.jib-articl.fr.f14.jib-lh-articl > strong')[0].get_text().strip()[0:-2]   #get disease name

        if len(name) > 0:           # if this is a null webpage
            prevention['page_num'] = page_num
            prevention['name'] = name
            prevention['prevention'] = info[0].get_text().strip().split()[1:]
    except:
        a = 1
        
    return prevention


def complication_info(url,header,page_num):
    comp = {                   # initialize complication dictionary
        'page_num': -1,
        'name':None,
        'complication':None,
        'description':None
    }
    try:
        
        web_data = requests.get(url,headers = header)
        soup = BeautifulSoup(web_data.text,'lxml')
        name = soup.select('div.jib-articl.fr.f14.jib-lh-articl > strong')[0].get_text().strip()[0:-3]  #get disease name

        if len(name) > 0 :       # if this is a null page 
            comp['page_num'] = page_num
            comp['name'] = name
            # get complication and split each complication by ','
            comp['complication'] = soup.select('div.jib-articl.fr.f14.jib-lh-articl > span')[0].get_text(',').split()
            description = soup.select('div.jib-articl.fr.f14.jib-lh-articl > p')
            tmp = 'header'   # use to initialize tmp 
            for i in range(len(description)):           # merge all description
                tmp = tmp+" "+ description[i].get_text().strip()
            comp['description'] = tmp[7:]       # fill description and remove header
    except:
        a = 1 
        
        
    return comp


def symptom_info(url,header,page_num):
    symptom = {                   # initialize complication dictionary
        'page_num': -1,
        'name':None,
        'symptom':None,
        'description':None
    }
    try:
        
        web_data = requests.get(url,headers = header)
        soup = BeautifulSoup(web_data.text,'lxml')
        name = soup.select('div.jib-articl.fr.f14.jib-lh-articl > strong')[0].get_text().strip()[0:-2]  #get disease name

        if len(name) > 0 :       # if this is a null page 
            symptom['page_num'] = page_num
            symptom['name'] = name
            # get symptom and split it by ','
            symptom['symptom'] = [soup.select('div.jib-articl.fr.f14.jib-lh-articl > span')[0].get_text().split()]
            description = soup.select('div.jib-articl.fr.f14.jib-lh-articl > p')
            tmp = 'header'   # use to initialize tmp 
            for i in range(len(description)):           # merge all description
                tmp = tmp+" "+ description[i].get_text().strip()
            symptom['description'] = tmp[7:]       # fill description and remove header
    except:
        a = 1
        
        
    return symptom


def inspection_info(url,header,page_num):
    inspection = {                   # initialize inspection dictionary
        'page_num': -1,
        'name':None,
        'item':None,
        'description':None
    }
    try:
        
        web_data = requests.get(url,headers = header)
        soup = BeautifulSoup(web_data.text,'lxml')
        name = soup.select('div.jib-articl.fr.f14.jib-lh-articl > strong')[0].get_text().strip()[0:-3]  #get disease name

        if len(name) > 0 :       # if this is a null page 
            inspection['page_num'] = page_num
            inspection['name'] = name
            # get specific check item and split it by ','
            item = soup.select('li.check-item')
            lst = []
            for i in item:
                lst.append(i.get_text().strip())
            inspection['item'] = [lst[1:]]
            description = soup.select('div.jib-articl.fr.f14.jib-lh-articl > p')
            tmp = 'header'   # use to initialize tmp 
            for i in range(len(description)):           # merge all description
                tmp = tmp+" "+ description[i].get_text().strip()
            inspection['description'] = tmp[7:]       # fill description and remove header
    except:
        a = 1 
        
    return inspection


def diagnosis_info(url,header,page_num):
    diagnosis = {                   # initialize diagnosis dictionary
        'page_num': -1,
        'name':None,
        'diagnosis':None,
        'judge':None
    }
    try:
        
        web_data = requests.get(url,headers = header)
        soup = BeautifulSoup(web_data.text,'lxml')
        name = soup.select('div.jib-articl.fr.f14.jib-lh-articl > strong')[0].get_text().strip()[0:-4]  #get disease name

        if len(name) > 0 :       # if this is a null page 
            diagnosis['page_num'] = page_num
            diagnosis['name'] = name
            lst_diag = []    # store diagnosis info 
            lst_judge = []    # store judge info
            flag = 1         # if append all diagnosis info
            content = soup.select('div.jib-articl.fr.f14.jib-lh-articl > p')
            for i in content:
                tmp = i.get_text().strip()
                if tmp != '鉴别诊断' and flag == 1:
                    lst_diag.append(tmp)
                else:
                    flag = 0
                    lst_judge.append(tmp)
            diagnosis['diagnosis'] = [lst_diag[1:]]
            diagnosis['judge'] = [lst_judge[1:]]
    except:
        a = 1 
        
    return diagnosis

def treatment_info(url, header, page_num):
    treatment = {
        "page_num":-1,
        "name":None,
        "department":None,
        "approach":None,
        "period":None,
        "sick_ratio":None,
        "drug":None,
        "charge":None,
        "description": None
    }
    
    try:
        
        web_data = requests.get(url,headers = header)
        soup = BeautifulSoup(web_data.text,'lxml')
        name = soup.select('div.jib-articl.fr.f14 > strong')[0].get_text().strip()[:-2] #get disease name

        if len(name) > 0:
            treatment['page_num'] = page_num
            treatment['name'] = name
            left = soup.select('.mt20 .txt-left')    # get tag 
            right = soup.select('.mt20 .txt-right')   # get specific info 
            for i in range(len(left)):                 # according to tag , fill specific info
                if left[i].get_text().strip()[:-1] == '就诊科室':
                    treatment['department'] = [right[i].get_text().strip().split()]
                elif left[i].get_text().strip()[:-1] == '治疗方式':
                    treatment['approach'] = [right[i].get_text().strip().split()]
                elif left[i].get_text().strip()[:-1] == '治疗周期':
                    treatment['period'] = [right[i].get_text().strip().split()]
                elif left[i].get_text().strip()[:-1] == '治愈率':
                    treatment['sick_ratio'] = [right[i].get_text().strip().split()]
                elif left[i].get_text().strip()[:-1] == '常用药品':
                    treatment['drug'] = [right[i].get_text().strip().split()]
                elif left[i].get_text().strip()[:-1] == '治疗费用':
                    treatment['charge'] = [right[i].get_text().strip()]
                else:
                    a = 1 
                
            # get specific description
            description = soup.select('div.jib-lh-articl > p')
            tmp = 'header'   # use to initialize tmp 
            for i in range(len(description)):           # merge all description
                tmp = tmp+" "+ description[i].get_text().strip()
            treatment['description'] = tmp[7:]       # fill description and remove header
    except:
        a = 1
        
    
    return treatment


def nursing_info(url, header, page_num):
    nursing = {
        "page_num":-1,
        "name": None,
        "description": None
    }
    try:
        web_data = requests.get(url,headers = header)
        soup = BeautifulSoup(web_data.text,'lxml')        
        name = soup.select('div.jib-articl.fr.f14.jib-lh-articl > strong')[0].get_text().strip()[0:-2]
        if len(name) > 0:
            nursing['page_num'] = page_num 
            nursing['name'] = name
            description = soup.select('div.jib-articl.fr.f14.jib-lh-articl > p')
            tmp = 'header'   # use to initialize tmp 
            for i in range(len(description)):           # merge all description
                tmp = tmp+" "+ description[i].get_text().strip()
                nursing['description'] = tmp[7:]       # fill description and remove header
    except:
        a = 1
        
    return nursing


def drug_info(url, header, page_num):
    drug = {
        "page_num":-1,
        "name": None,
        "drug":None
    }
    try:
        web_data = requests.get(url,headers = header)    
        soup = BeautifulSoup(web_data.text,'lxml')  # parsing webpage
        name = soup.select('div.wrap.mt5 > div')[0].get_text()
        if len(name) > 0:
            drug['page_num'] = page_num
            drug['name'] = name
            drugs = soup.select(' div.fl.drug-pic-rec.mr30 > p > a')
            tmp = 'header'   # use to initialize tmp 
            for i in range(len(drugs)):           # merge all description
                tmp = tmp+","+ drugs[i].get_text().strip()
                drug['drug'] = [tmp[7:]]       # fill description and remove header
    except:
        a = 1
    
    return drug

def food_info(url, header, page_num):
    food = {
        'page_num': -1,
        "name": None,
        "food":None,
        "good":None,
        "good_food": None,
        "bad":None,
        "bad_food":None,
        "recommendation":None
    }
    try:
        web_data = requests.get(url,headers = header)
        soup = BeautifulSoup(web_data.text, 'lxml')
        name = soup.select(' .wrap.mt5 > div')[0].get_text().strip()
        
        if len(name) > 0:
            food['page_num'] = page_num
            food['name'] = name
            info = soup.select('.panels > .diet-item')
            food['food'] = soup.select('.panels > .diet-item')[0].get_text().strip()
            food['good'] = soup.select('.panels > .diet-item')[1].select('.diet-good-txt')[0].get_text().strip()
            good_food = []
            specific_good = soup.select('.panels > .diet-item')[1].select('.diet-img p')
            for i in range(len(specific_good)):
                tmp = soup.select('.panels > .diet-item')[1].select('.diet-img p')[i].get_text().strip()
                good_food.append(tmp)
            food['good_food'] = [good_food]

            food['bad'] = soup.select('.panels > .diet-item')[2].select('.diet-good-txt')[0].get_text().strip()
            bad_food = []
            specific_bad = soup.select('.panels > .diet-item')[2].select('.diet-img p')
            for i in range(len(specific_bad)):
                tmp = soup.select('.panels > .diet-item')[2].select('.diet-img p')[i].get_text().strip()
                bad_food.append(tmp)
            food['bad_food'] = [bad_food]
            
            recommendation_food = []
            specific_recom = soup.select('.panels > .diet-item')[3].select('.diet-img p')
            for i in range(len(specific_recom)):
                tmp = soup.select('.panels > .diet-item')[3].select('.diet-img p')[i].get_text().strip()
                recommendation_food.append(tmp)
            food['recommendation'] = [recommendation_food]
            
    except:
        a=1
    
    return food
