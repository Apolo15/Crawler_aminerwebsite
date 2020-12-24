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

browser = webdriver.Chrome(executable_path=driver_path)
# browser_1 = webdriver.Chrome(executable_path=driver_path)
# browser_2 = webdriver.Chrome(executable_path=driver_path)

# 计数count，计算一共插入多少个author了
# count = 22494

# 初始化浏览器，让他登陆和最大化，不然无法捕获所有元素
browser.maximize_window()
# browser_1.maximize_window()
# browser_2.maximize_window()
# browser_2.get('https://www.aminer.cn/login?callback=profile%2Fthomas-s-huang%2F53f48abedabfaea6fb77b490')
# username = browser_2.find_element_by_id('userPhone')
# username.clear()
# username.send_keys('18347989110')
# password = browser_2.find_element_by_id('phonePassword')
# password.clear()
# password.send_keys('aminer9110')
# loginbtn = browser_2.find_element_by_xpath(
#     '//*[@class="ant-btn a-aminer-core-auth-c-login-login-loginBtn a-aminer-core-auth-c-login-login-ready loginBtn"]')
# loginbtn.click()
time.sleep(3)


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
    # time.sleep(3)

    # 作者的各项资料
    try:

        name = WebDriverWait(browser_2, 30).until(EC.presence_of_element_located(
            (By.XPATH,
             '/html/body/div/section/main/main/article/section[1]/section[1]/div[1]/div/div[2]/div[1]/h1/span'))).text
        # ——————————————————————————————————————————————————————————————————————————————
        # name = browser_2.find_element_by_xpath(
        #     '/html/body/div/section/main/main/article/section[1]/section[1]/div[1]/div/div[2]/div[1]/h1/span').text
    except:
        name = "no name"

    try:
        # title = WebDriverWait(browser_2, 3).until(EC.presence_of_element_located(
        #     (By.XPATH,
        #      '/html/body/div/section/main/main/article/section[1]/section[1]/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/p[1]/span'))).text
        # ——————————————————————————————————————————————————————————————————————————————
        title = browser_2.find_element_by_xpath(
            '/html/body/div/section/main/main/article/section[1]/section[1]/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/p[1]/span').text
    except:
        title = "no title"

    try:
        # department = WebDriverWait(browser_2, 3).until(EC.presence_of_element_located(
        #     (By.XPATH,
        #      '/html/body/div/section/main/main/article/section[1]/section[1]/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/p[2]/textarea'))).text
        # ——————————————————————————————————————————————————————————————————————————————
        department = browser_2.find_element_by_xpath(
            '/html/body/div/section/main/main/article/section[1]/section[1]/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/p[2]/textarea').text
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
        details = browser_2.find_element_by_xpath('//*[@class="expert_info_content"]')
        homepage = details.find_elements_by_xpath('//*[@class="homepage baseInfo"]')
        h = ''
        for url in homepage:
            h = h + url.text + ' '
            # print(h)
        homepage = h
    except:
        homepage = "no homepage"

    try:
        # papers = WebDriverWait(browser_2, 3).until(EC.presence_of_element_located(
        #     (By.XPATH,
        #      '//*[@id="popover_radar"]/div[2]/p[1]/span[2]'))).text
        # ——————————————————————————————————————————————————————————————————————————————
        # papers = re.findall('"pubs":(.*?)}', browser_2.page_source, re.S)
        # ——————————————————————————————————————————————————————————————————————————————
        papers = browser_2.find_element_by_xpath('//*[@id="popover_radar"]/div[2]/p[1]/span[2]').text
    except:
        papers = "no papers"

    try:
        # citation = WebDriverWait(browser_2, 3).until(EC.presence_of_element_located(
        #     (By.XPATH,
        #      '//*[@id="popover_radar"]/div[2]/p[2]/span[2]'))).text
        # ——————————————————————————————————————————————————————————————————————————————
        citation = browser_2.find_element_by_xpath('//*[@id="popover_radar"]/div[2]/p[2]/span[2]').text
        # ——————————————————————————————————————————————————————————————————————————————
        # citation = re.findall('"citations":(.*?),', browser_2.page_source, re.S)
    except:
        citation = "no citation"

    try:
        # hindex = WebDriverWait(browser_2, 3).until(EC.presence_of_element_located(
        #     (By.XPATH,
        #      '//*[@id="popover_radar"]/div[2]/p[3]/span[2]'))).text
        # ——————————————————————————————————————————————————————————————————————————————
        hindex = browser_2.find_element_by_xpath('//*[@id="popover_radar"]/div[2]/p[3]/span[2]').text
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


