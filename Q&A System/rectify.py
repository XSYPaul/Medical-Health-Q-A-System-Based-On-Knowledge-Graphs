from pypinyin import pinyin, lazy_pinyin, Style, load_phrases_dict, load_single_dict
import numpy as np
from functools import cmp_to_key
import pkuseg
from functools import cmp_to_key
import math
class rectifier:
    def __init__(self):
        self.W = self.dictionary()
    def rotate_one(self,st):
        if len(st)<=1:
            return [st]
        strs = []
        strs.append(st)
        for i in range(len(st)-1):
            tmp = [x for x in st]
            tmp[i],tmp[i+1] = tmp[i+1],tmp[i]
            strs.append(''.join(tmp))
        return strs

    def search_firstletter(self,st):
        pinyin_firstletter =  ''.join(lazy_pinyin(st,Style.FIRST_LETTER))
        pinyin_firstletter = ''.join([x for x in pinyin_firstletter if x.isalpha()])
        l = len(pinyin_firstletter)
        candidates = []
        start = 0
        end = len(self.W)-1
        middle = (start+end)//2
        while(start<=end):
            if l<int(self.W[middle,3]):
                end = middle-1
            elif l>int(self.W[middle,3]):
                start = middle+1
            elif pinyin_firstletter<self.W[middle,1]:
                end = middle-1
            elif pinyin_firstletter>self.W[middle,1]:
                start = middle+1
            else:
                candidates.append(self.W[middle,:])
                for x in range(middle+1,len(self.W)):
                    if self.W[x,1]==pinyin_firstletter:
                        candidates.append(self.W[x,:])
                    else:
                        break
                for x in range(middle-1,0,-1):
                    if self.W[x,1]==pinyin_firstletter:
                        candidates.append(self.W[x,:])
                    else:
                        break
                break
            middle = (start+end)//2
        return candidates

    def pinyin_distence(self,p1,p2):#p1是正确拼音，p2是待纠正
        n,m = len(p1),len(p2)
        dp = np.zeros((n+1,m+1))#arr[i,j]表示，p1[:i]与p2[:j]最小修改
        dp[0,:] = np.array(range(m+1))
        dp[:,0] = np.array(range(n+1))
        for i in range(1,n+1):
            for j in range(1,m+1):
                tmp = 0
                if p1[i-1] != p2[j-1]:
                    tmp = 1
                dp[i,j] = min(dp[i-1,j]+1,dp[i,j-1]+1,dp[i-1,j-1]+tmp)
        return dp[n,m]

    def mycmp(self,a,b):
        if int(a[-1])!=int(b[-1]):
            return int(a[-1])-int(b[-1])
        else:
            if a[1]>b[1]:
                return 1
            else:
                return -1

    def dictionary(self):
        word_disease=np.loadtxt('disease.txt',dtype=np.str)
        word_drug=np.loadtxt('drugs.txt',dtype=np.str)
        word_check=np.loadtxt('inspect.txt',delimiter='\t',dtype=np.str)
        word_department=np.loadtxt('department.txt',dtype=np.str)
        word_food=np.loadtxt('food.txt',dtype=np.str)
        word_symptom=np.loadtxt('symptom.txt',dtype=np.str)
        words = np.r_[word_disease,word_drug,word_check,word_department,word_food,word_symptom]
        pinyin_firstletter = []
        pinyin_all = []
        lengths = []
        for w in words:
            p1 = lazy_pinyin(w,Style.FIRST_LETTER)
            p1 = ''.join([x for x in p1 if x.isalpha()])
            pinyin_firstletter.append(p1)
            length = len(p1)
            lengths.append(length)
            p2 = ''.join(lazy_pinyin(w))
            pinyin_all.append(p2)
        pinyin_firstletter = np.array(pinyin_firstletter).reshape(words.shape)
        pinyin_all = np.array(pinyin_all).reshape(words.shape)
        lengths = np.array(lengths).reshape(words.shape)
        words = np.c_[words,pinyin_firstletter,pinyin_all,lengths]
        words = np.array(sorted(words,key=cmp_to_key(self.mycmp)))
        return words

    def score(self,candidates,s,base=0,min_diff=10000):
        if len(candidates)==0:
            return None
        candidate = None
        pinyin = ''.join(lazy_pinyin(s))
        for c in candidates:
            diff=base
            if len(c[0])!=len(s):
                continue
            for i in range(len(c[0])):
                if c[0][i]!=s[i]:
                    diff+=1
            if diff!=base:
                diff+=self.pinyin_distence(c[2],pinyin)
            if diff<min_diff:
                min_diff=diff
                candidate = c[0]
        return candidate,min_diff

    def final_candidate(self,s):
        if(len(s)<=1):
            return None,10000
        strs = self.rotate_one(s)
        i=0
        min_diff=10000
        final_candidate = None
        for s in strs:
            candidates=self.search_firstletter(s)
            if len(candidates)<=0:
                i+=1
                continue
            base=0
            if(i!=0):
                base=1
            candidate,min_diff = self.score(candidates,s,base,min_diff)
            if candidate!=None:
                final_candidate = candidate
        return final_candidate,min_diff

    def final_corrector(self,sentence):
        #pe = pkuseg.pkuseg()
        #seg_list = pe.cut(sentence)
        word_list = sentence
        max_len = 10
        judge = False
        substitutes = []
        l = len(word_list)
        for i in range(l):
            for j in range(i,l):
                s = ''.join(word_list[i:j+1])
                if len(s)>max_len:
                    break
                else:
                    fc = self.final_candidate(s)
                    if fc[0]!=None and fc[1]<=1.5*math.log(len(fc[0])):
                        substitutes.append((i,j,fc[0],fc[1]))
        final_sub = []
        for sub in substitutes:
            judge = True
            for tmp in substitutes:
                if tmp[0]>=sub[0] and tmp[1]<=sub[1]:
                    pass
                elif tmp[1]<sub[0] or tmp[0]>sub[1]:
                    pass
                else:
                    judge = False
            if judge:
                final_sub.append(sub)
        amend_sentence=''
        i=0
        j=0
        while i < len(word_list):
            if j>=len(final_sub) or i!=final_sub[j][0]:
                amend_sentence+=word_list[i]
            else:
                amend_sentence+=final_sub[j][2]
                i=final_sub[j][1]
                j+=1
            i+=1
        return amend_sentence
