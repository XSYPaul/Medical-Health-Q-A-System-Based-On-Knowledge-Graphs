#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 09:42:35 2019

@author: xiongshanyu
"""

import json
import pandas as pd
import py2neo

basic_path = './cleaning_data/cleaning_basic.json'
cause_path = './cleaning_data/cleaning_cause.json'
nursing_path = './cleaning_data/cleaning_nursing.json'
treat_path = './cleaning_data/cleaning_treatment.json'
prevent_path = './cleaning_data/cleaning_prevent.json'
diagnosis_path = './cleaning_data/cleaning_diagnosis.json'

with open(basic_path,'r') as f:
    basic_file = f.readlines()
with open(cause_path,'r') as f:
    cause_file = f.readlines()
with open(nursing_path,'r') as f:
    nursing_file = f.readlines()
with open(treat_path,'r') as f:
    treat_file = f.readlines()
with open(prevent_path,'r') as f:
    prevent_file = f.readlines()
with open(diagnosis_path,'r') as f:
    diagnosis_file = f.readlines()
    
# 分别将这些文件做成dataframe 然后合并
lst = []
for line in cause_file:
    data = json.loads(line)
    lst.append(data)
cause = pd.DataFrame(lst)
# cause.head()
cause = cause[['page_num','cause']]

lst = []
for line in basic_file:
    data = json.loads(line)
    lst.append(data)
basic = pd.DataFrame(lst)

lst = []
for line in nursing_file:
    data = json.loads(line)
    lst.append(data)
nursing = pd.DataFrame(lst)
# nursing.head()
nursing = nursing[['page_num','desc']]

lst = []
for line in prevent_file:
    data = json.loads(line)
    lst.append(data)
prevent = pd.DataFrame(lst)
# prevent.head()
prevent = prevent[['page_num','prevent']]

lst = []
for line in treat_file:
    data = json.loads(line)
    lst.append(data)
treat = pd.DataFrame(lst)
# treat.head()
treat = treat[['page_num','desc','charge']]
treat = treat.drop_duplicates()

lst = []
for line in diagnosis_file:
    data = json.loads(line)
    lst.append(data)
diagnosis = pd.DataFrame(lst)
diagnosis = diagnosis[['page_num','diagnosis']]

df_1 = pd.merge(basic,cause,how = 'left', on = 'page_num')
df_2 = pd.merge(df_1,nursing,how = 'left', on = 'page_num')
df_3 = pd.merge(df_2,prevent,how = 'left', on = 'page_num')
df_4 = pd.merge(df_3,diagnosis,how = 'left', on = 'page_num')
df = pd.merge(df_4,treat,how = 'left', on = 'page_num')

disease_info = []
for i in range(df.shape[0]):
    
    disease = {
        'name':None,
        'description':None,
        'cause':None,
        'prevent':None,
        'nursing':None,
        'diagnosis':None,
        'assurance':None,
        'sick_ratio':None,
        "weak_people":None,
        "infection":None,
        'department':None,
        'treatment':None,
        'cure_period':None,
        'cure_ratio':None,
        'charge':None
    }
#     print(i)
    disease['name'] = df['name'][i]
    disease['description'] = df['description'][i]
    tmp = df['cause'][i] # cause 是一个list，将他们合并
    try:
        disease['cause'] = ''.join(tmp)
    except:
        disease['cause'] = None
    disease['prevent'] = df['prevent'][i]
    disease['nursing'] = df['desc_x'][i]
    disease['diagnosis'] = df['diagnosis'][i]
    disease['assurance'] = df['assurance'][i]
    disease['sick_ratio'] = df['sick_ratio'][i]
    disease['weak_people'] = df['weak_people'][i]
    disease['infection'] = df['infection'][i]
    disease['department'] = df['department'][i]
    disease['treatment'] = df['desc_y'][i]
    disease['cure_period'] = df['cure_period'][i]
    disease['cure_ratio'] = df['cure_ratio'][i]
    disease['charge'] = df['charge'][i]
    
    disease_info.append(disease)
    
# 节点 drug
drug_path = './cleaning_data/cleaning_drug.json'
with open(drug_path,'r') as f:
    drug = f.readlines()
drugs = []
i = 0 
for line in drug:
    data = json.loads(line)
    data_drug = data['drug']
    if data_drug != None:    # 有些疾病没有收集到药品
        for i in data_drug: 
            if len(i)>0:
                drugs.append(i[1])   # 去除厂家

# 节点 food
food_path = './cleaning_data/cleaning_food.json'
with open(food_path,'r') as f:
    food_file = f.readlines()
food = []
# json.loads(food_file[1])
for line in food_file:
    data = json.loads(line)
    food.extend(data['good_food'])
    food.extend(data['bad_food'])
    food.extend(data['recommendation'])
    
# 节点 inspect
inspect_path = './cleaning_data/cleaning_inspect.json'
with open(inspect_path,'r') as f:
    inspect_file = f.readlines()
inspect = []
for line in inspect_file:
    data = json.loads(line)
    inspect.extend(data['item'])
    
# 节点 symptom
symptom_path = './cleaning_data/cleaning_symptom.json'
with open(symptom_path,'r') as f:
    symptom_file = f.readlines()
symptom = []
for line in symptom_file:
    data = json.loads(line)
    symptom.extend(data['symptom'])

# 节点 Department
basic_path = './cleaning_data/cleaning_basic.json'
with open(basic_path,'r') as f:
    basic_file = f.readlines()
department = []
for line in basic_file:
    data = json.loads(line)
    try:
        department.extend(data['department'])
    except:
        a = 1

drugs = set(drugs)
food = set(food)
inspect = set(inspect)
symptom = set(symptom)
department = set(department)


# 得到所有疾病的名字
name = set()
for line in disease_info:
    name.add(line['name'])
all_entities = set(list(drugs) + list(food )+ list(inspect) + list(symptom) + list(department) + list(name) )
with open('all_entities.txt','w') as fw:   # 构建所有的实体
    for item in all_entities:
        fw.write(item+'\n')
with open('disease.txt','w') as fw:   # 疾病实体
    for item in name:
        fw.write(item+'\n')
        
with open('drugs.txt','w') as fw:   # 实体  药
    for item in drugs:
        fw.write(item+'\n')

with open('food.txt','w') as fw:    # 实体  食品
    for item in food:
        fw.write(item+'\n')

with open('inspect.txt','w') as fw:    # 实体  检查
    for item in inspect:
        fw.write(item+'\n')

with open('symptom.txt','w') as fw:    # 实体  症状
    for item in symptom:
        fw.write(item+'\n')

with open('department.txt','w') as fw:    # 实体  科室
    for item in department:
        fw.write(item+'\n')

'''
建立关系
'''
re_comlication = []     # 疾病并发关系
re_symptom = []         #疾病症状关系
re_inspect = []     # 疾病－检查关系
re_department = []   #　科室－科室关系
re_category = []        #　疾病与科室之间的关系
re_not_eat = []    # 疾病－忌吃食物关系    
re_eat =[]      # 疾病－宜吃食物关系
re_drug = []   # 疾病－药品关系

# 疾病并发关系
for line in basic_file:  
    data = json.loads(line)
    for item in data['complication']:
        re_comlication.append([data['name'],item])
        
#疾病症状关系
for line in symptom_file:
    data = json.loads(line)
    for item in data['symptom']:
        re_symptom.append([data['name'],item])

# 疾病－检查科目关系
for line in inspect_file:
    data = json.loads(line)
    for item in data['item']:
        re_inspect.append([data['name'],item])
        
#　科室－科室关系   疾病与科室之间的关系
for line in basic_file:
    data = json.loads(line)
    if data['department']:
        if len(data['department']) == 1:
            re_category.append([data['name'],data['department'][0]])
        
        if len(data['department']) == 2:
            re_department.append([data['department'][0],data['department'][1]])
            re_category.append([data['name'],data['department'][-1]])
            
df = pd.DataFrame(re_department)
df = df.drop_duplicates().reset_index(drop=True)
lst = []
for i in range(df.shape[0]):
    lst.append([df.iloc[i,0],df.iloc[i,1]])
re_department = lst

# 疾病－忌吃食物关系   疾病－宜吃食物关系
for line in food_file:
    data = json.loads(line)
    for good in data['good_food']:
        re_eat.append([data['name'],good])
    for recom in data['recommendation']:
        re_eat.append([data['name'],recom])
    for bad in data['bad_food']:
        re_not_eat.append([data['name'],bad])
        
# 疾病－药品关系
re_drug = []   # 疾病－药品关系
for line in drug:
    data = json.loads(line)
    if data['drug']:
        for item in data['drug']:
            if len(item) > 1:
                re_drug.append([data['name'],item[1]])
            if len(item) == 1:
                re_drug.append([data['name'],item[0]])
                
df = pd.DataFrame(re_drug)
df = df.drop_duplicates().reset_index(drop=True)
lst = []
for i in range(df.shape[0]):
    lst.append([df.iloc[i,0],df.iloc[i,1]])
re_drug = lst


"""
链接数据库创建节点
"""
# 创建节点
def create_node(label, nodes):
    for node_name in nodes:
        node = py2neo.Node(label, name = node_name)
        graph.create(node)
    
    return len(nodes)

def create_relationship(node_1,node_2,edges,rel_type,rel_name):
    set_edges = []
    for edge in edges:
        set_edges.append("===>".join(edge))
    set_edge = set(set_edges)
    for edge in set_edge:
        edge = edge.split('===>')
        p = edge[0]
        q = edge[1]
        query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (node_1,node_2,p,q,rel_type,rel_name)
        
        try:
            graph.run(query)
        except Exception as e:
            print(e)
    
    return 

#############################################################################

graph = py2neo.Graph(host = 'localhost',
                     http_port = 7474, 
                     user = 'neo4j',
                    password = 'admin123')

# 建立以疾病为中心的节点，一个节点有14个属性
for disease in disease_info:
    node = py2neo.Node('Disease',name = disease['name'], description = disease['description'],
                        cause = disease['cause'],prevent = disease['prevent'],
                       nursing = disease['nursing'], diagnosis = disease['diagnosis'],
                       assurance = disease['assurance'],sick_ratio = disease['sick_ratio'],
                       weak_people = disease['weak_people'],infection = disease['infection'],
                       treatment = disease['treatment'],cure_period = disease['cure_period'],
                       cure_ratio = disease['cure_ratio'], charge = disease['charge']
                    )
    graph.create(node)
    
node_drug = create_node('Drug',drugs)
node_food = create_node('Food',food)
node_inspect = create_node('Inspect',inspect)
node_department = create_node('Department',department)
node_symptom = create_node('Symptom',symptom)
    
disease_com = create_relationship('Disease','Disease',re_comlication,'acompany_with','并发症')
disease_sym = create_relationship('Disease','Symptom',re_symptom,'has_symptom','症状')
disease_inspect = create_relationship('Disease','Inspect',re_inspect,'has_inspectation','检查项目')
disease_department = create_relationship('Disease','Department',re_category,'cure_department','就诊科室')
department_department = create_relationship('Department','Department',re_department,'is_part_of','属于')
disease_not_eat = create_relationship('Disease','Food',re_not_eat,'worse_food','忌吃食物')
disease_eat = create_relationship('Disease','Food',re_eat,'better_food','宜吃食物')
disease_drug = create_relationship('Disease','Drug',re_drug,'general_drug','常用药品')

