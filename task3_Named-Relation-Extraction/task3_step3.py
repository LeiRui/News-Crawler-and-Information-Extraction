#coding:utf8
'''
第三步：将task3_cands_features.pkl输入到提前训练好的分类模型中，模型输出得到实体关系分类结果，并将结果保存到一个xml文件中。

ref:
[1] https://github.com/buppt/ChineseNRE
'''
import numpy as np
import pickle
import sys
import codecs
import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as D
from torch.autograd import Variable
from BiLSTM_ATT import BiLSTM_ATT

import sys
reload(sys)
sys.setdefaultencoding('utf8')

model = torch.load('/home/rl/ChineseNRE/model/model_epoch60.pkl') #TODO 模型要提供一个训练好的吧?

#模型的输入
with open('./data/task3_cands_features.pkl', 'rb') as inp:
    test = pickle.load(inp)
    position1_t = pickle.load(inp)
    position2_t = pickle.load(inp)

#类别id到关系名的映射
id2relation = {}
with codecs.open('./data/people-relation/relation2id.txt','r','utf-8') as input_data:
    for line in input_data.readlines():
        id2relation[int(line.split()[1])] = line.split()[0]
    input_data.close()

# BATCH=32 #注意这个数值必须使用和模型训练时一致的数值  ATTENTION后面改用100batch这边也要改！
BATCH=128 #注意这个数值必须使用和模型训练时一致的数值  ATTENTION后面改用100batch这边也要改！
remains=len(test)%BATCH
test_big = torch.LongTensor(test[:len(test)-remains]) #去掉余数变成batch的整数倍条
position1_t_big = torch.LongTensor(position1_t[:len(test)-remains])
position2_t_big = torch.LongTensor(position2_t[:len(test)-remains])
test_datasets_big = D.TensorDataset(test_big,position1_t_big,position2_t_big)
test_dataloader_big = D.DataLoader(test_datasets_big,BATCH,True,num_workers=2)

resY=[]
for sentence,pos1,pos2 in test_dataloader_big: #这里的加载增量@BATCH=10
    sentence = Variable(sentence) #已转换成字向量
    pos1 = Variable(pos1) #已转换成位置向量
    pos2 = Variable(pos2) #已转换成位置向量
    y = model(sentence,pos1,pos2)
    # print sentence.shape, pos1.shape, pos2.shape,y.shape #(BATCH, 50) (BATCH, 50) (BATCH, 50) (BATCH, 12)，其中12是关系类目数量
    y = np.argmax(y.data.numpy(),axis=1) # 横向在12个关系中取最大的作为分类结果，得到一个numpy.ndarray，维度是1*BATCH
    # print y.shape, y  #这里好像就是所有的sentences的向量N*1的输出结果，而不是一个数
    resY.extend(y.tolist())

# BATCH整数倍之外的余数条输入的处理
test_mod = torch.LongTensor(test[len(test)-BATCH:len(test)]) #反过来尾部一个BATCH长度
position1_t_mod = torch.LongTensor(position1_t[len(test)-BATCH:len(test)])
position2_t_mod = torch.LongTensor(position2_t[len(test)-BATCH:len(test)])
test_datasets_mod = D.TensorDataset(test_mod,position1_t_mod,position2_t_mod)
test_dataloader_mod = D.DataLoader(test_datasets_mod,BATCH,True,num_workers=2)

for sentence,pos1,pos2 in test_dataloader_mod: #这里的加载增量@BATCH=10
    sentence = Variable(sentence) #已转换成字向量
    pos1 = Variable(pos1) 
    pos2 = Variable(pos2) 
    y = model(sentence,pos1,pos2)
    y = np.argmax(y.data.numpy(),axis=1)
    resY.extend(y.tolist()[len(y)-remains:len(y)])  #把对应BATCH整数倍之外的余数条输入的模型输出结果加进来

print len(resY) 

infoOutput={}
# 将结果保存到xml文件
cnt=0
with codecs.open('/home/rl/task2/task3_cands.txt','r','utf-8') as tfc:  #记得改路径
    for lines in tfc:
        # print lines
        line = lines.split(" #||# ") #第一步生成txt文件的时候(@task3_step1.py)设置的特殊分隔符
        entity1=line[0]
        entity2=line[1]
        sentence=line[2]
        url=line[3]
        if url not in infoOutput:
        	infoOutput[url]={} #dict
        if sentence  not in infoOutput[url]:
        	infoOutput[url][sentence]=[] #list
        print len(resY),cnt,resY[cnt],id2relation[resY[cnt]]
        # print cnt
        infoOutput[url][sentence].append({
        	'entity1':entity1,
        	'entity2':entity2,
        	'relation':id2relation[resY[cnt]]
        	# 'relation':"todo"
        	})
        cnt+=1
        # if cnt >= len(resY): #resY因为经过batch整数倍裁剪，所以长度<=lines总数量
        # 	break;
print cnt,len(resY)

from dicttoxml import dicttoxml
xml=dicttoxml(infoOutput)
xmlFile=open("task3_out.xml","w") 
xmlFile.write(xml.decode())
xmlFile.close()
