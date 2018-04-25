import pickle
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

    defaultValue = 1/3840
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
                    # count += 1
                else:
                    # del PeopleDataFrame[key]
                    PeopleDataFrame[key] = defaultValue

            else:
                # del PeopleDataFrame[key]
                PeopleDataFrame[key] = defaultValue

            count += 1

    print(count)
    PeopleDataFrame = PeopleDataFrame.transpose()
    # print("%sPeople has %s "%(type, str(count)))
    PeopleDataFrame.to_csv('TrainingData/%sPeopleBook_normalized.csv'%type)
    return PeopleDataFrame

# getUserIds('Dog')
# getMatrix('Dog')
# getUserIds('Cat')
# getMatrix('Cat')


'''

DogPeople has 651  
CatPeople has 718  


'''

# dogBookMatrix = getMatrix('Dog')
# dogBookMatrix = np.array(dogBookMatrix)
# with open('TrainingData/dogBookMatrix.pickle', 'wb') as file:
#     pickle.dump(dogBookMatrix, file)
with open('TrainingData/dogBookMatrix.pickle', 'rb') as file:
    dogBookMatrix = pickle.load(file)

# catBookMatrix = getMatrix('Cat')
# catBookMatrix = np.array(catBookMatrix)
# with open('TrainingData/catBookMatrix.pickle', 'wb') as file:
#     pickle.dump(catBookMatrix, file)
with open('TrainingData/catBookMatrix.pickle', 'rb') as file:
    catBookMatrix = pickle.load(file)


def dataMining(matrix1, matrix2):

    dogList = matrix1.tolist()
    catList = matrix2.tolist()

    dogList.extend(catList)
    wholeList = dogList
    # wholeListT = np.array(wholeList).transpose().tolist()
    #no need for tf-idf
    # wholeList = getTFIDF(wholeList, wholeListT)


    # 0 for dog 1 for cat
    labels = np.zeros((1, 2001)).tolist()[0]
    labels.extend(np.ones((1, 2001)).tolist()[0])


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
    print('reduce the dimension to: ', count)
    # print((D[0]+D[1]+D[2]+D[3]+D[4])/sum(D))
    dimensionReductionMatrix = np.mat(V[0:count, :]).transpose()
    matrix_projected = np.dot(matrix_hat, dimensionReductionMatrix)
    matrix_projected = matrix_projected.tolist()
    # fig = plt.figure()
    # plt.scatter([t[0] for t in matrix_projected[:942]], [t[1] for t in matrix_projected[:942]], c='red', alpha=0.3)
    # plt.scatter([t[0] for t in matrix_projected[942:]], [t[1] for t in matrix_projected[942:]], c='blue', alpha=0.3)
    # plt.show()

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
    for item in result:
        print(item)





dataMining(dogBookMatrix, catBookMatrix)







