# Sina-News-Crawler
Modern Database Project 1 task 1

## Task Description
(1)	网络爬虫程序能够自动从新浪新闻网站（ https://news.sina.com.cn/ ）爬取一定数量的新闻。

(2)	新闻覆盖5种主题类型：体育、军事、科技、国内、国际。

(3)	每类主题爬取的新闻不少于200条。

(4)	每条新闻爬取8个内容：主题、原网页地址、标题、时间、正文内容、责任编辑、新闻来源、图片url。

(5)	全部爬取结果保存在一个xml文件（格式自定义）中供下一步实验使用。

## Guidance
（1）需要用到的库有requests、BeautifulSoup4、dicttoxml、selenium。基于selenium+firefox技术路线，使用ubuntu自带的firefox，需要安装firefox的驱动geckodriver。然后提前把firefox和geckodriver的路径添加到PATH中。相应命令如下（注意选择合适的下载版本）：
```
sudo pip install requests
sudo pip install BeautifulSoup4
sudo pip install dicttoxml
sudo pip install selenium
wget https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-linux64.tar.gz
sudo tar xzvf geckodriver-v0.23.0-linux64.tar.gz -C /usr/local/bin
sudo chmod +x /usr/local/bin/geckodriver
export PATH=${PATH:+$PATH:}/usr/lib/firefox:/usr/local/bin/geckodriver
```
完成上述指令后，直接执行
```
python task1-method2.py
```
即可运行输出结果task1_out.xml文件。

（2） 把得到的task1_out.xml结果转存到out-safe子文件夹内供后面的任务2使用，避免下次执行task1-method2.py时被覆盖：
```
mv task1_out.xml out-safe/.
```

