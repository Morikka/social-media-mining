import pickle
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np



import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier



def prepareColumns():
    allTags = set()
    count = 0
    for i in range(131):
        path = 'raw data/movieTags/moviesTags_%s.pickle'%str(i)
        with open(path, 'rb') as file:
            data = pickle.load(file)

        for key in data.keys():
            for item in data[key]:
                allTags.add(item)
            count += 1
    with open('raw data/movieTags.pickle', 'wb') as file:
        pickle.dump(list(allTags), file)
    print(count)


# prepareColumns()

def getMovieDataFrame():
    with open('raw data/movieTags.pickle', 'rb') as file:
        columns = list(pickle.load(file))

    # valid number of movies is 12726

    movieMatrix = np.zeros((41, 12726))
    movies = list()
    count = 0
    for i in range(131):
        path = 'raw data/movieTags/moviesTags_%s.pickle' % str(i)
        with open(path, 'rb') as file:
            data = pickle.load(file)

        for key in data.keys():
            for item in data[key]:
                movieMatrix[columns.index(item)][count] += 1
            movies.append(key)
            count += 1

    movieDataFrame = pd.DataFrame(movieMatrix, columns, movies)
    return movieDataFrame, columns

    # save the information for each film
    # movieDataFrame.to_csv('raw data/movieInfomation.csv')

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

def getFriend(type):
    followInfo = {}

    for i in range(10):
        if type == 'Cat':
            path = r'raw data\catfollow\CatfollowInfo_%s.pickle' % str(i)
        else:
            path = r'raw data\dogfollow\followInfo_%s.pickle' % str(i)
        with open(path, 'rb') as file:
            data = pickle.load(file)
        for key in data.keys():
            followInfo[key] = data[key]
    return followInfo



def getMatrix(type):

    #type == Dog/Cat

    df, columnNames = getMovieDataFrame()

    with open('userMoviesBooks_%sPeople/userId.pickle'%type, 'rb') as file:
        userIds = pickle.load(file)


    PeopleDataFrame = pd.DataFrame(np.zeros((41, 2001)), columnNames, userIds)
    count = 0
    defaultValue = 1/37
    for i in range(20):

        with open('userMoviesBooks_%sPeople/record_%s.pickle' % (type, str(i)), 'rb') as file:
            data = pickle.load(file)

        for key in data.keys():
            movieList = data[key]['movie']

            if len(movieList) != 0:
                k = len(movieList)
                likes = []
                for item in movieList:
                    try:
                        likes.append(df[item])
                    except:
                        pass
                if len(likes)!=0:
                    PeopleDataFrame[key] = sum(likes)/k
                    # count += 1
                else:
                    # del PeopleDataFrame[key]
                    PeopleDataFrame[key] = defaultValue
            else:
                # del PeopleDataFrame[key]
                PeopleDataFrame[key] = defaultValue

    # regularizer = PeopleDataFrame.apply(sum)
    #
    # for key in PeopleDataFrame.columns:
    #     PeopleDataFrame[key] /= regularizer[key]
    # deValue = 1/41

    print(count)
    PeopleDataFrame = PeopleDataFrame.transpose()
    PeopleDataFrame['纪录片'] = PeopleDataFrame['紀錄片 Documentary'] + PeopleDataFrame['纪录片'] + PeopleDataFrame['记录']
    del PeopleDataFrame['紀錄片 Documentary']
    del PeopleDataFrame['记录']
    PeopleDataFrame['真人秀'] = PeopleDataFrame['Reality-TV'] + PeopleDataFrame['真人秀']
    del PeopleDataFrame['Reality-TV']
    PeopleDataFrame['脱口秀'] = PeopleDataFrame['Talk-Show'] + PeopleDataFrame['脱口秀']
    del PeopleDataFrame['Talk-Show']

    # userIds = PeopleDataFrame.transpose().columns
    # followInfor = getFriend(type)
    #
    # followMatrix = []
    # for uid in userIds:
    #     followMatrix.append(followInfor[uid])
    #
    # follow = np.array([int(t[0]) for t in followMatrix])
    # follower = np.array([int(t[1]) for t in followMatrix])
    # group = np.array([int(t[2]) for t in followMatrix])
    #
    #
    # PeopleDataFrame['follow'] = follow
    # PeopleDataFrame['follower'] = follower
    # PeopleDataFrame['group'] = group
    # print("%sPeople has %s " % (type, str(count)))
    # totally 37 dimensions
    PeopleDataFrame.to_csv('TrainingData/%sPeopleMovie_normalized.csv'%type)
    return PeopleDataFrame

# getUserIds('Dog')

dogMovieMatrix = getMatrix('Dog')
dogMovieMatrix = np.array(dogMovieMatrix)
with open('TrainingData/dogMovieMatrix.pickle', 'wb') as file:
    pickle.dump(dogMovieMatrix, file)
