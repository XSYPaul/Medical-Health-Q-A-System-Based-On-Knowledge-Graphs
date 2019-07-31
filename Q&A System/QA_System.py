#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 11:35:13 2019

@author: xiongshanyu
"""

from py2neo import Graph

class QA_System(object):
    def __init__(self):
        self.g = Graph(
            host= '127.0.0.1',
            http_port = 7474,
            user = 'neo4j',
            password='admin123')
        
        print('connect to database successfully...')
        return 
    
    def triple_to_sql(self,triple_lst):
        sql = []
        sql_type = []

        for i in triple_lst:
            entity = i[0]
            relation = i[1]

            if relation == 'disease_description':
                sql.append("MATCH (m:Disease) where m.name = '%s' return m.name, m.description"%entity)

            if relation =='disease_cause':
                sql.append("MATCH (m:Disease) where m.name = '%s' return m.name, m.cause"%entity)

            if relation == 'disease_prevent':
                sql.append("MATCH (m:Disease) where m.name = '%s' return m.name, m.prevent"%entity)

            if relation == 'disease_treatment':
                sql.append("MATCH (m:Disease) where m.name = '%s' return m.name, m.treatment"%entity)

            if relation == 'disease_nursing':
                sql.append("MATCH (m:Disease) where m.name = '%s' return m.name, m.nursing"%entity)

            if relation == 'disease_assurance':
                sql.append("MATCH (m:Disease) where m.name = '%s' return m.name, m.assurance"%entity)

            if relation == 'disease_sickRatio':   # 暂时没有定义此关系
                sql.append("MATCH (m:Disease) where m.name = '%s' return m.name, m.sick_ratio"%entity)

            if relation == 'disease_easyget':
                sql.append("MATCH (m:Disease) where m.name = '%s' return m.name, m.weak_people"%entity)

            if relation == 'disease_infection':
                sql.append("MATCH (m:Disease) where m.name = '%s' return m.name, m.infection"%entity)

            if relation == 'disease_department': 
                sql.append("MATCH (m:Disease)-[r:cure_department]->(n:Department) where m.name = '%s' return m.name, r.name, n.name"%entity)

            if relation == 'disease_cureratio':
                sql.append("MATCH (m:Disease) where m.name = '%s' return m.name, m.cure_ratio"%entity)

            if relation == 'disease_period':
                sql.append("MATCH (m:Disease) where m.name = '%s' return m.name, m.cure_period"%entity)

            if relation =='disease_fee':
                sql.append("MATCH (m:Disease) where m.name = '%s' return m.name, m.charge"%entity)

            if relation == 'disease_symptom':
                sql.append("MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where m.name = '%s' return m.name, r.name, n.name"%entity)

            if relation == 'disease_inspect':
                sql.append("MATCH (m:Disease)-[r:has_inspectation]->(n:Inspect) where m.name = '%s' return m.name, r.name, n.name"%entity)

            if relation == 'disease_goodeat':
                sql.append("MATCH (m:Disease)-[r:better_food]->(n:Food) where m.name = '%s' return m.name, r.name, n.name"%entity)

            if relation == 'disease_badeat':
                sql.append("MATCH (m:Disease)-[r:worse_food]->(n:Food) where m.name = '%s' return m.name, r.name, n.name"%entity)

            if relation == 'disease_drug':
                sql.append("MATCH (m:Disease)-[r:general_drug]->(n:Drug) where m.name = '%s' return m.name, r.name, n.name"%entity)

            if relation == 'disease_disease':   # 需要修改
                sql.append("MATCH (m:Disease)-[r:acompany_with]->(n:Disease) where m.name = '%s' return m.name, r.name, n.name"%entity)
                sql.append("MATCH (m:Disease)-[r:acompany_with]->(n:Disease) where n.name = '%s' return m.name, r.name, n.name"%entity)

            if relation == 'symptom_disease':
                sql.append("MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where n.name = '%s' return m.name, r.name, n.name"%entity)

            if relation == 'drug_disease': 
                sql.append("MATCH (m:Disease)-[r:general_drug]->(n:Drug) where n.name = '%s' return m.name, r.name, n.name"%entity)

            sql_type.append([relation,sql])
            
#            print(sql_type)
        return sql_type
    
    def retrival(self,triple_lst):
        result = []
        for i in range(len(triple_lst)):# 可能存在对个triple
            sql_type = self.triple_to_sql([triple_lst[i]])
            rel_type= sql_type[0][0]  # 得到关系类型   
            query = sql_type[0][1][0]     # 具体的query语句
            answer = self.g.run(query).data()   #得到查询结果
            ans = ''
            try:
                #  根据关系类型套用返回模板
                if rel_type == 'disease_description':
                    desc = [answer[0]['m.description']]
                    name = answer[0]['m.name']
                    ans = '%s,熟悉一下：%s'%(name,desc[0])

                if rel_type == 'disease_cause':    
                    cause = [answer[0]['m.cause']]
                    name = answer[0]['m.name']
                    ans = '造成%s可能的原因有：%s'%(name,cause[0])

                if rel_type == 'disease_prevent':
                    prevent = [answer[0]['m.prevent']]
                    name = answer[0]['m.name']
                    ans = '预防%s的办法有：%s'%(name,prevent[0])

                if rel_type == 'disease_treatment':
                    treatment = [answer[0]['m.treatment']]
                    name = answer[0]['m.name']
                    ans = '%s的治疗方法有：%s'%(name,treatment[0])

                if rel_type == 'disease_nursing':  
                    nursing = [answer[0]['m.nursing']]
                    name = answer[0]['m.name']
                    ans = '%s护理的措施有：%s'%(name,nursing[0])

                if rel_type == 'disease_assurance':
                    assurance = [answer[0]['m.assurance']]
                    name = answer[0]['m.name']
                    if assurance[0][0] == '否':
                        ans = '%s不属于医保疾病'%name
                    else:
                        ans = '%s属于医保疾病'%name

                if rel_type == 'disease_easyget':
                    easyget = [answer[0]['m.weak_people']]
                    name = answer[0]['m.name']
                    ans = '%s的易感人群是：%s'%(name,','.join(i for i in easyget[0]))

                if rel_type == 'disease_infection':
                    infection = [answer[0]['m.infection']]
                    name = answer[0]['m.name']
                    ans = '%s传播途径是：%s'%(name,','.join(i for i in infection[0]))

                if rel_type == 'disease_cureratio':
                    cureratio = [answer[0]['m.cure_ratio']]
                    name = answer[0]['m.name']
                    ans = '%s能治愈的概率是(仅供参考)：%s'%(name,cureratio[0][0])

                if rel_type == 'disease_period':
                    period = [answer[0]['m.cure_period']]
                    name = answer[0]['m.name']
                    ans = '治疗好%s大概需要的周期是：%s'%(name,period[0][0])

                if rel_type == 'disease_fee':
                    fee = [answer[0]['m.charge']]
                    name = answer[0]['m.name']
                    ans = '治疗%s的费用是：%s'%(name,fee[0])

                if rel_type == 'disease_symptom':
                    symptom_lst = []
                    for i in answer:
                        symptom_lst.append(i['n.name'])
                    symptom_lst=list(set(symptom_lst))
                    name = answer[0]['m.name']
                    ans = '%s的症状是：%s'%(name,'；'.join(symptom_lst[:15]))

                if rel_type == 'disease_inspect':
                    inspect_lst = []
                    for i in answer:
                        inspect_lst.append(i['n.name'])
                    inspect_lst=list(set(inspect_lst))
                    name = answer[0]['m.name']
                    ans = '%s可以通过以下方法检查出来：%s'%(name,'；'.join(inspect_lst[:15]))

                if rel_type == 'disease_goodeat':
                    food_lst = []
                    for i in answer:
                        food_lst.append(i['n.name'])
                    food_lst=list(set(food_lst))
                    name = answer[0]['m.name']
                    ans = '%s的推荐食谱是：%s'%(name,'；'.join(food_lst[:15]))

                if rel_type == 'disease_badeat':
                    food_lst = []
                    for i in answer:
                        food_lst.append(i['n.name'])
                    food_lst=list(set(food_lst))
                    name = answer[0]['m.name']
                    ans = '患有%s的患者不要吃以下食物：%s'%(name,'；'.join(food_lst[:15]))

                if rel_type == 'disease_drug':
                    drug_lst = []
                    for i in answer:
                        drug_lst.append(i['n.name'])
                    drug_lst=list(set(drug_lst))
                    name = answer[0]['m.name']
                    ans = '%s的推荐药品是：%s'%(name,'；'.join(drug_lst[:15]))

                if rel_type == 'symptom_disease':
                    disease_lst = []
                    for i in answer:
                        disease_lst.append(i['m.name'])
                    disease_lst=list(set(disease_lst))
                    name = answer[0]['n.name']
                    ans = '%s可能是以下病症引起的：%s'%(name,'；'.join(disease_lst[:20]))

                if rel_type == 'drug_disease':
                    disease_lst = []
                    for i in answer:
                        disease_lst.append(i['m.name'])
                    disease_lst=list(set(disease_lst))
                    name = answer[0]['n.name']
                    ans = '%s可以治疗以下病症：%s'%(name,'；'.join(disease_lst[:24]))

                if rel_type == 'disease_disease':
                    disease_lst = []
                    for i in answer:
                        disease_lst.append(i['n.name'])
                    disease_lst=list(set(disease_lst))
                    name = answer[0]['m.name']
                    ans = '%s可能引起以下疾病：%s'%(name,'；'.join(disease_lst[:24]))

                if rel_type == 'disease_department':
                    department = answer[0]['n.name']
                    name = answer[0]['m.name']
                    ans = '%s的就诊科室是：%s'%(name,department)

                if rel_type == 'disease_sickRatio':
                    sickRatio = answer[0]['m.sick_ratio']
                    name = answer[0]['m.name']
                    ans = '%s的患病率大概为(仅供参考)：%s'%(name,sickRatio[0])

                if len(ans) !=0:
                    result.append(ans)
            except:
                a = 1

        return result

