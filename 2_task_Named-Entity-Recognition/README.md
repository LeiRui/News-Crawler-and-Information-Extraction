# Named Entity Recognition
Modern Database Project 1 Task 2

## Task Description
使⽤任务一⽹络爬⾍得到的结果，对于每⼀条爬取到的新闻，识别出其标题和正⽂内容中出现的⼈名、地名、机构名、事件名和专有名词等。⼈名和地名为必做项，机构名、事件名、专有名词等其它类型的实体为选做项（额外分判定依据之⼀），全部的识别结果保存在⼀个xml⽂件中（格式⾃定义，要合理）。

## Guidance
安装THULAC命令：
```
sudo pip install thulac
```
然后直接执行：
```
python task2-thulac.py
```
即可运行输出结果task2_out.xml文件。

把task2_out.xml文件转存到out-safe子文件夹内供后面的任务3使用，避免下次执行task2-thulac.py时被覆盖。
```
mv task2_out.xml out-safe/.
```

