import time
from selenium import webdriver  # 导入必要的库
from selenium.webdriver.support import expected_conditions as EC

option = webdriver.ChromeOptions()
option.add_argument("headless")
# chromedriver.exe的存放路径
driver_path = 'E:\zhangxu\pythonanzhuang\python-3.9\Scripts\chromedriver.exe'

# 通过webdriver对象的Chrome方法【不同的浏览器对应不同的方法】，获取到chromedriver.exe

browser_2 = webdriver.Chrome(executable_path=driver_path, chrome_options=option)
browser_1 = webdriver.Chrome(executable_path=driver_path, chrome_options=option)
# browser = webdriver.Chrome(executable_path=driver_path, chrome_options=option)


# browser_2 = webdriver.Chrome(executable_path=driver_path)
# browser_1 = webdriver.Chrome(executable_path=driver_path)
browser = webdriver.Chrome(executable_path=driver_path)



class Author:
    def __init__(self, title, position, employer, homepage, experience, interests_list):
        self.title = title
        self.position = position
        self.employer = employer
        self.homepage = homepage
        self.experience = experience
        self.interests_list = interests_list

    def print(self):
        print(self.title, self.position, self.employer, self.homepage, self.experience, self.interests_list)

    def f1(self):
        return True


# 抓取【个人主页】的详细信息
def author_info_scratch(url):
    browser_2.get(url)
    time.sleep(5)

    # print("主窗口",mainwindow)
    # print("切换过来的窗口",browser.current_window_handle)
    # page = browser.page_source

    # 作者的各项资料
    try:
        title = browser_2.find_element_by_xpath(
            '/html/body/div[1]/section/section/main/div/article/div/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/h1').text
    except:
        title = "no title"

    try:
        position = browser_2.find_element_by_xpath(
            '/html/body/div[1]/section/section/main/div/article/div/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/div/div[1]/div[1]/p/span').text

    except:
        position = "no position"

    try:
        employer = browser_2.find_element_by_xpath(
            '/html/body/div[1]/section/section/main/div/article/div/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/div/div[1]/div[2]/p/span').text
    except:
        employer = "no employer"

    try:

        homepage = browser_2.find_element_by_xpath(
            '/html/body/div[1]/section/section/main/div/article/div/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/div/div[1]/div[5]/p/a').text
    except:
        homepage = "no homepage"

    try:
        experience = browser_2.find_element_by_xpath(
            '/html/body/div[1]/section/section/main/div/article/div/div/div[3]/div[1]/div[2]/div[1]/div[2]/div/div/ul/li/div/div').text

    except:
        experience = "no experience"

    try:
        interests = browser_2.find_elements_by_class_name("nv-legend-text")
        interests_list = []
        for span in interests:
            interests_list = interests_list + [span.text]
            # print(interests_list)
    except:
        interests_list = ["no interests"]

    author = Author(title, position, employer, homepage, experience, interests_list)
    author.print()

    # browser.switch_to.window(mainwindow)
    # print(browser.current_window_handle)
    time.sleep(2)

    # print(page)
    # print(interests)


# 挨个点击【作者列表】，进入【个人主页】后调用author_info_scratch
def author_list(url):
    browser_1.get(url)
    for num in range(6):
        # browser.switch_to.window(browser.window_handles[num])
        # print("当前浏览器地址:",browser.current_url)
        time.sleep(2)

        # mainwindow=browser.current_window_handle
        # browser.switch_to.window(mainwindow)
        # print(mainwindow)



        links = browser_1.find_elements_by_xpath(
            '/html/body/div[1]/section/section/main/div/div[3]/div/div[2]/div/div[2]/div[2]/div[1]/div//*[@href]')

        for span in links:
            # rightnowwindow=browser.current_window_handle
            # print("rightnowwindow:",rightnowwindow)

            print(span.get_attribute("href"))
            author_info_scratch(span.get_attribute("href"))

        a = browser_1.find_element_by_xpath(
            '//*[@id="root"]/section/section/main/div/div[3]/div/div[2]/div/div[2]/div[2]/div[2]/ul/li[9]/a')
        a.click()

        print("a爬取到了", num)


# 挨个点击【系列库】，进入【作者列表】后调用author_list
def library_list(url):
    browser.get(url)

    time.sleep(2)
    main_window=browser.current_window_handle
    fo=open("C:/Users/ZL/Desktop/test.txt","w")
    # for num in range(0):
    #     print(num)
    a = browser.find_element_by_xpath(
        '/html/body/div/section/section/main/div/div[2]/div/div/div/div/div/div[1]/div/a[1]')
    a.click()
    # print(browser.current_url)
    a = browser.find_element_by_xpath(
        '/html/body/div/section/section/main/div/div[2]/div/div/div/div/div/div[1]/div/a[2]')
    a.click()
    # print(browser.current_url)

    all_handles =browser.window_handles

    for handle in all_handles:
        if handle != main_window:
            browser.switch_to.window(handle)
            fo.write(browser.current_url+'\n')


    "这里再用for循环，把之前写入文件的地址，拿出来给browser1一个一个拿过去解析"


        # libraries=browser.find_elements_by_xpath('//*[@id="root"]/section/section/main/div/div[2]/div/div/div/div/div/div[1]/div/a[4]')

        # print(libraries)
        # for span in libraries:
        #     print(span)
        # a = browser_1.find_element_by_class_name(span)
        # a.click()
        # print(span.text)
        # author_list(span.get_attribute("href"))

        # a = browser.find_element_by_xpath(
        #     '//*[@id="root"]/section/section/main/div/div[3]/div/div[2]/div/div[2]/div[2]/div[2]/ul/li[9]/a')
        # a.click()

        # print("a爬取到了", num)


# 测试作者信息爬取demo
author_info_scratch("https://gct.aminer.cn/eb/profile/56cb18a3c35f4f3c656585bf")
# 测试爬取一页作者的信息demo
# author_list('https://gct.aminer.cn/eb/gallery/detail/eb/5d525f7a530c70a9b3631ecf')
# author_info_scratch('https://gct.aminer.cn/eb/profile/56cb18a3c35f4f3c656585bf')
# author_info_scratch('https://gct.aminer.cn/eb/profile/56cb18adc35f4f3c6565b217')
# author_info_scratch('https://gct.aminer.cn/eb/profile/5602ba9045cedb33960282cd')
# author_info_scratch('https://gct.aminer.cn/eb/profile/542dc733dabfae11fc49f3fe')

# 测试爬取一整块系列库
# library_list('https://gct.aminer.cn/eb/gallery?check=all')
