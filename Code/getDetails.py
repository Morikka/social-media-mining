'''
use the two databases I create in step 1:
CatPeople
DogPeople
to crawl each and everyone of them to get their habit

'''



import re
import os
from bs4 import BeautifulSoup
import urllib
import sqlite3
from selenium import webdriver
import time
import pandas as pd
import pickle
import random



def getCursor():
    conn = sqlite3.connect('CDPeopleDB.sqlite')
    cursor = conn.cursor()
    return cursor

def getAllUser(cursor):
    cursor.execute("select distinct * from DogPeople")
    return cursor.fetchall()



def getURLs(type, id):
    wishURL = 'https://%s.douban.com/people/%s/wish?start='%(type, id)
    doURL = 'https://%s.douban.com/people/%s/do?start='%(type, id)
    collectURL = 'https://%s.douban.com/people/%s/collect?start='%(type, id)
    return [wishURL, doURL, collectURL]


def getDriver():
    driver = webdriver.Chrome()
    return driver



# return a list of hyperlinks of movies
def getItems(type, soup):
    # soup = BeautifulSoup()
    if type == 'movie':
        items = soup.find_all('div', {'class': 'item'})
    else:
        items = soup.find_all('li', {'class': 'subject-item'})
    itemList = []
    for item in items:
        item = str(item).strip().replace('\n', '')
        item_id = re.sub(r'.*https://%s.douban.com/subject/(.*?)/.*'%type, '\\1', item)
        itemList.append(item_id)

    return itemList



#return ids of movies(tag: frequency)
def getList(type, driver, url_head):
    start = 0
    url = url_head + "%s&sort=rating&rating=all&filter=all&mode=grid"%start
    driver.get(url)
    page = driver.page_source
    soup = BeautifulSoup(page, "html5lib")
    itemNumber = soup.find_all('span', {'class': 'subject-num'})
    itemNumber = str(itemNumber[0]).replace("\n", '')
    totalNumber = int(re.sub(r".*\/\D*(\d+)\D*", '\\1', itemNumber))
    itemList = []
    time.sleep(1.5 + random.random())
    if totalNumber < 60:
        if totalNumber>0:
            start += 15
            itemList.extend(getItems(type, soup))
            totalNumber -= 15

        while(totalNumber>0):

            url = url_head + "%s&sort=rating&rating=all&filter=all&mode=grid"%start
            driver.get(url)
            page = driver.page_source
            soup = BeautifulSoup(page, "html5lib")
            itemList.extend(getItems(type, soup))
            start += 15
            totalNumber = totalNumber - 15
            time.sleep(1.5 + random.random())
    else:
        start += 15
        itemList.extend(getItems(type, soup))
        totalNumber -= 15

        i = 1
        while (totalNumber > 0 and i<4):
            url = url_head + "%s&sort=rating&rating=all&filter=all&mode=grid" % start
            driver.get(url)
            page = driver.page_source
            soup = BeautifulSoup(page, "html5lib")
            itemList.extend(getItems(type, soup))
            start += 15
            totalNumber = totalNumber - 15
            time.sleep(1.5 + random.random())
            i += 1

    return itemList


if __name__ == '__main__':
    cursor = getCursor()
    users = getAllUser(cursor)
    random.shuffle(users)   # randomly pick 2000 people
    driver = getDriver()
    driver.get('https://www.douban.com/accounts/login?source=main')
    time.sleep(15)
    count = 0
    userProfile = {}
    for i in range(len(users)):
        print("i = ", i)
        id = users[i][0]
        urls = getURLs(type='movie', id=id)
        movies = []
        movies.extend(getList('movie', driver, urls[0]))
        movies.extend(getList('movie', driver, urls[1]))
        movies.extend(getList('movie', driver, urls[2]))

        urls = getURLs(type='book', id=id)
        books = []
        books.extend(getList('book', driver, urls[0]))
        books.extend(getList('book', driver, urls[1]))
        books.extend(getList('book', driver, urls[2]))
        userProfile[id]={'movie': movies, 'book': books}

        if i % 100 == 0 and i != 0:
            with open('userMoviesBooks_DogPeople/record_%s.pickle' % count, 'wb') as file:
                pickle.dump(userProfile, file)
                userProfile = {}
            print('---------------------------------------', count, '---------------------------------------')
            count += 1

    with open('userMoviesBooks_DogPeople/record_%s.pickle' % count, 'wb') as file:
        pickle.dump(userProfile, file)
        userProfile = {}
        print('Successfully, end of the step 2!!!!!')


