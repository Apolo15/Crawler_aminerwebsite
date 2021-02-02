import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymysql.cursors
from selenium import webdriver  # 导入必要的库
import requests
import json
import re

option = webdriver.ChromeOptions()
option.add_argument("headless")
# chromedriver.exe的存放路径,使用chromedrive需要下载驱动
driver_path = 'E:\zhangxu\pythonanzhuang\python-3.9\Scripts\chromedriver.exe'

# 通过webdriver对象的Chrome方法【不同的浏览器对应不同的方法】，获取到chromedriver.exe
# browser = webdriver.Chrome(executable_path=driver_path, chrome_options=option)
# browser_1 = webdriver.Chrome(executable_path=driver_path, chrome_options=option)
# browser_2 = webdriver.Chrome(executable_path=driver_path, chrome_options=option)

# browser = webdriver.Chrome(executable_path=driver_path)
browser_1 = webdriver.Chrome(executable_path=driver_path)
# browser_2 = webdriver.Chrome(executable_path=driver_path)

# 计数count，计算一共插入多少个author了(开始的专家id）
count = 194115
# 初始化浏览器，让他登陆和最大化，不然无法捕获所有元素
# browser.maximize_window()
browser_1.maximize_window()
# browser_2.maximize_window()

time.sleep(2)


class Author:
    def __init__(self, name, title, department, homepage, papers, citation, hindex, interests):
        self.name = name
        self.title = title
        self.department = department
        self.homepage = homepage
        self.papers = papers
        self.citation = citation
        self.hindex = hindex
        self.interests = interests

    def print(self):
        print(self.name, self.title, self.department, self.homepage, self.papers, self.citation, self.hindex,
              self.interests)


def insert_mysql(author, discipline, disciplineid):
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
    sql = "INSERT INTO people (disciplineid,discipline,expertid,name,title,department,homepage,papers,citation,hindex,interests) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "

    val = [disciplineid, discipline, count, author.name, author.title, author.department, author.homepage,
           str(author.papers), str(author.citation), str(author.hindex), author.interests]

    try:
        cursor.execute(sql, val)
    except:
        sql2 = "INSERT INTO people (disciplineid,discipline,expertid,name,title,department,homepage,papers,citation,hindex,interests) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "

        val2 = [999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999]
        cursor.execute(sql2, val2)

    print("已插入第 :" + str(count) + "条数据")

    # 创建的connection是非自动提交，需要手动commit
    connection.commit()


# 抓取【个人主页】的详细信息
def author_info_scratch(url, discipline, disciplineid):
    postUrl = 'https://apiv2.aminer.cn/magic'

    temp_id = re.findall('profile/(.*)', url, re.S)
    for span in temp_id:
        id = span

    # //json.loads 是将json字符串（str类型）转化为字典(python格式）
    payloadData = json.loads(
        '[{"action":"personapi.get","parameters":{"ids":["' + id + '"]},"schema":{"person":["id","name","name_zh","avatar","num_view","is_follow","work","hide","nation","language","bind","acm_citations","links","educations","tags","tags_zh","num_view","num_follow","is_upvoted","num_upvoted","is_downvoted","is_lock",{"indices":["hindex","pubs","citations"]},{"profile":["position","position_zh","affiliation","affiliation_zh","work","gender","lang","homepage","phone","email","fax","bio","bio_zh","edu","address","note","homepage","titles"]}]}}]')

    try:
        # //json.dumps是将字典(python格式）转化为json字符串（str类型
        result = requests.post(postUrl, data=json.dumps(payloadData))
        result_processed = result.json()

        data1 = result_processed.get('data')
        # print(data1)
        for span in data1:
            data2 = span.get('data')
            # print(data2)
            for span2 in data2:
                # name
                try:
                    name = span2.get('name')
                    name_zh = span2.get('name_zh')
                    if (name_zh != ''):
                        name = name + '(' + name_zh + ')'
                except:
                    name='no name'
                # title
                try:
                    position = span2.get('profile').get('position')
                    title = position
                except:
                    title='no title'

                # department
                try:
                    affiliation_zh = span2.get('profile').get('affiliation_zh')  # 做个逻辑判断，有中文只出现中文
                    affiliation = span2.get('profile').get('affiliation')
                    department = affiliation
                    if (affiliation_zh != None):
                        department = affiliation_zh
                except:
                    department='no department'

                # homepage
                try:
                    homepage = span2.get('profile').get('homepage')
                except:
                    homepage='no homepage'

                # papers
                try:
                    pubs = span2.get('indices').get('pubs')
                    papers = pubs
                except:
                    papers='no papers'


                # citation
                try:
                    citations = span2.get('indices').get('citations')
                    citation = citations
                except:
                    citation='no citation'

                # hindex
                try:
                    hindex = span2.get('indices').get('hindex')
                except:
                    hindex='no hindex'

                # interests
                try:
                    tags = span2.get('tags')
                    interests = ''
                    if(tags==None):
                        interests=''
                    else:
                        if (len(tags) >= 5):
                            for span in range(0, 5):
                                interests = interests + tags[span] + ','
                        else:
                            for span in range(0, len(tags)):
                                interests = interests + tags[span] + ','
                except:
                    interests='no interests'

        author = Author(name, title, department, homepage, papers, citation, hindex, interests)
        author.print()
        time.sleep(1)
        insert_mysql(author, discipline, disciplineid)
    except:
        return 0

    return 1


