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

count=41480

def insert_perauthor_paperinfo(aminer_person_paper):
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


    sql = "INSERT INTO aminer_person_paper (ordernum,disciplineid,discipline,expertid,author,name,paper_id,paper_name,journal_name,year,level,paperdoi) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
    val = [count,
           aminer_person_paper.disciplineid,
           aminer_person_paper.discipline,
           aminer_person_paper.expertid,
           aminer_person_paper.author,
           aminer_person_paper.name,
           aminer_person_paper.paper_id,
           aminer_person_paper.paper_name,
           aminer_person_paper.journal_name,
           aminer_person_paper.year,
           aminer_person_paper.level,
           aminer_person_paper.paperdoi
           ]

    try:
        cursor.execute(sql, val)
    except:
        sql2 = "INSERT INTO aminer_person_paper (ordernum,disciplineid,discipline,expertid,author,name,paper_id,paper_name,journal_name,year,level,paperdoi) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
        val2 = [count, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999,999]
        cursor.execute(sql2, val2)

    print("已插入第 :" + str(count) + "条数据")

    # 创建的connection是非自动提交，需要手动commit
    connection.commit()
def get_perauthor_paperinfo(author,id,discipline,domain):
        url = "https://www.aminer.cn/profile/"+id
        headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"}


        try:
            time.sleep(1)
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
                initialProps = re.findall('window.g_initialProps = (.*?});', str(two_string), re.S)
                # print(initialProps[0])

                #str转化为json用这一句就够了
                try:
                    r=json.loads(initialProps[0])
                except:
                    print("initialProps 无数据")
                    return


                profile = r.get('profile')
                #所有论文的列表profilePubs
                profilePubs=profile.get('profilePubs')
                # 某一篇论文
                for span1 in profilePubs:
                        try:
                                authors=span1.get('authors')
                                name=""
                                for span2 in authors:
                                        if(span2==authors[0]):
                                                name=name+span2.get('name')
                                        else:
                                                name=name+','+span2.get('name')
                                # print(name)####################################
                        except:
                                name="no name"

                        try:
                                title=span1.get('title')
                                paper_name=title#####################################
                        except:
                                paper_name="no paper_name"

                        try:
                                paper_id=span1.get('id')

                        except:
                                paper_id="no paper_id"

                        try:
                            label=""
                            labels = soup.find_all("div", id="pid_" + paper_id)

                            for row in labels:
                                label_temps = row.find_all("span", class_="label")
                                for row2 in label_temps:
                                    if(row2==label_temps[0]):
                                        label=label+row2.text
                                    else:
                                        label=label+","+row2.text
                                # label = label_temps.text
                                # print(label.text)
                        except:
                            label = "no label"

                        try:
                                venue=span1.get('venue')
                                info=venue.get('info')
                                journal_name=info.get('name')###################################
                        except:
                                journal_name="no journal_name"

                        try:
                                year=span1.get('year')###################################
                        except:
                                year="no year"

                        try:
                                paperdoi=span1.get('doi')###################################
                        except:
                                paperdoi="no paperdoi"
                        entity=aminer_person_paper(domain,discipline,id,author,name,paper_id,paper_name,journal_name,year,label,paperdoi)
                        entity.print()
                        insert_perauthor_paperinfo(entity)
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

    sql = "SELECT * FROM index_author  WHERE ordernum>'2206' "
    cursor.execute(sql)
    results=cursor.fetchall()
    #row代表一个作者
    for row in results:
        ordernum=row[0]
        name=row[1]
        id=row[2]
        discipline=row[3]
        disciplineid=row[4]
        domain=row[5]
        author=index_Author(ordernum,name, id, discipline, disciplineid, domain)
        get_perauthor_paperinfo(author.name,author.id,author.discipline,author.domain)


main()









