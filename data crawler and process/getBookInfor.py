import pickle
import re
import pandas as pd
import numpy as np


def prepareTags():
    allTags = set()
    count = 0

    for i in range(197):
        path = 'raw data/bookTags/booksTags_%s.pickle'%str(i)
        with open(path, 'rb') as file:
            data = pickle.load(file)

        for key in data.keys():
            for item in data[key][:1]:
                allTags.add(item)
            count += 1
    with open('raw data/bookTags.pickle', 'wb') as file:
        pickle.dump(list(allTags), file)
    print(len(allTags))
    print(count)


# prepareTags() # 19558 books    #3840 Tags


def getBookDataFrame():
    with open('raw data/bookTags.pickle', 'rb') as file:
        indexes = list(pickle.load(file))

    # valid number of books with tag information is 14061

    bookMatrix = np.zeros((3840, 14061))
    books = list()
    count = 0
    for i in range(197):
        path = 'raw data/bookTags/booksTags_%s.pickle' % str(i)
        with open(path, 'rb') as file:
            data = pickle.load(file)

        for key in data.keys():
            if key not in books:
                if len(data[key]) > 0:
                    for item in data[key]:
                        try:
                            bookMatrix[indexes.index(item)][count] += 1
                        except:
                            continue

                    books.append(key)
                    count += 1
    bookDataFrame = pd.DataFrame(bookMatrix, indexes, books)
    # save the information for each film
    # bookDataFrame.to_csv('raw data/bookInfomation.csv')
    # with open('raw data/bookDataFrame.pickle', 'wb') as file:
    #     pickle.dump(bookDataFrame, file)
    return bookDataFrame, indexes




def getUserIds(type):
    userId = set()

    for i in range(20):
        with open('userMoviesBooks_%sPeople/record_%s.pickle'%(type, str(i)), 'rb') as file:
            data = pickle.load(file)
        for key in data.keys():
            userId.add(key)
    userId = list(userId)
    with open('userMoviesBooks_%sPeople/userId.pickle'%type, 'wb') as file:
        pickle.dump(userId, file)

def getMatrix(type):

    #type == Dog/Cat

    df, indexes = getBookDataFrame()
    with open('userMoviesBooks_%sPeople/userId.pickle' % type, 'rb') as file:
        userIds = pickle.load(file)

    PeopleDataFrame = pd.DataFrame(np.zeros((3840, 2001)), indexes, userIds)
    count = 0
    for i in range(20):
        with open('userMoviesBooks_%sPeople/record_%s.pickle' % (type, str(i)), 'rb') as file:
            data = pickle.load(file)

        for key in data.keys():
            bookList = data[key]['book']

            if len(bookList) != 0:
                k = len(bookList)
                likes = []
                for item in bookList:
                    try:
                        likes.append(df[item])
                    except:
                        pass
                if len(likes) != 0:
                    PeopleDataFrame[key] = sum(likes)/k
                    count += 1
                else:
                    del PeopleDataFrame[key]

            else:
                del PeopleDataFrame[key]


    print(count)
    PeopleDataFrame = PeopleDataFrame.transpose()
    # print("%sPeople has %s "%(type, str(count)))
    PeopleDataFrame.to_csv('TrainingData/%sPeopleBook_normalized.csv'%type)
    return PeopleDataFrame

# getUserIds('Dog')
getMatrix('Dog')
# getUserIds('Cat')
getMatrix('Cat')


'''

DogPeople has 1350 
CatPeople has 1283 


'''

