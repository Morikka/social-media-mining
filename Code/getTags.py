import pickle
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import re




def getDriver():
    driver = webdriver.Chrome()
    return driver


def prepareMovieAndBookId():
    movieIdSet = set()
    bookIdSet = set()


    for i in range(20):

        fileName = 'userMoviesBooks_CatPeople/record_%s.pickle'%i

        with open(fileName, 'rb') as file:
            users = pickle.load(file)

        for key in users.keys():
            movies = users[key]['movie']
            if len(movies)!=0:
                for item in movies:
                    movieIdSet.add(item)
            books = users[key]['book']
            if len(books)!=0:
                for item in books:
                    bookIdSet.add(item)

    for i in range(20):

        fileName = 'userMoviesBooks_DogPeople/record_%s.pickle'%i

        with open(fileName, 'rb') as file:
            users = pickle.load(file)

        for key in users.keys():
            movies = users[key]['movie']
            if len(movies)!=0:
                for item in movies:
                    movieIdSet.add(item)
            books = users[key]['book']
            if len(books) != 0:
                for item in books:
                    bookIdSet.add(item)

    with open('raw data/movies.pickle', 'wb') as file:
        pickle.dump(movieIdSet, file)

    with open('raw data/books.pickle', 'wb') as file:
        pickle.dump(bookIdSet, file)

    print(len(movieIdSet))  #13048
    print('---------------')
    print(len(bookIdSet))   #19683


# prepareMovieAndBookId()

def getTags(type):

    with open('raw data/%s.pickle'%type, 'rb') as file:
        itemIdSet = pickle.load(file)

    driver = webdriver.Chrome()

    driver.get('https://www.douban.com/accounts/login?source=main')

    time.sleep(15)

    itemIdList = list(itemIdSet)

    count = 0

    Result = {}

    for i in range(count*100+1, len(itemIdList)):

        time.sleep(2.6)

        if type == 'movies':
            url = r'https://movie.douban.com/subject/%s' % itemIdList[i]
        else:
            url = r'https://book.douban.com/subject/' % itemIdList[i]
        try:
            driver.get(url)
            page = driver.page_source
            soup = BeautifulSoup(page, "html5lib")
            tag = soup.find_all('span', {'property': 'v:genre'})
            temp = []
            if len(tag) != 0:
                for item in tag:
                    regex = r'<span property="v:genre">(.*?)\</span>'
                    temp.append(re.sub(regex, "\\1", str(item).strip()))
                Result[itemIdList[i]] = temp

        except Exception as e:
            with open('%sError.log' % type, 'a') as f:
                f.write(str(i)+'\t'+str(itemIdList[i])+'\t'+str(e)+'\n')

        if i % 10 == 0 and i != 0:
            print(i)

        if i % 100 == 0 and i != 0:
            print('-------------count--------------')
            print(count)
            print('-------------count--------------')
            with open('raw data/movieTags/%sTags_%s.pickle' % (type, str(count)), 'wb') as file:
                pickle.dump(Result, file)
            Result = {}
            count += 1

    with open('raw data/movieTags/%sTags_%s.pickle' % (type, str(count)), 'wb') as file:
        pickle.dump(Result, file)

    print('get all %s tags' % type)



getTags('movies')