# 挨个点击【作者列表】，进入【个人主页】后调用author_info_scratch
def author_list(url, discipline, disciplineid):
    browser_1.get(url)
    time.sleep(2)
    pagenum = WebDriverWait(browser_1, 100).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'ant-pagination-simple-pager'))).text
    # pagenum = browser_1.find_element_by_xpath(
    #     '/html/body/div/section/main/main/article/div[2]/div[3]/div[1]/div[2]/div[1]/div[3]/div[2]/div[2]/ul/li[2]').text
    pagenum = pagenum.replace("/", "")
    print("pagenum的数目为", pagenum)

    for n in range(int(pagenum)):

        time.sleep(7)

        # 该页所有学者的aminer主页链接
        # links = WebDriverWait(browser_1, 30).until(EC.presence_of_all_elements_located((By.XPATH,
        #                                                                              '/html/body/div[1]/section/main/main/article/div[2]/div[3]/div[1]/div[2]/div[1]/div[3]/div[3]/div[1]/div[1]/div//div[@class="person_name"]//*[@href]')))
        links = browser_1.find_elements_by_xpath('//*[@class="title_zone"]/div/h2/a')

        for span in links:
            try:
                count2 = 0
                while (1):
                    count2 = count2 + 1
                    # 如果确实有未知情况导致实在读取不到了，就放弃这个崽种
                    if(count2==30):
                        break
                    if (count2 >= 2):
                        print("现在在延迟")
                        time.sleep(2)
                    r = author_info_scratch(span.get_attribute("href"), discipline, disciplineid)
                    if (r != 1):
                        continue
                    if (r == 1):
                        break
            except:
                time.sleep(10)
                print("插入发生错误，延迟10秒")

        # 点击下一页
        next_bottom = browser_1.find_element_by_xpath(
            '//*[@id="root"]/section/section/main/div/div[3]/div/div[2]/div/div[1]/div/div[1]/div/div/ul/li[3]')
        next_bottom.click()

        print("爬取到了，现在页数：", n)


print("开始干活咯")
file = open('cardbox_urls.txt', 'r')
count1 = 1
links = file.readlines()
# 441行尾号为96的2021页数据有误，到500页就出不来东西了
# 从0开始，意味着初始数目为n-1
for span in range(594, 604):
    #     print(links[span])
    # for span in links:
    author_list(links[span], "华人库", "999")
    print("爬完一个cardbox拉,现在的cardbox编号为:", count1)
    count1 = count1 + 1
print("爬完所有cardbox拉")
