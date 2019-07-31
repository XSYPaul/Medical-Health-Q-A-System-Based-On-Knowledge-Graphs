#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 11:34:20 2019

@author: xiongshanyu
"""

import ahocorasick
class Entity_Relation():
    def __init__(self):
        with open('disease.txt','r') as f:
            self.disease_file = f.readlines()
        with open('drugs.txt','r') as f:
            self.drug_file = f.readlines()
        with open('food.txt','r') as f:
            self.food_file = f.readlines()
        with open('inspect.txt','r') as f:
            self.inspect_file = f.readlines()
        with open('department.txt','r') as f:
            self.department_file = f.readlines()
        with open('symptom.txt','r') as f:
            self.symptom_file = f.readlines()
        with open('all_entities.txt','r') as f:
            self.entities_file = f.readlines()
        # 装载相应的词典
        self.disease_words = [i.strip() for i in self.disease_file if i.strip()]
        self.drug_words = [i.strip() for i in self.drug_file if i.strip()]
        self.food_words = [i.strip() for i in self.food_file if i.strip()]
        self.department_words = [i.strip() for i in self.department_file if i.strip()]
        self.symptom_words = [i.strip() for i in self.symptom_file if i.strip()]
        self.inspect_words = [i.strip() for i in self.inspect_file if i.strip()]
        self.all_entity = [i.strip() for i in self.entities_file if i.strip()]    # 所有实体的并集
        
        # hash 处理每个词，每个词对应相应的类型
        self.word_dict = {}
        for word in self.all_entity:
            self.word_dict[word] = []      # 用list的原因是避免一个词属于多个类
            if word in self.disease_words:
                self.word_dict[word].append('disease')
            if word in self.drug_words:
                self.word_dict[word].append('drug')
            if word in self.food_words:
                self.word_dict[word].append('food')
            if word in self.department_words:
                self.word_dict[word].append('department')
            if word in self.symptom_words:
                self.word_dict[word].append('symptom')
            if word in self.inspect_words:
                self.word_dict[word].append('inspect')
        # 构造AC自动机，加速问句的处理并且提取出问句中所有实体
        self.actree = ahocorasick.Automaton()
        for index,name in enumerate(self.all_entity):
            self.actree.add_word(name,(index,name))
        self.actree.make_automaton()
        
        # 询问原因
        self.cause_words = ['原因', '成因', '病因', '缘由', '来由', '生病的原因', '病的原因', '为什么', '怎么会', '怎样才', '咋样才', '怎样会', '如何会', '为啥', '为啥会', '为何', '如何才会', '怎么才会', '会导致', '会造成', '会引起', '会引发', '会产生', '会出现']

        # 询问预防
        self.prevent_words = ['预防', '防范', '抵制', '抵御', '防止', '躲避', '逃避', '避开', '免得', '逃开', '避开', '避掉', '躲开', '躲掉', '绕开', '避过', '躲过', '绕过',
                              '怎样才能不', '怎么才能不', '咋样才能不', '咋才能不', '如何才能不',
                              '怎样才不', '怎么才不', '咋样才不','咋才不', '如何才不',
                              '怎样才可以不', '怎么才可以不', '咋样才可以不', '咋才可以不', '如何可以不',
                              '怎样才可不', '怎么才可不', '咋样才可不', '咋才可不', '如何可不']

        #询问医保
        self.assurance_words = ['医保', '报销', '医疗保险', '健康保险', '就医保险', '医疗保障', '就医保障', '健康保障']

        #询问易感人群
        self.weakpeople_words = ['易感人群', '容易感染', '易发人群', '何人', '什么人', '哪些人', '哪类人', '哪种人', '感染', '染上', '得上']

        # 询问传播方式
        self.infection_words = ['传染', '传播', '隔离', '传染方式', '传播方式', '怎么传染', '怎么传播', '会遗传吗']

        # 询问就诊科室
        self.department_words = ['属于什么科', '属于', '应属', '应去', '科室', '部门', '类别', '什么科', '什么科室', '什么部', '什么部门', '什么地方', '什么类别']

        # 询问治疗方式
        self.treatment_words = ['怎么治疗', '如何医治', '怎么医治', '怎么治', '怎么医', '如何治', '医治', '治疗', '医治方式', '治疗方式', '疗法', '咋治', '怎么办', '咋办', '咋治']

        # 询问治愈率
        self.cureRatio_words = ['多大概率能治好', '多大几率能治好', '治好希望大么', '几率', '几成', '比例', '概率', '机会', '可能性', '能治', '可治', '可以治', '可以医','严重吗']

        # 询问周期
        self.period_words = ['周期', '多久', '多长时间', '多少时间', '几天', '几年', '多少天', '多少小时', '几个小时', '多少年', '时间长短']

        # 询问花费
        self.charge_words = ['多少钱', '花费', '花销', '费用', '花多少', '收多少']

        # 询问症状
        self.symptom_words = ['症状', '表征', '现象', '症候', '表现', '样子', '病症', '体现']

        # 询问检查项目
        self.inspect_words = ['检查', '检查项目', '查出', '检查', '测出', '试出', '体检', '体检项目', '身体检查']

        # 询问食物
        self.food_words = ['饮食', '饮用', '饮品', '吃', '多吃', '食', '餐', '伙食', '膳食', '喝', '饮', '菜', '忌口', '宜吃', '宜食', '水果', '补品', '保健品', '食谱', '菜谱', '食用', '食物', '食品', '食疗']
        self.deny_words = ['不', '否', '非', '无', '弗', '勿', '毋', '未', '没', '莫',
                           '没有', '防止', '不再', '不会', '不能', '忌', '禁止', '防止', '难以', '忘记', '忽视', '放弃', '拒绝', '杜绝', '不是',
                           '并未', '并无', '仍未', '难以出现', '切勿', '不要', '不可', '别', '管住', '注意', '小心', '少']

        # 询问吃什么药品
        self.drug_words = ['药', '药品', '药方', '方子', '用药', '胶囊', '口服液', '炎片', '冲剂', '什么药', '哪种药', '用什么药', '吃什么药', '买什么药','偏方']

        # 询问药品用处
        self.cure_words = ['治疗什么', '治啥', '治疗啥', '医治什么', '医治啥', '治愈什么', '治愈啥', '主治啥', '主治什么', '主治症状', '主治症', '主治疾病', '主治病',
                           '有什么用', '有何用', '用处', '用途', '有什么好处', '有什么益处', '有何益处', '用来', '用来做啥', '用来作甚', '需要', '要', '针对什么', '针对啥']

        # 询问并发症
        self.compli_words = ['并发症', '并发', '一起发生', '一并发生', '一起出现', '一并出现', '一同发生', '伴随发生', '一同出现', '同时发生', '同时出现', '一并发作', '一同发作', '伴随发作', '同时发作', '伴随', '共现']

        # 病的基本描述
        self.desc_words = ['介绍', '描述', '简介', '什么病', '是什么', '什么样', '是怎样的', '是怎么样的','区别','辨别']

        # 询问护理
        self.nursing_words = ['护理', '疗养', '照顾', '照料', '照看', '调理', '养护', '注意', '料理']

        # 合并所有的疑问词：
        self.question_words = self.cause_words + self.prevent_words + self.assurance_words + self.weakpeople_words + self.infection_words + self.department_words + \
                        self.treatment_words + self.cureRatio_words + self.period_words + self.charge_words + self.symptom_words + self.inspect_words + \
                        self.food_words + self.drug_words + self.cure_words + self.compli_words + self.desc_words + self.nursing_words
        
        print('model init finished ......')
        
        return 
        
    def matching_key(self,question,keywords):
        for word in keywords:
            if word in question:
                return True

        return False
        
    def medical_entity(self,question):
        entity_tmp = []
        for i in self.actree.iter(question):
            wd = i[1][1]
            entity_tmp.append(wd)
        stop_words = []
        for word_1 in entity_tmp:
            for word_2 in entity_tmp:
                if word_1 in word_2 and word_1 != word_2:
                    stop_words.append(word_1)

        final_words = [i for i in entity_tmp if i not in stop_words]     # 选择长的词作为实体
        final_dict = {i: self.word_dict.get(i) for i in final_words}

        return final_dict
    
    def if_exist_rel(self,question):
        for i in self.question_words:
            if i in question:
                return True
        return False

    def relationship(self,entity,question):    # 问句中的实体会影响到关系的查找
        rel = []

        if entity == 'symptom':    # 如果实体是症状 直接返回 症状到病
    #         if matching_key(question,symptom_words):
    #             rel.append('symptom_disease')
            rel.append('symptom_disease')

        elif entity == 'disease':
            if self.matching_key(question,self.cause_words):  # 病到原因
                rel.append('disease_cause')
            if self.matching_key(question,self.assurance_words):   # 病到医保
                rel.append('disease_assurance')
            if self.matching_key(question,self.weakpeople_words):    # 病到易感人群
                rel.append('disease_easyget')
            if self.matching_key(question,self.infection_words):     # 病到传染
                rel.append('disease_infection')
            if self.matching_key(question,self.department_words):    #  病到科室
                rel.append('disease_department')
            if self.matching_key(question,self.symptom_words):      # 病到症状
                rel.append('disease_symptom')
            if self.matching_key(question,self.inspect_words):      # 病到检查
                rel.append('disease_inspect')
            if self.matching_key(question,self.food_words) and '药' not in question:   # 病到食品
                res = self.matching_key(question,self.deny_words)
                if res:
                    rel.append('disease_badeat')       # 忌吃
                else:
                    rel.append('disease_goodeat')      # 宜吃

            if self.matching_key(question,self.drug_words):       # 病到药
                rel.append('disease_drug')
            if self.matching_key(question,self.treatment_words):   # 病到治疗
                rel.append('disease_treatment')
            if self.matching_key(question,self.cureRatio_words):    # 病到治愈率
                rel.append('disease_cureratio')
            if self.matching_key(question,self.period_words):       # 病到周期
                rel.append('disease_period')
            if self.matching_key(question,self.charge_words):      # 病到花费
                rel.append('disease_fee') 
            if self.matching_key(question,self.compli_words):      # 病到并发症
                rel.append('disease_disease')
            if self.matching_key(question,self.nursing_words):      # 病到护理
                rel.append('disease_nursing')
            if self.matching_key(question,self.desc_words):         # 病到描述
                rel.append('disease_description')
        else:          # 如果实体是药
            if self.matching_key(question,self.cure_words):
                rel.append('drug_disease')

        return rel
    
    def entity_relation(self,question,pre_entity,pre_rel):
    
        final_dict = self.medical_entity(question)
        res = []
        if len(final_dict) > 0 and self.if_exist_rel(question):   # 既有实体也有关系
            for i in final_dict.keys():
                for j in final_dict[i]:
                    rel = self.relationship(j,question)
                    for k in rel:
                        res.append([i,k])
        if len(final_dict) == 0:    # 如果没有实体，就从上继承实体
            for i in pre_entity.keys():
                for j in pre_entity[i]:
                    rel = self.relationship(j,question)
                    for k in rel:
                        res.append([i,k])

        if len(final_dict) >0 and self.if_exist_rel(question)==False:    # 如果有实体但是没有关系，就从上继承关系
            for i in final_dict.keys():
                for j in final_dict[i]:
                    for k in pre_rel:
                        res.append([i,k])
        
        # 实体-关系 去重
        res_unique = []
        for i in res:
            if i not in res_unique:
                res_unique.append(i)
#        print(res_unique)
        return res_unique
        