with open('TrainingData/dogMovieMatrix.pickle', 'rb') as file:
    dogMovieMatrix = pickle.load(file)



#25 34 4
# dogList = np.array(dogList).transpose()
# catList = np.array(catList).transpose()
#
# dogList = dogList.tolist()[0]
# catList = catList.tolist()[0]

# print(dogList)
# print(catList)

# print('--------------')
# cat = getMatrix('Cat')
# avg = np.array(cat).mean(0)
# position = np.argsort(avg)[-10:][::-1]
# for p in position:
#     print(cat.columns[p], avg[p])

#23, 4, 34, 7
#爱情 喜剧 冒险 犯罪
# getUserIds('Cat')





catMovieMatrix = getMatrix('Cat')
catMovieMatrix = np.array(catMovieMatrix)
with open('TrainingData/catMovieMatrix.pickle', 'wb') as file:
    pickle.dump(catMovieMatrix, file)
with open('TrainingData/catMovieMatrix.pickle', 'rb') as file:
    catMovieMatrix = pickle.load(file)

# print(dogMovieMatrix)
def getTFIDF(Xlist, XlistT):#use transpose
    length = len(Xlist)
    width = len(XlistT)

    for i in range(width):
        count = 0

        for item in XlistT[i]:
            if item != 0:
                count += 1
        if count != 0:
            idf = np.log10(length/count)
            for j in range(length):
                Xlist[j][i] = Xlist[j][i] * idf
    return Xlist

def dataMining(matrix1, matrix2):

    dogList = matrix1.tolist()
    catList = matrix2.tolist()

    dogList.extend(catList)
    wholeList = dogList
    # wholeListT = np.array(wholeList).transpose().tolist()
    #no need for tf-idf
    # wholeList = getTFIDF(wholeList, wholeListT)
    # 942 1025

    # 0 for dog 1 for cat
    labels = np.zeros((1, 942)).tolist()[0]
    labels.extend(np.ones((1, 1025)).tolist()[0])


    data = np.array(wholeList)
    matrix_mean = np.mean(data, 0)

    matrix_hat = data - matrix_mean


    U, D, V = np.linalg.svd(matrix_hat, full_matrices=False)
    #
    # ## find 90% of the sum of the eigenvalues
    #
    temp = 0.0
    count = 0
    for item in D:
        if temp <= (sum(D)*0.9):
            temp += item
            count += 1
    print('dimension: ', count)
    print((D[0]+D[1])/sum(D))
    dimensionReductionMatrix = np.mat(V[0:count, :]).transpose()
    matrix_projected = np.dot(matrix_hat, dimensionReductionMatrix)
    matrix_projected = matrix_projected.tolist()
    fig = plt.figure()
    plt.scatter([t[0] for t in matrix_projected[:942]], [t[1] for t in matrix_projected[:942]], c='red', alpha=0.3)
    plt.scatter([t[0] for t in matrix_projected[942:]], [t[1] for t in matrix_projected[942:]], c='blue', alpha=0.3)
    plt.show()

    result = np.zeros((6, 10))
    for i in range(10):
        X_train, X_test, y_train, y_test = train_test_split(matrix_projected, labels, test_size=0.2, random_state=3)
        #
        # no significant find
        #
        lr = LogisticRegression()
        lr.fit(X_train, y_train)
        result[0][i] = lr.score(X_test, y_test)
        # print('logistic regression score: ', lr.score(X_test, y_test))


        clf = DecisionTreeClassifier()
        clf.fit(X_train, y_train)
        result[1][i] = clf.score(X_test, y_test)
        # print('ldecision tree score: ', clf.score(X_test, y_test))

        clf = SVC()
        clf.fit(X_train, y_train)
        result[2][i] = clf.score(X_test, y_test)
        # print('SVM score: ', clf.score(X_test, y_test))

        clf = GaussianNB()
        clf.fit(X_train, y_train)
        result[3][i] = clf.score(X_test, y_test)
        # print('Naive bayes score: ', clf.score(X_test, y_test))

        neigh = KNeighborsClassifier(n_neighbors=3)
        neigh.fit(X_train, y_train)
        result[4][i] = neigh.score(X_test, y_test)
        # print('k nearest neighbour score: ', neigh.score(X_test, y_test))

        clf = GradientBoostingClassifier()
        clf.fit(X_train, y_train)
        result[5][i] = clf.score(X_test, y_test)
        # print('boosting score: ', clf.score(X_test, y_test))
        # print(result)

    result = result.mean(axis=1)
    print('average scores are')
    for item in result:
        print(item)


dataMining(dogMovieMatrix, catMovieMatrix)

'''
DogPeople has 942 
CatPeople has 1025 
'''

