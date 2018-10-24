#coding=utf-8
'''
try:
    import xml.etree.CElementTree as ET
except:
    import xml.etree.ElementTree as ET

从Python3.3开始ElementTree模块会自动寻找可用的C库来加快速度    
'''
import xml.etree.ElementTree as ET
from dicttoxml import dicttoxml
import jieba.posseg as pseg
import copy
import sys
reload(sys)
sys.setdefaultencoding('utf8')

'''
该函数用于中文段落分句
'''
def cut_sentences(sentence):
    if not isinstance(sentence, unicode):
        sentence = unicode(sentence)
    puns = frozenset(u'。！？')
    tmp = []
    for ch in sentence:
        tmp.append(ch)
        if puns.__contains__(ch):
            yield ''.join(tmp)
            tmp = []
    yield ''.join(tmp)


tree = ET.parse('task1_out.xml')
root = tree.getroot()
infoOutput={}
for i in range(0,5): #遍历每一类主题新闻
	NewsGroup=root[i] #得到某一类主题新闻的所有数据
	news=NewsGroup.getchildren()
	# print len(news)
	for child in news:
		url=child[2].text
		infoOutput[url]=[]

		#处理标题
		title=child[3].text
		sentenceInfo={'sentence':title} #初始化sentenceInfo
		sentenceInfo['jieba']={'nr':[],'ns':[],'nt':[],'nz':[]}
		words =pseg.cut(title) #命名实体识别 @jieba词性标注
		pos=0
		for w in words:
			if w.flag in ('nr' , 'ns' , 'nt' , 'nz'):
				sentenceInfo['jieba'][w.flag].append({'start':pos,'end':pos+len(w.word)})
			pos+=len(w.word)
		infoOutput[url].append(copy.deepcopy(sentenceInfo))

		#处理正文内容
		article=child[4].getchildren()
		for paragraph in article: #遍历一篇新闻正文内容中的段落
			pcontent=paragraph.text
			for scontent in cut_sentences(pcontent): #把段落分成句子遍历
				sentenceInfo={'sentence':scontent} #初始化sentenceInfo
				sentenceInfo['jieba']={'nr':[],'ns':[],'nt':[],'nz':[]}
				words =pseg.cut(scontent) #命名实体识别 @jieba词性标注
				pos=0
				for w in words:
					if w.flag in ('nr' , 'ns' , 'nt' , 'nz'):
						sentenceInfo['jieba'][w.flag].append({'start':pos,'end':pos+len(w.word)})
					pos+=len(w.word)
				infoOutput[url].append(copy.deepcopy(sentenceInfo))

xmlFilePath="task2_out.xml"
xml=dicttoxml(infoOutput)
xmlFile=open(xmlFilePath,"w") 
xmlFile.write(xml.decode())
xmlFile.close()