# 挨个点击【作者列表】，进入【个人主页】后调用author_info_scratch
def author_list(url, discipline, disciplineid):
    browser_1.get(url)

    pagenum = WebDriverWait(browser_1, 30).until(EC.presence_of_element_located((By.XPATH,
                                                                                 '/html/body/div/section/main/main/article/div[2]/div[3]/div[1]/div[2]/div[1]/div[3]/div[2]/div[2]/ul/li[2]'))).text
    # pagenum = browser_1.find_element_by_xpath(
    #     '/html/body/div/section/main/main/article/div[2]/div[3]/div[1]/div[2]/div[1]/div[3]/div[2]/div[2]/ul/li[2]').text
    pagenum = pagenum.replace("/", "")
    print("pagenum的数目为", pagenum)

    for n in range(int(pagenum)):

        time.sleep(20)

        # 该页所有学者的aminer主页链接
        # links = WebDriverWait(browser_1, 30).until(EC.presence_of_all_elements_located((By.XPATH,
        #                                                                              '/html/body/div[1]/section/main/main/article/div[2]/div[3]/div[1]/div[2]/div[1]/div[3]/div[3]/div[1]/div[1]/div//div[@class="person_name"]//*[@href]')))
        links = browser_1.find_elements_by_xpath(
            '/html/body/div[1]/section/main/main/article/div[2]/div[3]/div[1]/div[2]/div[1]/div[3]/div[3]/div[1]/div[1]/div//div[@class="person_name"]//*[@href]')

        for span in links:
            # print(span.get_attribute("href"))
            try:
                author_info_scratch(span.get_attribute("href"), discipline, disciplineid)
            except:
                time.sleep(10)
                print("数据延迟，等待10秒")

        # 点击下一页
        next_bottom = browser_1.find_element_by_xpath(
            '/html/body/div[1]/section/main/main/article/div[2]/div[3]/div[1]/div[2]/div[1]/div[3]/div[2]/div[2]/ul/li[3]')
        next_bottom.click()

        print("爬取到了，现在页数：", n)


# cardbox列表获取，进去之后调用author_list
def cardbox_list(url):

    count = 1
    file = open('cardbox_urls.txt', 'a')
    browser.get(url)
    for n in range(0, 30):
        # 获取所有的cardbox的链接
        time.sleep(5)
        links = WebDriverWait(browser, 30).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'antd-pro-components-eb-gallery-e-b-gallery-cardBox')))
        # links = browser.find_elements_by_class_name('antd-pro-components-eb-gallery-e-b-gallery-cardBox')
        for span in links:
            try:
                span.click()
                handle = browser.current_window_handle
                handles = browser.window_handles
                for newhandle in handles:
                    if newhandle != handle:
                        browser.switch_to.window(newhandle)
                        url = browser.current_url
                        file.write(url+"\n")
                        browser.close()
                        browser.switch_to.window(handle)
                        print("已获取cardbox数量", count)
                        count = count + 1
            except:
                time.sleep(10)
                print("数据延迟，等待10秒")
                file.close()

        # 点击下一页
        next_bottom = browser.find_element_by_class_name('ant-pagination-next')
        next_bottom.click()

        print("cardbox爬取到了，现在页数：", n)
    print("所有页数爬完了，写入文件")
    file.close()

# 测试作者信息爬取demo
# author_info_scratch("https://www.aminer.cn/profile/h-vincent-poor/54055927dabfae8faa5c5dfa","测试",111)
# 测试爬取一页作者的信息demo
# author_list('https://www.aminer.cn/search/person?domain=143&t=b','急急急',111)#计算机科学


# print("所有的都执行完毕啦~")
cardbox_list('https://gct.aminer.cn/eb/gallery?check=all')
