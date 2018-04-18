
'''
step 1
get the userID and their locations
put them all into a database
'''

from bs4 import BeautifulSoup
import urllib
import sqlite3
from selenium import webdriver
import time
import re
from urllib import request
import random
import pickle
import os
import pytesseract





url_dog = "https://www.douban.com/group/lovelydog/members?start="

url_cat = "https://www.douban.com/group/cat/members?start="

'''
cat = 1 ~ 336770
dog = 1 ~ 156240
            '''
class getInfo(object):

    memberList = []
    type = None
    url = None
    memberNumber = 0
    conn = None
    cursor = None

    def __init__(self, type):
        getInfo.type = type

        if type == "cat":
            getInfo.url = url_cat
            getInfo.memberNumber = 336770
        else:
            getInfo.url = url_dog
            getInfo.memberNumber = 156240

        dbName = "CDPeopleDB.sqlite"

        #iniate the start point
        if not os.path.isfile('stopPoint.pickle'):
            with open('stopPoint.pickle', 'rb') as file:
                pickle.dump(1, file)

        conn = sqlite3.connect(dbName)
        getInfo.conn = conn

        getInfo.cursor = getInfo.conn.cursor()


        # if getInfo.type == 'dog':
        #     getInfo.cursor.execute("drop table if exists DogPeople")
        #     getInfo.cursor.execute("create table DogPeople(id varchar(48), location varchar(48))")
        # else:
        #     getInfo.cursor.execute("drop table if exists CatPeople")
        #     getInfo.cursor.execute("create table CatPeople(id varchar(48), location varchar(48))")


    def sliceContent(self, pageContent):
        pageContent = re.sub(r"<ul>(.*)</ul>", "\\1", pageContent.replace("\n", ""))
        # print(pageContent)
        memberList = re.sub(r'<li class=""> (.*?) </li>', "\\1mark", pageContent.strip())
        memberList = re.split(r"mark", memberList)
        inforContent = re.findall(r'<div class="name">(.*?)</div>', memberList[35])
        for member in memberList:
            if member.strip() != '':
                inforContent = re.findall(r'<div class="name">(.*?)</div>', member)
                if len(inforContent)!= 0:
                    inforContent = inforContent[0].strip()
                    identity = re.findall(r'https://www.douban.com/people/(.*?)/', inforContent)[0]
                    if len(identity)!=0:
                        id = identity[0]
                        location = re.findall(r'<span class="pl">\((.*?)\)</span>', inforContent)
                        if len(location) != 0:
                            coordinate = str(location[0])
                        else:
                            coordinate = 'Unknown'
                    else:
                        continue
                if getInfo.type == 'dog':
                    getInfo.cursor.execute("insert into DogPeople values(?, ?)", (id, coordinate))
                else:
                    getInfo.cursor.execute("insert into CatPeople values(?, ?)", (id, coordinate))
        getInfo.conn.commit()






    def crawler(self):

        opener = urllib.request.build_opener(urllib.request.HTTPSHandler)
        header = ("User-Agent",
                  " Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        opener.addheaders = [header]
        driver = webdriver.Chrome()
        driver.get(getInfo.url)
        time.sleep(20)

        #store the current position in case there is something wrong with the crawlering
        with open('stopPoint.pickle', 'rb') as file:
            startPoint = pickle.load(file)

        #use the record to be the start position
        for i in range(startPoint, getInfo.memberNumber, 35):
            driver.get(getInfo.url+str(i))
            page = driver.page_source
            soup = BeautifulSoup(page, "html5lib")
            print(i)
            with open('stopPoint.pickle', 'wb') as file:
                pickle.dump(i, file)
            memberList = soup.find('div', {'class': 'member-list'}).ul
            content = str(memberList)
            getInfo.sliceContent(self, pageContent=content)
            time.sleep(2+random.random())

# info_dog = getInfo("dog")
# info_dog.crawler()
info_cat = getInfo("cat")
info_cat.crawler()


'''
create table CatPeople
as
select distinct * 
from CatPeople_backup
WHERE not location GLOB '*[A-Za-z]*';

pre-processing to delete locations out of China

'''




