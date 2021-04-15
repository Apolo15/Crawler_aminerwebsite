import pymysql.cursors
import requests
import re
from bs4 import BeautifulSoup
import json
import time

connection = pymysql.connect(
        host='localhost',
        user='root',
        password='000000',
        db='aminer',
        charset='utf8mb4',
    )

cursor = connection.cursor()

sql = "SELECT * FROM people "
cursor.execute(sql)
results = cursor.fetchall()
# row代表一个作者
count=0
for row in results:
    name=row[3]
    title=row[4]
    papers=row[7]

    sql2="SELECT expertid FROM people WHERE name=%s AND title=%s AND papers=%s"
    val2=[name,title,papers]
    cursor.execute(sql2, val2)
    result =cursor.fetchall()
    # print(type(result))

    # print(result[1])
    for row in result:
        if(row!=result[0]):
            # num = re.findall('window.g_initialProps = (.*?});', str(two_string), re.S)
            num = re.findall('\((.*?),\)', str(row), re.S)
            sql3 = "DELETE FROM people WHERE expertid=%s"
            val3 = [num]
            cursor.execute(sql3, val3)
            count=count+1
            print("已经删除:"+str(count)+"    "+ str(num))
            # print(type(num))



    # sql2="UPDATE reader_collect_diary_combination SET time= %s WHERE id= %s"
    # val2=[t1,id]
    # cursor.execute(sql2,val2)
    # count=count+1
    # print("已经插入"+str(count))

connection.commit()