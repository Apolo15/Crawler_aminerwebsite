import pymysql.cursors
import requests
import re
from bs4 import BeautifulSoup
import json
import time

count = 0


class aminer_paper_citation:
    def __init__(self, paper_id, discipline_id, citation_id, citation_paper_name, author, year, journal_name,
                 citation_num):
        self.discipline_id = discipline_id  # 传参
        self.author = author  # 传参
        self.paper_id = paper_id
        self.journal_name = journal_name
        self.year = year
        self.citation_id = citation_id
        self.citation_paper_name = citation_paper_name
        self.citation_num = citation_num

    def print(self):
        print(self.paper_id, self.discipline_id, self.citation_id, self.citation_paper_name, self.author, self.year,
              self.journal_name, self.citation_num)


def insert_aminer_paper_citation(entity):
    # 初始化connection
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='000000',
        db='aminer',
        charset='utf8mb4',
    )
    cursor = connection.cursor()

    global count
    count = count + 1

    sql = "INSERT INTO aminer_paper_citation (ordernum,paper_id,discipline_id,citation_id,citation_paper_name,author,year,journal_name,citation_num) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) "
    val = [count,
           entity.paper_id,
           entity.discipline_id,
           entity.citation_id,
           entity.citation_paper_name,
           entity.author,
           entity.year,
           entity.journal_name,
           entity.citation_num
           ]

    try:
        cursor.execute(sql, val)
    except:
        sql2 = "INSERT INTO entity (ordernum,disciplineid,discipline,expertid,author,name,paper_id,paper_name,journal_name,year,level,paperdoi) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
        val2 = [count, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999]
        cursor.execute(sql2, val2)

    print("已插入第 :" + str(count) + "条数据")

    # 创建的connection是非自动提交，需要手动commit
    connection.commit()


def get_paper_citepaerinfo(ordernum, paperid, disciplineid):
    print("目前paper_ordernum", ordernum)
    url = "https://apiv2.aminer.cn/magic?a=getCited__publication.CitedByPid___"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"}

    # //json.loads 是将json字符串（str类型）转化为字典(python格式）
    payload = json.loads(
        '[{"action":"publication.CitedByPid","parameters":{"ids":["' + paperid + '"],"offset":0,"size":30}}]')

    # //json.loads 是将json字符串（str类型）转化为字典(python格式）

    try:
        # time.sleep(1)
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=(20, 30))
    except:
        print("连接超时此条作废")
        return
    if response.status_code == 200:
        r = response.json()
        # print(r)
        data = r.get('data')
        if (data != None):
            for row in data:
                # 获取各项详细信息 items 为所有被引用论文信息
                items = row.get('items')
                # 一个item（row2）是一篇被引用论文
                if (items != None):
                    for row2 in items:
                        try:
                            authors = row2.get('authors')
                            author = ""
                            for row3 in authors:
                                if (row3 == authors[0]):
                                    author = author + row3.get('name')
                                else:
                                    author = author + ',' + row3.get('name')
                        except:
                            author = "no author"

                        try:
                            citation_id = row2.get('id')
                        except:
                            citation_id = "no citation_id"

                        try:
                            citation_paper_name = row2.get('title')
                        except:
                            citation_paper_name = "no citation_paper_name"

                        try:
                            year = row2.get('year')
                        except:
                            year = "no year"

                        try:
                            venue = row2.get('venue')
                            info = venue.get('info')
                            journal_name = info.get('name')
                        except:
                            journal_name = "no journal_name"

                        try:
                            citation_num = row2.get('num_citation')
                        except:
                            citation_num = "no citation_num"

                        entity = aminer_paper_citation(paperid, disciplineid, citation_id, citation_paper_name, author,
                                                       year, journal_name, citation_num)
                        entity.print()
                        insert_aminer_paper_citation(entity)

                else:
                    print("no items")
        else:
            print("no data")


def main():
    # 初始化connection
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='000000',
        db='aminer',
        charset='utf8mb4',
    )
    cursor = connection.cursor()

    sql = "SELECT * FROM aminer_person_paper "
    cursor.execute(sql)
    results = cursor.fetchall()
    # row代表一个作者
    for row in results:
        ordernum = row[0]
        disciplineid = row[1]
        paper_id = row[6]

        get_paper_citepaerinfo(ordernum, paper_id, disciplineid)


main()