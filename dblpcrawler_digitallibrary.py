# -*- coding: utf-8 -*-
"""
原代码只将数据解析到文本，且对重复字段没有进行处理
<article>
    <author>Mr.A</author>
    <author>Mr.B</author>
</article>
此代码修正了上述不足，然后将解析后字段导入数据库
读取数据：dblp.xml 2.01G
导入Mysql：170万+
导入表：visual_dataset.dblp
生成备份文件：insert.sql
@author: Administrator
"""
# !/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import print_function
import xml.sax
import sys
import io
import re
import logging
import traceback
import pymysql.cursors

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')  # 改变标准输出的默认编码
'''
logging.basicConfig(level=logging.DEBUG,
                    format='%(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='I:\\ABC000000000000\\Dblp\\simple\\app.log',
                    filemode='w')
'''

class MovieHandler(xml.sax.ContentHandler):
    '''
    res  类变量，记录解析后的字段值
    '''
    athr = []
    ee = []
    res = ''
    sqlval = ''

    def __init__(self):
        self.CurrentData = ""
        self.author = ""
        self.title = ""
        self.pages = ""
        self.year = ""
        self.volume = ""
        self.journal = ""
        self.number = ""
        self.url = ""
        self.ee = ""

    # 元素开始事件处理,对每个顶级标签内数据的解析都会重复的调用此方法
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "article":
            try:
                if len(self.__class__.sqlval):
                    # print(re.sub(",$","",self.__class__.sqlval))

                    lt = re.sub(",$", "", self.__class__.sqlval).split(",")
                    lt2 = sorted(set(lt), key=lt.index)

                    insert_mysql(
                        ','.join(lt2), self.__class__.res,
                        ','.join(self.__class__.athr),
                        ','.join(self.__class__.ee)
                    )
            except:
                traceback.print_exc()
            # 清空res变量，由于跨方法拼字符串，所以使用了类变量
            self.__class__.res = ''
            self.__class__.sqlval = ''
            self.__class__.athr = []
            self.__class__.ee = []
            # 因为处在if判断后，所以只解析第一个标签内的属性值
            mdate = attributes["mdate"]
            key = attributes["key"]
            # 拼接字符串
            self.__class__.res += mdate + SYMBOL + key + SYMBOL
            self.__class__.sqlval += "article_mdate,article_key,"
            # 经过开始事件->内容事件的方法之后，调用此结束事件处理，
            # 对先前内容事件方法中对实例变量的值进行统一过滤处理

    def endElement(self, tag):
        if self.CurrentData == "author":
            self.__class__.sqlval += "author,"
            if '$_author_$' not in self.__class__.res:
                self.__class__.res += "$_author_$" + SYMBOL
            self.__class__.athr.append(self.author)
        elif self.CurrentData == "title":
            self.__class__.sqlval += "title,"
            self.__class__.res += self.title + SYMBOL
        elif self.CurrentData == "pages":
            self.__class__.sqlval += "pages,"
            self.__class__.res += self.pages + SYMBOL
        elif self.CurrentData == "year":
            self.__class__.sqlval += "year,"
            self.__class__.res += self.year + SYMBOL
        elif self.CurrentData == "volume":
            self.__class__.sqlval += "volume,"
            self.__class__.res += self.volume + SYMBOL
        elif self.CurrentData == "journal":
            self.__class__.sqlval += "journal,"
            self.__class__.res += self.journal + SYMBOL
        elif self.CurrentData == "number":
            self.__class__.sqlval += "number,"
            self.__class__.res += self.number + SYMBOL
        elif self.CurrentData == "url":
            self.__class__.sqlval += "url,"
            self.__class__.res += self.url + SYMBOL
        elif self.CurrentData == "ee":
            self.__class__.sqlval += "ee,"
            if '$_ee_$' not in self.__class__.res:
                self.__class__.res += "$_ee_$" + SYMBOL
            self.__class__.ee.append(self.ee)

        self.CurrentData = ""
        # 内容事件处理，对每个子元素都执行此方法，并且重置实例变量的值

    def characters(self, content):
        if self.CurrentData == "author":
            self.author = content.replace("'", "`")
        elif self.CurrentData == "title":
            self.title = content.replace("'", "`")
        elif self.CurrentData == "pages":
            self.pages = content.replace("'", "`")
        elif self.CurrentData == "year":
            self.year = content.replace("'", "`")
        elif self.CurrentData == "volume":
            self.volume = content.replace("'", "`")
        elif self.CurrentData == "journal":
            self.journal = content.replace("'", "`")
        elif self.CurrentData == "number":
            self.number = content.replace("'", "`")
        elif self.CurrentData == "url":
            self.url = content.replace("'", "`")
        elif self.CurrentData == "ee":
            self.ee = content.replace("'", "`")


# class结束
'''
独立方法：将解析出的字段导入Mysql
'''


def insert_mysql(names, values, authors, ees):
    global count
    if count == 100:
        sys.exit
    val = re.sub(",'$", "", values)
    val = re.sub("#", "&", val)
    val = val.replace("$_ee_$", re.sub(",", ",", ees))
    val = val.replace("$_author_$", re.sub(",", ",", authors))
    sql = ''
    if len(names) & len(names):
        try:
            # 存入Mysql via：github.com/PyMySQL/PyMySQL
            with connection.cursor() as cursor:

                sql = "INSERT INTO `dblp` ("
                sql += names
                sql += " )VALUES ('"
                sql += val
                sql += " )"
                count += 1
                print('parse items and inserted :' + str(count))
                if sql is not None and sql != 'None':
                    logging.info(sql + ';')
                    cursor.execute(sql)
            # 创建的connection是非自动提交，需要手动commit
            connection.commit()
            a = 1
        except:

            logging.error(traceback.print_exc())


# 这里直接运行，则本身__name__就是__main__
if (__name__ == "__main__"):
    count = 0

    # 定义全局分隔符
    SYMBOL = "','"
    XMLFPATH = "E:\\zhangxu\\digital library\\dblp.xml\\dblp.xml"
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    Handler = MovieHandler()
    parser.setContentHandler(Handler)
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='000000',
        db='dblp',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)
    parser.parse(XMLFPATH)
    connection.close()