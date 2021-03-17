import pymysql.cursors
import requests
import re
from bs4 import BeautifulSoup
import json

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

def get_perauthor_paper(author,id,discipline,domain):
        url = "https://www.aminer.cn/profile/"+id
        headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"}


            # //json.loads 是将json字符串（str类型）转化为字典(python格式）
        response = requests.get(url,headers=headers)

        if response.status_code==200:
                # print("数据解析成功")
                #解析数据
                soup=BeautifulSoup(response.text,'html.parser')
                # print(soup)
                #获取页面中的数据
                two_string=soup.body.script.string
                # print(two_string)
                initialProps = re.findall('window.g_initialProps = (.*?});', two_string, re.S)
                # print(initialProps[0])

                #str转化为json用这一句就够了
                r=json.loads(initialProps[0])


                profile = r.get('profile')
                #所有论文的列表profilePubs
                profilePubs=profile.get('profilePubs')
                # 某一组论文
                for span1 in profilePubs:
                        try:
                                authors=span1.get('authors')
                                name=""
                                for span2 in authors:
                                        if(span2==authors[0]):
                                                name=name+span2.get('name')
                                        else:
                                                name=name+' , '+span2.get('name')
                                # print(name)####################################
                        except:
                                name="no name"

                        try:
                                title=span1.get('title')
                                paper_name=title#####################################
                        except:
                                paper_name="no paper_name"

                        try:
                                id=span1.get('id')
                                paper_id=id###################################
                        except:
                                paper_id="no paper_id"

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
                        entity=aminer_person_paper(domain,discipline,id,author,name,paper_id,paper_name,journal_name,year,'暂时没得到',paperdoi)
                        entity.print()
                        print('/n')

        else:
                print("数据请求不成功")#要做循环重新处理
def get():
    # 初始化connection
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='000000',
        db='aminer',
        charset='utf8mb4',
    )
    cursor = connection.cursor()

    sql = "SELECT * FROM index_author "
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
        get_perauthor_paper(author.name,author.id,author.discipline,author.domain)
        # author.print()

get()









