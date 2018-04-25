import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import re
from datetime import datetime

'''
^01\-
2018-01

'''
'year month date'
timeListd = []
with open('dogTimeRecord.txt', 'r') as file:
    for item in file.readlines():
        ymd = str(item).split(' ')[0].strip()
        t = datetime.strptime(ymd, '%Y-%m-%d')
        # year = re.sub("(\d{4}).*", "\\1", ymd)
        # month = re.sub(".*\-(\d{2})\-.*", "\\1", ymd)
        # date = re.sub(".*\-(\d{2})$", "\\1", ymd)
        timeListd.append(t)
with open('dogTimeRecord_v2.txt', 'r') as file:
    for item in file.readlines():
        ymd = str(item).split(' ')[0].strip()
        t = datetime.strptime(ymd, '%Y-%m-%d')
        timeListd.append(t)

yearListd = [t.year for t in timeListd]
monthListd = [t.month for t in timeListd]
dayListd = [t.day for t in timeListd]

timeListc = []
with open('catTimeRecord.txt', 'r') as file:
    for item in file.readlines():
        ymd = str(item).split(' ')[0].strip()
        t = datetime.strptime(ymd, '%Y-%m-%d')
        timeListc.append(t)
with open('catTimeRecord_v2.txt', 'r') as file:
    for item in file.readlines():
        ymd = str(item).split(' ')[0].strip()
        t = datetime.strptime(ymd, '%Y-%m-%d')
        timeListc.append(t)

yearListc = [t.year for t in timeListc]
monthListc = [t.month for t in timeListc]
dayListc = [t.day for t in timeListc]


x = []
y = []
for item in sorted(list(set(yearListd))):
    x.append(item)
    y.append(yearListd.count(item))


xc = []
yc = []
for item in sorted(list(set(yearListc))):
    xc.append(item)
    yc.append(yearListc.count(item))

print(np.array(y)-np.min(y)/(np.max(y)-np.min(y)))


print((np.array(yc)-np.min(yc))/(np.max(yc)-np.min(yc)))

fig = plt.figure()

dog,  = plt.plot([i for i in x], [j for j in (np.array(y)-np.min(y))/(np.max(y)-np.min(y))], c='b')
cat,  = plt.plot([i for i in xc], [j for j in (np.array(yc)-np.min(yc))/(np.max(yc)-np.min(yc))], c='r')
plt.legend([dog, cat], ['dog', 'cat'], loc='upper right')


# plt.hist(timeListd, bins=6, alpha=0.5, label=['dog'])
# plt.legend(loc='upper right')
#
# '''
#
#
# '''
# #
# fig = plt.figure()
# plt.hist(yearListc, bins=6, alpha=0.5, label=['cat'])
# plt.legend(loc='upper right')
'''
[2013, 2014, 2015, 2016, 2017, 2018]
[17083, 27622, 22666, 20877, 17654, 4037]

'''
#
plt.show()