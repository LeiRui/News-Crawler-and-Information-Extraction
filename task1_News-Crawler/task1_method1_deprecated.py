# -*- coding: UTF-8 -*- 
'''
⽹络爬⾍程序需要⾃动从新闻⽹站（⽂末给出了⼀些参考新闻源）爬取⼀定数量的新闻，新闻⾄少覆盖5种主
题类型（主题类型⾃选，如可以是政治主题、体育主题、经济主题、科技主题、娱乐主题等），每类主题爬
取的新闻不少于200条，每条新闻要包含原⽹⻚地址、主题、标题、时间和正⽂内容。全部爬取结果保存在
⼀个xml⽂件（格式⾃定义，要合理）中，以供下⼀步实验使⽤。

本次作业基于新浪新闻（https://news.sina.com.cn/），
覆盖五种主题："国内","国际","社会","军事","评论"，
每条新闻抓取八种信息：主题、原⽹⻚地址、标题、时间、正⽂内容、责任编辑、来源、图片。

本代码技术路线：解析真实地址抓取 @https://zhuanlan.zhihu.com/p/31127887

Refs: 
1. https://www.jianshu.com/p/ba6b64ffef45
2. https://blog.csdn.net/God_favored_one/article/details/78828565
3. https://blog.csdn.net/weixin_42243942/article/details/80639040

'''
import json
import requests
from bs4 import BeautifulSoup
from dicttoxml import dicttoxml
'''
需用用到的库有json requests BeautifulSoup dicttoxml
新闻的存储方式采用xml格式进行数据存储
'''
import sys
reload(sys)
sys.setdefaultencoding('utf8')

count=[0,0,0,0,0] #全局变量 对各类主题新闻计数
infoOutput={} #全局变量 最后保存到一个xml文件

def get_html(url, page):
    #进行页面请求时，我们添加捕获异常的处理语句
    try:
        res=requests.get(url.format(page))
        if res.status_code==200: #状态码为200表示请求成功
            return res.text
    except TimeoutError:
        print('请求失败!')
        return None
'''
该函数用来获取的新闻链接
'''
def parser_url(html):
    urls=[]
    jd=json.loads(html)['result']['data'] #使用json进行解析
    for data in jd:
        url=data['url']  #单独分析页面中的一条新闻url
        urls.append(url)
    return urls

def parse_content(topicIndex,urls):
    '''
    采用CSS选择器对网页进行解析
    :param urls:
    :return:
    '''
    for url in urls: #一个url对应一则新闻
        imgs=[] #一篇新闻可能含有多个图片，用scrs来存放
        article=[] #存放一篇新闻
        res=requests.get(url)
        res.encoding='utf-8' #不设置utf-8编码，会出现乱码的情况
        soup=BeautifulSoup(res.text,'html.parser')
        show_author=soup.select('.show_author')[0].text[5:] #将字符串为责任编辑： 去掉
        date=soup.select('.date')[0].text #获取日期
        title = soup.select('.main-title')[0].text #获取新闻标题
        source = soup.select('.source')[0].text #新闻来源
        print("【主题】 "+topicList[topicIndex])
        print("【原网页地址】："+url)
        print("【标题】 "+title)
        print("【时间】 "+date)
        print("【正文内容】 ")
        for i in soup.select('.article p'): #class为article，并且标签为p
            #获取每一个新闻段落，并存放在列表article中
            print(i.text)
            article.append(i.text)
        #打印相关信息
        print("【责任编辑】 "+show_author)
        print("【来源】 "+source)
        print("【图片】")
        for i in soup.select('.img_wrapper img'):
            imgs.append(i.get('src'))
            print(i.get('src'))

        #向全局字典变量infoOutput中添加这条新闻的抓取信息
        global count,infoOutput
        if topicList[topicIndex] not in infoOutput:
            infoOutput[topicList[topicIndex]]=[]
        infoOutput[topicList[topicIndex]].append({
                'url':url, #原网页地址
                'title':title, #标题
                'date':date, #时间
                'article:':article, #正文内容
                'show_author': show_author, #责任编辑
                'source':source, #来源
                'imgs':imgs #图片
            })
        count[topicIndex]+=1
        print("##############"+bytes(count)+"条新闻爬取完成##############")

def save_xml():
    xml=dicttoxml(infoOutput)
    xmlFile=open(xmlFilePath,"w") 
    xmlFile.write(xml.decode())
    xmlFile.close()
    print("===================全部爬取工作完成 结果保存在"+xmlFilePath+"中===================")

def start():
    for i in range(len(topicList)):
        j=0
        while(count[i]<225):  #这里只访问不修改全局变量count
            j+=1
            html=get_html(URLtopicList[i],j) #请求第i类新闻的下一个页面，其中每个页面包含的新闻条数通过参数控制为20，但不能保证每次都有20条
            urls=parser_url(html) 
            parse_content(i, urls) #新闻主题类别通过i传递进去
    save_xml()

if __name__=='__main__':
    #topicList=["国内","国际","社会","军事","评论"]
    topicList=["国内","国际"]
    URLtopicList=["http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page={}",
    "http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gjxw&level==1||=2&show_ext=1&show_all=1&show_num=20&tag=1&format=json&page={}"]
    xmlFilePath="task1_out.xml"
    start()
