#coding=utf-8
'''
第一步：对task2_out.xml信息加以整理，提取出一个task3_cands.txt文件，txt文件中一行表示新闻某一个句子包含的实体对信息，格式为:
[句中实体1的名字，句中实体2的名字，完整句子内容，句子所属的新闻url]。 
'''
import xml.etree.ElementTree as ET
from dicttoxml import dicttoxml
import jieba.posseg as pseg
import copy
import sys
reload(sys)
sys.setdefaultencoding('utf8')

f=open('task3_cands.txt','w')
tree = ET.parse('../task2_Named-Entity-Recognition/task2_out.xml')
root = tree.getroot()
for child in root.getchildren(): #一条新闻
	url=child.attrib['name']
	for sentenceInfo in child.getchildren(): #新闻中的一句话
		sentence=sentenceInfo[1].text
		peopleList=sentenceInfo[0][0] #句子中的人名实体
		num=len(peopleList)
		# print num
		if num>1: #过滤出至少有两个人名的句子，因为后面要研究人与人的关系
			for i in range(0,num-1):
				for j in range(i+1,num):
					# print i,j
					start1=peopleList[i][0].text
					end1=peopleList[i][1].text
					start2=peopleList[j][0].text
					end2=peopleList[j][1].text
					entity1=sentence[int(start1):int(end1)]
					entity2=sentence[int(start2):int(end2)]
					if entity1==entity2:
						continue  #一句话里同一个人名出现两次及以上，不考虑它们之间的关系
					f.write(entity1+" #||# "+entity2+" #||# "+sentence+" #||# "+url+"\n")		
f.close()
