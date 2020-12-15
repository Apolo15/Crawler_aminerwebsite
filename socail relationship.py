# -*- coding: utf-8 -*-
import jieba   #分词工具
import codecs  #解析器
import pandas as pd  #相当于excel，处理多维数组？
import numpy as np  #支持维度数据和矩阵运算
from PIL import Image
import jieba.posseg as pseg  #词性标注
import matplotlib.pyplot as plt #基于python的图标绘图系统
from wordcloud import WordCloud, ImageColorGenerator

# names        :  姓名字典，保存人物，键为人物名称，值为该人物在全文中出现的次数
# relationship :  关系字典，保存人物关系的有向边，键为有向边的起点，值为一个字典 edge ，edge 的键为有向边的终点，
#                 值是有向边的权值，代表两个人物之间联系的紧密程度
# lineNames    :  缓存变量，保存对每一段分词得到当前段中出现的人物名称关系
# node         :  存放处理后的人物
# stopwords    :  存放停用词
# replace_words:  替代词字典，保存要相互替代的词，键为被替代词，值为替代词
names = {}
relationships = {}
lineNames = []


stopwords = ['吕州', '林城', '银行卡', '明白', '白云', '嗡嗡嘤嘤',
             '阴云密布', '雷声', '陈大', '谢谢您', '安置费', '任重道远',
             '孤鹰岭', '阿庆嫂', '岳飞', '师生', '养老院', '段子', '老总']
replace_words = {'师母': '吴慧芬', '陈老': '陈岩石', '老赵': '赵德汉', '达康': '李达康', '高总': '高小琴',
                 '猴子': '侯亮平', '老郑': '郑西坡', '小艾': '钟小艾', '老师': '高育良', '同伟': '祁同伟',
                 '赵公子': '赵瑞龙', '郑乾': '郑胜利', '孙书记': '孙连城', '赵总': '赵瑞龙', '昌明': '季昌明',
                 '沙书记': '沙瑞金', '郑董': '郑胜利', '宝宝': '张宝宝', '小高': '高小凤', '老高': '高育良',
                 '伯仲': '杜伯仲', '老杜': '杜伯仲', '老肖': '肖钢玉', '刘总': '刘新建', '美女老总': '高小琴'}

jieba.load_userdict("C:/Users/ZL/Desktop/dict.txt")  # 加载字典
with codecs.open("C:/Users/ZL/Desktop/renmin.txt", "r", "gb18030") as f:
    for line in f.readlines():
        poss = pseg.cut(line)  # 分词并返回该词词性
        lineNames.append([])  # 为新读入的一段添加人物名称列表
        for w in poss:
            if w.word in stopwords:  # 去掉某些停用词，防止干扰人物关系
                continue
            if w.flag != "nr" or len(w.word) < 2:  # 判断当前词的词性和长度
                if w.word not in replace_words:
                    continue
            if w.word in replace_words:  # 将文中某些人物的昵称替换成正式的名字
                w.word = replace_words[w.word]
            lineNames[-1].append(w.word)  # 为当前段的环境增加一个人物
            if names.get(w.word) is None:  # 如果这个名字从来没有出现过，初始化这个名字
                names[w.word] = 0
                relationships[w.word] = {}
            names[w.word] += 1  # 该人物出现次数加1

        # explore relationships
        for line in lineNames:
            for name1 in line:
                for name2 in line:
                    if name1 == name2:
                        continue
                    if relationships[name1].get(name2) is None:  # 如果没有出现过两者之间的关系，则新建
                        relationships[name1][name2] = 1
                    else:
                        relationships[name1][name2] += 1  # 两人共同出现次数加 1

# output_txt
with codecs.open("data/ccout/renmin_node.txt", "w", "gbk") as f:
    f.write("Id Label Weight\r\n")
    for name, times in names.items():
        f.write(name + " " + name + " " + str(times) + "\r\n")

with codecs.open("data/ccout/renmin_edge.txt", "w", "gbk") as f:
    f.write("Source Target Weight\r\n")
    for name, edges in relationships.items():
        for v, w in edges.items():
            if w > 3:
                f.write(name + " " + v + " " + str(w) + " \r\n ")

# output_csv
list_node = []

for name, times in names.items():
    # print('name1: ',name,'name2: ',name,'频数: ',times)
    list_node.append([name, name, times])
df1 = pd.DataFrame(list_node, columns=['Id', 'Label', 'weight'])
df1.to_csv('data/ccout/node.csv', index=False,encoding='utf_8_sig')

list_edge = []
for name, edges in relationships.items():
    for v, w in edges.items():
        if w > 3:
            list_edge.append([name, v, str(w)])
df2 = pd.DataFrame(list_edge, columns=['Source', 'Target', 'weight'])
df2.to_csv('data/ccout/edge.csv', index=False)
# 至此，代码就生成了目标文件: node.csv,edge.csv文件

# def draw_cloud()
names2 = names.copy()
ci = list(names2.keys())  # 将字典的键值转换为列表
for seg in ci:
    if names2[seg] < 5 or '一' in seg:
        names2.pop(seg)
# 图片遮罩层
mask_img = np.array(Image.open("data/ccin/yunBackground.png"))
font = r'font/simfang.ttf'
wc = WordCloud(
    background_color="white",  # 设置背景颜色，与图片的背景色相关
    mask=mask_img,  # 设置背景图片
    collocations=False,
    font_path=font,  # 显示中文，可以更换字体
    max_font_size=2000,  # 设置字体最大值
    random_state=1,  # 设置有多少种随机生成状态，即有多少种配色方案
    width=1600,
    margin=0).generate_from_frequencies(names2)
plt.imshow(wc)
image_colors = ImageColorGenerator(mask_img)
plt.imshow(wc.recolor(color_func=image_colors))
plt.axis('off')  # 隐藏图像坐标轴
plt.show()  # 展示图片
wc.to_file('data/ccout/ciyun.png')  # 保存生成的词云图

print("程序结束")