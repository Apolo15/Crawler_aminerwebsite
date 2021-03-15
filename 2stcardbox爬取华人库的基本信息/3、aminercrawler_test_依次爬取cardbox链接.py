import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymysql.cursors
from selenium import webdriver  # 导入必要的库

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
browser_2 = webdriver.Chrome(executable_path=driver_path)

# 计数count，计算一共插入多少个author了(开始的专家id）
count = 194115
# 初始化浏览器，让他登陆和最大化，不然无法捕获所有元素
# browser.maximize_window()
browser_1.maximize_window()
browser_2.maximize_window()

# browser_2.get('https://www.aminer.cn/login?callback=profile%2Fthomas-s-huang%2F53f48abedabfaea6fb77b490')
# time.sleep(3)
# phonebtn=browser_2.find_element_by_xpath('/html/body/div/section/main/main/article/section/div[1]/div[2]/div/div[1]/div/div/div/div/div[1]/div[2]')
# phonebtn.click()
# username = browser_2.find_element_by_id('userPhone')
# username.clear()
# username.send_keys('18347989110')
# password = browser_2.find_element_by_id('phonePassword')
# password.clear()
# password.send_keys('aminer9110')
# loginbtn = browser_2.find_element_by_xpath(
#     '/html/body/div/section/main/main/article/section/div[1]/div[2]/div/div[3]/div[2]/form/div/div[5]/div/div/span/button')
# loginbtn.click()
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
    browser_2.get(url)
    time.sleep(2)
    # handle = browser_2.current_window_handle
    handles = browser_2.window_handles
    handle=handles[0]
    for newhandle in handles:
        if newhandle != handle:
            browser_2.switch_to.window(newhandle)
            browser_2.close()
    browser_2.switch_to.window(handle)



    # 作者的各项资料
    try:

        name = WebDriverWait(browser_2, 30).until(EC.presence_of_element_located(
            (By.XPATH,
             '//*[@id="market_content"]/div/div/div/div[1]/div[1]/div/div/div[2]/div[1]/h1/span'))).text
        # ——————————————————————————————————————————————————————————————————————————————
        # name = browser_2.find_element_by_xpath(
        #     '/html/body/div/section/main/main/article/section[1]/section[1]/div[1]/div/div[2]/div[1]/h1/span').text
    except:
        # return 0
        name = "no name"

    try:
        # title = WebDriverWait(browser_2, 3).until(EC.presence_of_element_located(
        #     (By.XPATH,
        #      '/html/body/div/section/main/main/article/section[1]/section[1]/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/p[1]/span'))).text
        # ——————————————————————————————————————————————————————————————————————————————
        title = browser_2.find_element_by_xpath(
            '//*[@id="market_content"]/div/div/div/div[1]/div[1]/div/div/div[2]/div[3]/div/div[1]/div[1]/div/span').text
    except:
        title = "no title"

    try:
        # department = WebDriverWait(browser_2, 3).until(EC.presence_of_element_located(
        #     (By.XPATH,
        #      '/html/body/div/section/main/main/article/section[1]/section[1]/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/p[2]/textarea'))).text
        # ——————————————————————————————————————————————————————————————————————————————
        department = browser_2.find_element_by_xpath(
            '//*[@id="market_content"]/div/div/div/div[1]/div[1]/div/div/div[2]/div[3]/div/div[1]/div[2]/div/span').text
    except:
        department = "no department"

    try:
        # url_list = re.findall('"url":\"(.*?)\"', browser_2.page_source, re.S)
        # homepage=[]
        # for url in url_list:
        #     homepage=homepage+[url.replace("\\u002F", "/")]
        # ——————————————————————————————————————————————————————————————————————————————
        # details = WebDriverWait(browser_2, 3).until(EC.presence_of_element_located(
        #     (By.XPATH,
        #      '//*[@class="expert_info_content"]')))
        # ——————————————————————————————————————————————————————————————————————————————
        # details = browser_2.find_element_by_xpath('//*[@class="expert_info_content"]')
        # homepage = details.find_elements_by_xpath('//*[@class="homepage baseInfo"]')
        # h = ''
        # for url in homepage:
        #     h = h + url.text + ' '
        #     # print(h)
        # homepage = h
        # ——————————————————————————————————————————————————————————————————————————————
        homepage=browser_2.find_element_by_xpath('//*[@id="market_content"]/div/div/div/div[1]/div[1]/div/div/div[2]/div[3]/div/div[1]/div[4]/div/a').text
    except:
        homepage = "no homepage"

    try:
        # papers = WebDriverWait(browser_2, 3).until(EC.presence_of_element_located(
        #     (By.XPATH,
        #      '//*[@id="popover_radar"]/div[2]/p[1]/span[2]'))).text
        # ——————————————————————————————————————————————————————————————————————————————
        # papers = re.findall('"pubs":(.*?)}', browser_2.page_source, re.S)
        # ——————————————————————————————————————————————————————————————————————————————
        papers = browser_2.find_elements_by_xpath('//*[@class="num"]')
        papers=papers[0].text
    except:
        papers = "no papers"

    try:
        # citation = WebDriverWait(browser_2, 3).until(EC.presence_of_element_located(
        #     (By.XPATH,
        #      '//*[@id="popover_radar"]/div[2]/p[2]/span[2]'))).text
        # ——————————————————————————————————————————————————————————————————————————————
        citation = browser_2.find_elements_by_xpath('//*[@class="num"]')
        citation=citation[1].text
        # ——————————————————————————————————————————————————————————————————————————————
        # citation = re.findall('"citations":(.*?),', browser_2.page_source, re.S)
    except:
        citation = "no citation"

    try:
        # hindex = WebDriverWait(browser_2, 3).until(EC.presence_of_element_located(
        #     (By.XPATH,
        #      '//*[@id="popover_radar"]/div[2]/p[3]/span[2]'))).text
        # ——————————————————————————————————————————————————————————————————————————————
        hindex = browser_2.find_elements_by_xpath('//*[@class="num"]')
        hindex=hindex[2].text
        # ——————————————————————————————————————————————————————————————————————————————
        # hindex = re.findall('"hindex":(.*?),', browser_2.page_source, re.S)
    except:
        hindex = "no hindex"

    try:
        # interests = WebDriverWait(browser_2, 3).until(EC.presence_of_all_elements_located(
        #     (By.CLASS_NAME,
        #      "nv-legend-text")))
        # ——————————————————————————————————————————————————————————————————————————————
        interests = browser_2.find_elements_by_class_name("nv-legend-text")
        interests_list = ''
        for span in interests:
            interests_list = interests_list + span.text + ','
        interests = interests_list
    except:
        interests = "no interests"

    author = Author(name, title, department, homepage, papers, citation, hindex, interests)
    author.print()

    insert_mysql(author, discipline, disciplineid)
    return 1


