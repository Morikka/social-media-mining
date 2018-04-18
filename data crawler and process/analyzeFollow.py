import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier


follow = []
follower = []
group = []
dogList = []
catList = []
count = 0
followInfor = {}
for i in range(10):
    path = r'raw data\catfollow\CatfollowInfo_%s.pickle'%str(i)
    with open(path, 'rb') as file:
        data = pickle.load(file)
    for key in data.keys():

        infomation = data[key]
        if [int(i) for i in data[key]] != [0, 0, 0]:
            dogList.append([int(i) for i in data[key]])
            count += 1
        follow.append(infomation[0])
        follower.append(infomation[1])
        group.append(infomation[2])
        followInfor[key] = [follow, follower, group]


followd = []
followerd = []
groupd = []
count = 0
for i in range(10):
    path = r'raw data\dogfollow\followInfo_%s.pickle' % str(i)
    with open(path, 'rb') as file:
        data = pickle.load(file)
    for key in data.keys():
        infomation = data[key]
        if [int(i) for i in data[key]] != [0, 0, 0]:
            dogList.append([int(i) for i in data[key]])
            count += 1
        followd.append(infomation[0])
        followerd.append(infomation[1])
        groupd.append(infomation[2])

# print(count)
cat = [follow, follower, group]
dog = [followd, followerd, groupd]
N = ['follow', 'follower', 'group']

# print(cat[0])
# print(dog[0])


labels = np.zeros((1, 1945)).tolist()[0]
labels.extend(np.ones((1, 1946)).tolist()[0])
# 0 for cat 1 and for dog

dogList.extend(catList)
wholeList = dogList


# X_train, X_test, y_train, y_test = train_test_split(wholeList, labels, test_size=0.3, random_state=0)
#
# lr = LogisticRegression()
# lr.fit(X_train, y_train)
# print('logistic regression score: ', lr.score(X_test, y_test))
#
#
# clf = DecisionTreeClassifier()
# clf.fit(X_train, y_train)
# print('ldecision tree score: ', clf.score(X_test, y_test))
#
# clf = SVC()
# clf.fit(X_train, y_train)
# print('SVM score: ', clf.score(X_test, y_test))
#
# clf = GaussianNB()
# clf.fit(X_train, y_train)
# print('Naive bayes score: ', clf.score(X_test, y_test))
#
# neigh = KNeighborsClassifier(n_neighbors=5)
# neigh.fit(X_train, y_train)
# print('k nearest neighbour score: ', neigh.score(X_test, y_test))
#
# clf = GradientBoostingClassifier()
# clf.fit(X_train, y_train)
# print('boosting score: ', clf.score(X_test, y_test))

# fig = plt.figure()
# array, bins = np.histogram(np.array(cat[1]).astype('float'), bins='auto')
# plt.hist(array, bins)
# plt.xlim((0, 1))
# fig1 = plt.figure()
# arrayd, binsd = np.histogram(np.array(dog[1]).astype('float'), bins='auto')
# plt.hist(arrayd, binsd)
# plt.xlim((0, 1))
# plt.show()



# for i in range(3):
#     for j in range(3):
#         position = '33%s'%str(3*(i)+(j+1))
#         ax = plt.subplot(int(position))
#         # plt.scatter(cat[j], cat[i], c='r', alpha=0.1)
#         plt.scatter(dog[j], dog[i], c='b', alpha=0.1)
#         plt.xlabel(N[j])
#         plt.ylabel(N[i])
#         # plt.xlim((-10, 500))
#         # plt.ylim((-10, 500))
# arrayc, binsc = np.histogram(np.array(cat[0]).astype('float'), bins='auto')
# arrayd, binsd = np.histogram(np.array(dog[0]).astype('float'), bins='auto')
leg = ['cat', 'dog']
#
# plt.hist([arrayc, arrayd], bins=binsd, label=leg)
# plt.legend(prop={'size': 10})
# plt.title("number of users' following")
# plt.xlim((-1, 50))
# plt.ylim((-1, 50))

fig2 = plt.figure()

arrayc, binsc = np.histogram(np.array(cat[2]).astype('int'), bins='auto')
arrayd, binsd = np.histogram(np.array(dog[2]).astype('int'), bins='auto')
plt.hist([np.array(cat[1]).astype('int'), np.array(dog[1]).astype('int')], binsc, label=leg)
plt.legend(prop={'size': 10})
plt.xlabel('number of groups')

print(arrayc)
print(arrayd)
plt.title("number of groups users participate")
plt.xlim((-1, 15))
plt.ylim((-1, 2000))


# plt.scatter(cat[0], cat[1], c='r', alpha=0.1)
# plt.scatter(dog[0], dog[1], c='b', alpha=0.1)
plt.show()

# fig3 = plt.figure()
# plt.scatter(group, follower)

# plt.ylim((0, 60))











