import pickle
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import random





driver = webdriver.Chrome()
driver.get('https://www.douban.com/accounts/login?source=main')
time.sleep(15)

timeInfo = {}
count = 0
for i in range(1000, 3000):
    url = 'https://www.douban.com/group/lovelydog/discussion?start=%s' % str(i*25)
    driver.get(url)
    page = driver.page_source
    soup = BeautifulSoup(page, "html5lib")
    timestamps = soup.find_all('td', {'class': 'time'})

    for item in timestamps:
        t = str(item).strip().replace('\n', '')
        t = re.sub('.*nowrap="nowrap">(.*?)</td>.*', '\\1', t)
        with open('dogTimeRecord_v2.txt', 'a') as file:
            file.write(t)
            file.write('\n')
    print(i)
    time.sleep(1.5)







