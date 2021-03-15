import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymysql.cursors
from selenium import webdriver  # 导入必要的库
import requests
import json


count=0
class index_Author:
    def __init__(self, name, id, discipline, disciplineid, domain):
        self.name = name
        self.id = id
        self.discipline = discipline
        self.disciplineid = disciplineid
        self.domain = domain

    def print(self):
        print(self.name,  self.id, self.discipline, self.disciplineid, self.domain)

def insert_index_Author(author):
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

    sql = ''
    sql = "INSERT INTO index_people (ordernum,name,id,discipline,disciplineid,domain) VALUES (%s,%s,%s,%s,%s,%s) "
    val = [count, author.name, author.id, author.discipline, author.disciplineid, author.domain]

    try:
        cursor.execute(sql, val)
    except:
        sql2 = "INSERT INTO index_people (ordernum,name,id,discipline,disciplineid,domain) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
        val2 = [999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999]
        cursor.execute(sql2, val2)

    print("已插入第 :" + str(count) + "条数据")

    # 创建的connection是非自动提交，需要手动commit
    connection.commit()






def get_People_Info(homepagerurl,discipline,disciplineid,domain):

    url = "https://apiv2.aminer.cn/n?a=__searchapi.SearchPerson__"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"}

    # //json.loads 是将json字符串（str类型）转化为字典(python格式）
    payload=json.loads('[{"action":"searchapi.SearchPerson","parameters":{"offset":0,"size":20000,"query":"","include":["agg","intelli","topics"],"domains":["'+domain+'"]},"schema":{"person":["id","name","name_zh","avatar","tags","is_follow","num_view","num_follow","is_upvoted","num_upvoted","is_downvoted","bind",{"profile":["position","position_zh","affiliation","affiliation_zh","org"]},{"indices":["hindex","gindex","pubs","citations","newStar","risingStar","activity","diversity","sociability"]},"tags_translated_zh"]}}]')


    # //json.loads 是将json字符串（str类型）转化为字典(python格式）
    response = requests.post(url,headers=headers,data=json.dumps(payload))

    r=response.json()

    data=r.get('data')
    for span1 in data:
        persons = span1.get('persons')
        for span2 in persons:
            id=span2.get('id')
            name=span2.get('name')
            author=index_Author(name,id,discipline,disciplineid,domain)
            insert_index_Author(author)
            author.print()
        print("该学科所有专家6个信息爬取完毕")





Disciplines = [
    ["https://www.aminer.cn/search/person?domain=143&t=b", "计算机科学", 1,142],
    ["https://www.aminer.cn/search/person?domain=122&q=&t=b", "通信与信息科学", 2,122],
    ["https://www.aminer.cn/search/person?domain=102&q=&t=b", "数学", 3,102],
    ["https://www.aminer.cn/search/person?domain=103&q=&t=b", "物理学", 4,103],
    ["https://www.aminer.cn/search/person?domain=137&q=&t=b", "化学", 5,137],
    ["https://www.aminer.cn/search/person?domain=119&q=&t=b", "光学", 6,119],
    ["https://www.aminer.cn/search/person?domain=117&q=&t=b", "生物学", 7,117],
    ["https://www.aminer.cn/search/person?domain=113&q=&t=b", "天文学", 8,113],
    ["https://www.aminer.cn/search/person?domain=129&q=&t=b", "航空航天工程", 9,129],
    ["https://www.aminer.cn/search/person?domain=114&q=&t=b", "地理学", 10,114],
    ["https://www.aminer.cn/search/person?domain=116&q=&t=b", "地质学", 11,116],
    ["https://www.aminer.cn/search/person?domain=115&q=&t=b", "地球物理学", 12,115],
    ["https://www.aminer.cn/search/person?domain=124&q=&t=b", "地质工程", 13,124],
    ["https://www.aminer.cn/search/person?domain=125&q=&t=b", "矿业", 14,125],
    ["https://www.aminer.cn/search/person?domain=126&q=&t=b", "石油工程", 15,126],
    ["https://www.aminer.cn/search/person?domain=128&q=&t=b", "海洋工程", 16,128],
    ["https://www.aminer.cn/search/person?domain=105&q=&t=b", "电气工程", 17,105],
    ["https://www.aminer.cn/search/person?domain=127&q=&t=b", "交通运输", 18,127],
    ["https://www.aminer.cn/search/person?domain=106&q=&t=b", "医学", 19,106],
    ["https://www.aminer.cn/search/person?domain=107&q=&t=b", "临床医学", 20,107],
    ["https://www.aminer.cn/search/person?domain=108&q=&t=b", "药学", 21,108],
    ["https://www.aminer.cn/search/person?domain=138&q=&t=b", "心理学", 22,138],
    ["https://www.aminer.cn/search/person?domain=139&q=&t=b", "免疫与微生物学", 23,139],
    ["https://www.aminer.cn/search/person?domain=140&q=&t=b", "神经科学", 24,140],
    ["https://www.aminer.cn/search/person?domain=134&q=&t=b", "生物医学工程", 25,134],
    ["https://www.aminer.cn/search/person?domain=120&q=&t=b", "仪器科学技术", 26,120],
    ["https://www.aminer.cn/search/person?domain=121&q=&t=b", "冶金工程", 27,121],
    ["https://www.aminer.cn/search/person?domain=123&q=&t=b", "建筑学", 28,123],
    ["https://www.aminer.cn/search/person?domain=130&q=&t=b", "核科学与技术", 29,130],
    ["https://www.aminer.cn/search/person?domain=131&q=&t=b", "农业工程", 30,131],
    ["https://www.aminer.cn/search/person?domain=132&q=&t=b", "林学", 31,132],
    ["https://www.aminer.cn/search/person?domain=133&q=&t=b", "环境科学与工程", 32,133],
    ["https://www.aminer.cn/search/person?domain=135&q=&t=b", "食品科学与工程", 33,135],
    ["https://www.aminer.cn/search/person?domain=109&q=&t=b", "经济学", 34,109],
    ["https://www.aminer.cn/search/person?domain=136&q=&t=b", "管理学", 35,136],
    ["https://www.aminer.cn/search/person?domain=110&q=&t=b", "社会学", 36,110],
    ["https://www.aminer.cn/search/person?domain=111&q=&t=b", "教育学", 37,111],
    ["https://www.aminer.cn/search/person?domain=112&q=&t=b", "体育学", 38,112],
    ["https://www.aminer.cn/search/person?domain=118&q=&t=b", "历史学", 39,118]]

for i in range(0, 39):#第一层遍历，所有的学科
    get_People_Info(Disciplines[i][0], Disciplines[i][1], Disciplines[i][2],Disciplines[i][3])#第二层遍历，每个学科下面的每个专家

print("所有的都执行完毕啦~")
