import pickle
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import random




with open('userMoviesBooks_%sPeople/userId.pickle' % 'Dog', 'rb') as file:
    dogIds = pickle.load(file)

driver = webdriver.Chrome()
driver.get('https://www.douban.com/accounts/login?source=main')
time.sleep(15)

followInfo = {}
count = 3
for i in range(count*200+1, len(dogIds)):
    url = 'https://www.douban.com/people/%s/'%dogIds[i]
    driver.get(url)
    page = driver.page_source
    soup = BeautifulSoup(page, "html5lib")
    content = str(soup.contents).strip().replace('\n', '')
    if re.match(".*成员(\d+)</a.*", content) is not None:
        followN = re.sub(".*成员(\d+)</a.*", "\\1", content)
    else:
        followN = 0
    if re.match(".*(\d+)人关注.*", content) is not None:
        followerN = re.sub(".*(\d+)人关注.*", "\\1", content)
    else:
        followerN = 0
    if re.match(".*常去的小组\((\d+)\).*", content) is not None:
        group = re.sub(".*常去的小组\((\d+)\).*", "\\1", content)
    else:
        group = 0

    followInfo[dogIds[i]] = [followN, followerN, group]

    print(i, '----------', dogIds[i], '--------', followInfo[dogIds[i]])
    time.sleep(1.5+random.random())
    if i % 200 == 0 and i != 0:
        with open('raw data/followInfo_%s.pickle' % count, 'wb') as file:
            pickle.dump(followInfo, file)
            followInfo = {}
            count += 1


with open('raw data/followInfo_%s.pickle' % count, 'wb') as file:
    pickle.dump(followInfo, file)

print('all finished')