# 挨个点击【作者列表】，进入【个人主页】后调用author_info_scratch
def author_list(url, discipline, disciplineid):
    browser_1.get(url)
    time.sleep(2)
    pagenum = WebDriverWait(browser_1, 100).until(EC.presence_of_element_located((By.CLASS_NAME,'ant-pagination-simple-pager'))).text
    # pagenum = browser_1.find_element_by_xpath(
    #     '/html/body/div/section/main/main/article/div[2]/div[3]/div[1]/div[2]/div[1]/div[3]/div[2]/div[2]/ul/li[2]').text
    pagenum = pagenum.replace("/", "")
    print("pagenum的数目为", pagenum)

    for n in range(int(pagenum)):

        time.sleep(20)

        # 该页所有学者的aminer主页链接
        # links = WebDriverWait(browser_1, 30).until(EC.presence_of_all_elements_located((By.XPATH,
        #                                                                              '/html/body/div[1]/section/main/main/article/div[2]/div[3]/div[1]/div[2]/div[1]/div[3]/div[3]/div[1]/div[1]/div//div[@class="person_name"]//*[@href]')))
        links = browser_1.find_elements_by_xpath('//*[@class="title_zone"]/div/h2/a')

        for span in links:
            try:
                count2=0
                while(1):
                    count2=count2+1
                    if(count2>=2):
                        print("现在在延迟")
                    if(author_info_scratch(span.get_attribute("href"), discipline, disciplineid)==1):
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
count1=1
links=file.readlines()
#441行尾号为96的2021页数据有误，到500页就出不来东西了
#从0开始，意味着初始数目为n-1
for span in range(594,604):
#     print(links[span])
# for span in links:
    author_list(links[span],"华人库","999")
    print("爬完一个cardbox拉,现在的cardbox编号为:",count1)
    count1=count1+1
print("爬完所有cardbox拉")