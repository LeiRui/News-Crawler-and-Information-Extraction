# Named Entity Recognition
Modern Database Project 1 Task 3

## Task Description
使⽤之前⽹络爬⾍得到的结果，对于每⼀条爬取到的新闻，识别出其标题和正⽂部分出现的实体关系，要求⾄少能够抽取出3种关系，实体关系类型不限，可⾃⾏定义，如可以是⼈与⼈之间的关系、⼈与机构之间的关系或者⼈与事件之间的关系等。

## Guidance
代码用到pandas和pytorch，pytorch下载方法直接参见 https://pytorch.org/ 。

然后按顺序直接依次执行下述三个python文件即可得到最终的关系抽取结果task3_out.xml。

### task3_step1.py
作用是从任务2命名实体识别的结果中提取人名实体并整理成规定的格式：[句中实体1的名字，句中实体2的名字，完整句子内容，句子所属的新闻url]，供下一步使用。

输入的数据来自`2_task-Named-Entity-Recognition/out-safe/task2_out.xml`，输出`task3_step1_out.txt`。

### task3_step2.py
作用是参考`ChineseNRE/data/people-relation/data_util.py`写法，把txt输入数据处理成pkl文件，包含特征：词向量和位置向量，供下一步的模型使用。

输入的数据为`task3_step1_out.txt`，输出`task3_step2_out.pkl`。

### task3_step3.py
作用是通过模型得到输入的实体对之间的关系类别输出。

输入的数据为`task3_step1_out.txt`和`task3_step2_out.pkl`，输出`task3_out.xml`。使用的训练好的模型来自`ChineseNRE/model_trained/model_01.pkl`。这个模型是通过在本地运行ChineseNRE项目 (https://github.com/buppt/ChineseNRE) 代码训练得到的，具体的训练过程参见它的README。


