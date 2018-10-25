# -*- coding: UTF-8 -*- 
'''
任务描述：
⽹络爬⾍程序需要⾃动从新闻⽹站（⽂末给出了⼀些参考新闻源）爬取⼀定数量的新闻，新闻⾄少覆盖5种主
题类型（主题类型⾃选，如可以是政治主题、体育主题、经济主题、科技主题、娱乐主题等），每类主题爬
取的新闻不少于200条，每条新闻要包含原⽹⻚地址、主题、标题、时间和正⽂内容。全部爬取结果保存在
⼀个xml⽂件（格式⾃定义，要合理）中，以供下⼀步实验使⽤。

本代码基于新浪新闻（https://news.sina.com.cn/），
覆盖五种主题："体育","军事","科技","国内","国际"，
每条新闻抓取八种信息：主题、原⽹⻚地址、标题、时间、正⽂内容、责任编辑、来源、图片。
技术路线：通过selenium+firefox模拟浏览器抓取 （参考@https://zhuanlan.zhihu.com/p/31127896）

Refs: 
1. https://www.jianshu.com/p/ba6b64ffef45
2. https://blog.csdn.net/God_favored_one/article/details/78828565
3. https://blog.csdn.net/weixin_42243942/article/details/80639040
4. https://selenium-python.readthedocs.io/getting-started.html
5. https://zhuanlan.zhihu.com/p/29645367
6. https://zhuanlan.zhihu.com/p/31127887
7. https://zhuanlan.zhihu.com/p/31127896
......

ATTENTION: 要提前在命令行执行export PATH=${PATH:+$PATH:}/usr/lib/firefox:/usr/local/bin/geckodriver，添加firefox和相应驱动的路径到PATH中

'''
import json
import requests
from bs4 import BeautifulSoup
from dicttoxml import dicttoxml
from selenium import webdriver
# import time
'''
需用用到的库有json requests BeautifulSoup dicttoxml selenium
因为滚动新闻是动态网页，所以实践最终采用selenium+firefox方案来获取JS渲染后的html。
新闻的存储方式采用xml格式进行数据存储。
'''
import sys
reload(sys)
sys.setdefaultencoding('utf8')

count=[0,0,0,0,0] #全局变量 对各类主题新闻计数
infoOutput={} #全局变量 最后保存到一个xml文件

'''
获取一个指定了类型和页码的滚动新闻HTML页面：
根据page参数完整化url，然后根据这个url，利用selenium+firefox实现动态网页抓取
'''
def get_html(url, page):
    driver = webdriver.Firefox()
    # time.sleep(2)
    driver.get(url.format(page))  # 动态网页抓取
    # time.sleep(2)
    html=driver.page_source
    driver.close() #关闭当前窗口
    return html

'''
用来解析出一个滚动新闻页面上的所有新闻链接
'''
def parser_url(html):
    urls=[]
    soup=BeautifulSoup(html,'html.parser')
    for obj in soup.select('.c_tit'):
        '''
        例：结构为
        <span class="c_tit">
            <a href="https://news.sina.com.cn/c/2018-10-22/doc-ihmuuiyv8897273.shtml" target="_blank">人大初审药管法草案 围绕问题疫苗暴露问题作修改</a>
        </span>

        print obj
        print obj.text
        分别打印结果是
        <span class="c_tit"><a href="https://news.sina.com.cn/c/2018-10-22/doc-ifxeuwws6974662.shtml" target="_blank">北京市多地区发布大风蓝色预警 最大可达阵风7级</a></span>
        人大初审药管法草案 围绕问题疫苗暴露问题作修改
        '''
        news=obj.find('a') #一定是单个，所以不需要find_all
        # print news
        # print news.text
        # print news['href']
        url=news['href']
        urls.append(url)
    return urls

'''
信息抓取的主要功能函数
'''
def parse_content(topicIndex,urls):
    for url in urls: #一个url对应一则新闻
        imgs=[] #一篇新闻可能含有多个图片，用scrs来存放
        article=[] #存放一篇新闻
        res=requests.get(url)
        res.encoding='utf-8' #不设置utf-8编码，会出现乱码的情况
        soup=BeautifulSoup(res.text,'html.parser')
        testNULLlist=soup.select('.main-title') #顺便判断这个新闻是不是找不到页面
        if len(testNULLlist)==0:
        	continue
        title=testNULLlist[0].text #获取新闻标题（select返回的是一个tag的数组，[0]取数组里第一个tag元素。）
        date=soup.select('.date')[0].text #获取日期
        source = soup.select('.source')[0].text #新闻来源
        authorList=soup.select(".show_author")
        if len(authorList)==0: #有几类新闻没有责任编辑
        	show_author="" 
        else:
        	show_author=authorList[0].text[5:] #将字符串为责任编辑： 去掉
        print("【主题】 "+topicList[topicIndex])
        print("【原网页地址】："+url)
        print("【标题】 "+title)
        print("【时间】 "+date)
        print("【正文内容】 ")
        for i in soup.select('.article p')[:-1]: #class为article，并且标签为p
            '''
            [:-1] 
            It means "all elements of the sequence but the last". 
            In the context of f.readline()[:-1] it means "I'm pretty sure that line ends with a newline and I want to strip it".
            '''
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

        #向全局字典变量infoOutput中添加这一条新闻抓取出的信息
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

def start():
    for i in range(len(topicList)):
        j=0
        # 此处只访问而没有修改全局变量count
        while(count[i]<225):  #考虑到新闻列表是动态刷新不断增加的，所以比200多抓一些
            j+=1
            html=get_html(URLtopicList[i],j) #请求第i类新闻的下一个页面，其中每个页面包含的新闻条数通过参数控制为20，但不能保证每次都有20条
            urls=parser_url(html) 
            parse_content(i, urls) #新闻主题类别通过i传递进去
    save_xml()

def save_xml():
    xml=dicttoxml(infoOutput)
    xmlFile=open(xmlFilePath,"w") 
    xmlFile.write(xml.decode())
    xmlFile.close()
    print("===================全部爬取工作完成 结果保存在"+xmlFilePath+"中===================")

if __name__=='__main__':
    topicList=["体育","军事","科技","国内","国际"]
    URLtopicList=["https://news.sina.com.cn/roll/#pageid=153&lid=2512&k=&num=50&page={}",
    "https://news.sina.com.cn/roll/#pageid=153&lid=2514&k=&num=50&page={}",
    "https://news.sina.com.cn/roll/#pageid=153&lid=2515&k=&num=50&page={}",
    "https://news.sina.com.cn/roll/#pageid=153&lid=2510&k=&num=50&page={}",
    "https://news.sina.com.cn/roll/#pageid=153&lid=2511&k=&num=50&page={}"]
    xmlFilePath="task1_out.xml"
    start()
