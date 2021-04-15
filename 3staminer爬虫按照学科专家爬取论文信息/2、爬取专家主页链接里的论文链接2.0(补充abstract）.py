import pymysql.cursors
import requests
import re
from bs4 import BeautifulSoup
import json
import time

class aminer_person_paper:
        def __init__(self,disciplineid,discipline,expertid,author,name,paper_id,paper_name,journal_name,year,level,paperdoi):
                self.disciplineid=disciplineid  #传参
                self.discipline=discipline      #传参
                self.expertid=expertid          #传参
                self.author = author            #传参
                self.name=name
                self.paper_id=paper_id
                self.paper_name=paper_name
                self.journal_name=journal_name
                self.year=year
                self.level=level
                self.paperdoi=paperdoi

        def print(self):
                print(self.disciplineid,  #传参
                self.discipline,      #传参
                self.expertid,          #传参
                self.author,            #传参
                self.name,
                self.paper_id,
                self.paper_name,
                self.journal_name,
                self.year,
                self.level,
                self.paperdoi)
class index_Author:
    def __init__(self, ordernum,name, id, discipline, disciplineid, domain):
        self.ordernum = ordernum
        self.name = name
        self.id = id
        self.discipline = discipline
        self.disciplineid = disciplineid
        self.domain = domain

    def print(self):
        print(self.ordernum,self.name,  self.id, self.discipline, self.disciplineid, self.domain)

count=0

def insert_perauthor_paperinfo(paper_id,abstract):
    # 初始化connection
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='000000',
        db='aminer',
        charset='utf8mb4',
    )
    cursor = connection.cursor()

    sql="UPDATE aminer_person_paper_abstract SET abstract = %s WHERE paper_id= %s"
    val = [abstract,paper_id ]
    # cursor.execute(sql,val)
    try:
        cursor.execute(sql,val)
    except:
       print("update 更新错误")

    global count
    count=count+1
    print("已更新第 :" + str(count) + "条数据"+paper_id+"  ")

    # 创建的connection是非自动提交，需要手动commit
    connection.commit()

def get_perauthor_paperinfo(paper_id):
        url = "https://www.aminer.cn/pub/"+paper_id
        headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"}


        try:
            # time.sleep(1)
            response = requests.get(url,headers=headers,timeout=(20,30))

        except:
            print("连接超时，此条作废")
            return


        if response.status_code==200:
                # print("数据解析成功")
                #解析数据
                soup=BeautifulSoup(response.text,'html.parser')
                # print(soup)
                #获取页面中的数据
                two_string=soup.body.script.string
                # print(two_string)
                #返回一个数组
                try:
                    abstracts=re.findall('"abstract":"(.*?)"', str(two_string), re.S)

                    abstract=abstracts[0]
                except:
                    return
                print("abstract:"+ abstract)
                # initialProps = re.findall('window.g_initialProps = (.*?});', str(two_string), re.S)
                # print(initialProps[0])
                #str转化为json用这一句就够了
                # try:
                #     r=json.loads(initialProps[0])
                # except:
                #     print("initialProps 无数据")
                #     return

                # r = json.loads(""+initialProps[0]+"\'")
                # print(type(r))

                # print(r)

                # paper=r.get('paper')
                # abstract=paper.get('abstract')


                insert_perauthor_paperinfo(paper_id,abstract)
                print('\r\n')


        else:
                print("数据请求不成功,等待20秒")#要做循环重新处理
                time.sleep(20)


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

    # sql = "SELECT * FROM index_author  WHERE ordernum>'2206' "
    sql = "SELECT * FROM aminer_person_paper_abstract WHERE ordernum>'88507'"
    cursor.execute(sql)
    results=cursor.fetchall()
    #row代表一个作者
    for row in results:
        paper_id=row[6]

        get_perauthor_paperinfo(paper_id)


main()
print("爬完啦")








