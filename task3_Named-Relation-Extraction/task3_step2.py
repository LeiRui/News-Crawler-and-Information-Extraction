#coding:utf8
'''
第二步：将task3_cands.txt数据处理成task3_cands_features.pkl文件，以便于下一步输入模型。 (模型输入特征使用词向量+位置向量。)

参考链接:
[1] https://github.com/buppt/ChineseNRE
'''
import codecs
import sys
import pandas as pd
import numpy as np
from collections import deque  
import pdb

#关系类别
relation2id = {}
with codecs.open('relation2id.txt','r','utf-8') as input_data:
    for line in input_data.readlines():
        relation2id[line.split()[0]] = int(line.split()[1])
    input_data.close()


#为了word2id字向量
#注意必须使用和模型训练时完全一致的word2id生成过程
datas = deque() 
labels = deque()
positionE1 = deque()
positionE2 = deque()
count = [0,0,0,0,0,0,0,0,0,0,0,0]
total_data=0
with codecs.open('train.txt','r','utf-8') as tfc: 
    for lines in tfc:
        line = lines.split()
        if count[relation2id[line[2]]] <1500: #训练数据  这个是不是不能随便改 改了会改变训练模型用到的word2id的长度？是的！！！！
            sentence = []
            index1 = line[3].index(line[0]) #TODO 我直接有记录实体的start end
            position1 = []
            index2 = line[3].index(line[1]) #TODO 我直接有记录实体的start end
            position2 = []

            for i,word in enumerate(line[3]): #遍历句子中的每一个字word
                sentence.append(word)
                position1.append(i-3-index1) #每一个字到第1个实体的距离 为什么要-3？
                position2.append(i-3-index2) #每一个字到第2个实体的距离 为什么要-3？
                i+=1 #为什么这里要加i 不是有enumerate吗
            datas.append(sentence) #把一句话装进队列，不过为什么不直接用line[3]？
            labels.append(relation2id[line[2]]) #关系类别
            positionE1.append(position1) #把这句话每个字产生的到第1个实体的距离向量加到队列中
            positionE2.append(position2) #把这句话每个字产生的到第2个实体的距离向量加到队列中
        count[relation2id[line[2]]]+=1 #更新统计每个关系类型下的句频数
        total_data+=1
        
print total_data,len(datas) #200000 18000

from compiler.ast import flatten
all_words = flatten(datas)
sr_allwords = pd.Series(all_words)
sr_allwords = sr_allwords.value_counts()

set_words = sr_allwords.index
set_ids = range(1, len(set_words)+1)
word2id = pd.Series(set_ids, index=set_words)
id2word = pd.Series(set_words, index=set_ids)

word2id["BLANK"]=len(word2id)+1
word2id["UNKNOW"]=len(word2id)+1
id2word[len(id2word)+1]="BLANK"
id2word[len(id2word)+1]="UNKNOW"
#print "word2id",id2word
print "word2id len",len(word2id)




max_len = 50
def X_padding(words):
    """把 words 转为 id 形式，并自动补全位 max_len 长度。"""
    ids = []
    for i in words:
        if i in word2id:
            ids.append(word2id[i])
        else:
            ids.append(word2id["UNKNOW"])
    if len(ids) >= max_len: 
        return ids[:max_len]
    ids.extend([word2id["BLANK"]]*(max_len-len(ids))) 

    return ids
    
    
def pos(num):
    if num<-40:
        return 0
    if num>=-40 and num<=40:
        return num+40
    if num>40:
        return 80
def position_padding(words):
    words = [pos(i) for i in words]
    if len(words) >= max_len:  
        return words[:max_len]
    words.extend([81]*(max_len-len(words))) 
    return words


datas = deque()
labels = deque()
positionE1 = deque()
positionE2 = deque()
# count = [0,0,0,0,0,0,0,0,0,0,0,0]
with codecs.open('/home/rl/task2/task3_cands.txt','r','utf-8') as tfc:  #记得改路径
    for lines in tfc:
        line = lines.split(" #||# ") #第一步生成txt文件的时候(@task3_step1.py)设置的特殊分隔符
        # if count[relation2id[line[2]]] >1500 and count[relation2id[line[2]]]<=1800: #测试数据
        #if count[relation2id[line[2]]] <=1500:
        sentence = []
        index1 = line[2].index(line[0])
        index2 = line[2].index(line[1])
        # print index1,index2
        position1 = []
        position2 = []

        for i,word in enumerate(line[2]):
            sentence.append(word)
            position1.append(i-3-index1)
            position2.append(i-3-index2)
            i+=1
        datas.append(sentence)
        # labels.append(relation2id[line[2]])
        positionE1.append(position1)
        positionE2.append(position2)

        # count[relation2id[line[2]]]+=1
        
        
df_data = pd.DataFrame({'words': datas,'positionE1':positionE1,'positionE2':positionE2}, index=range(len(datas)))
df_data['words'] = df_data['words'].apply(X_padding)
df_data['positionE1'] = df_data['positionE1'].apply(position_padding)
df_data['positionE2'] = df_data['positionE2'].apply(position_padding)

datas = np.asarray(list(df_data['words'].values))
positionE1 = np.asarray(list(df_data['positionE1'].values))
positionE2 = np.asarray(list(df_data['positionE2'].values))



import pickle
with open('../task3_cands_features.pkl', 'wb') as outp:
	pickle.dump(datas, outp)
	pickle.dump(positionE1, outp)
	pickle.dump(positionE2, outp)
print '** Finished saving the data.'        
        

