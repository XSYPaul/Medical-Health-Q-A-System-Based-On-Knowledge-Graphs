#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 11:35:53 2019

@author: xiongshanyu
"""

import extraction
import QA_System
import rectify

pre_entity = {}
pre_relation = []
Extract = extraction.Entity_Relation()
QA = QA_System.QA_System()
corrector = rectify.rectifier()

while True:
    
    sentence = input("请输入您的问题：")
    question = corrector.final_corrector(sentence)
    if len(question)<5 and ('你好' in question or '您好' in question):   # 判断是不是问候语
        print('您的医疗助理朱皮特很高兴为您服务！')
    else:
        res = Extract.entity_relation(question,pre_entity,pre_relation)
        result = QA.retrival(res)
        if len(result)==0 and len(res) != 0:    # 如果在我们的系统没有找到答案
            print('对不起，您的问题朱皮特明白了，但是我的知识储备有限，请您谅解，您可以换个问题试试')
        if len(result) == 0 and len(res) ==0:
            print('对不起，您的问题朱皮特不是很明白，您可以换个说法试试')
        for answer in result:
            answer = answer.replace('\n','')
            print(answer)
            print('\n')
            
        # 多轮问答 ，改变初始化的实体和关系
        tmp_entity = Extract.medical_entity(question)
        if len(tmp_entity) > 0:     # 如果问题中存在实体将实体保存
            pre_entity = Extract.medical_entity(question)
            if Extract.if_exist_rel(question):    # 如果问题中存在关系，将关系保存
                for i in pre_entity.keys():
                    for j in pre_entity[i]:
                        pre_relation = Extract.relationship(j,question)