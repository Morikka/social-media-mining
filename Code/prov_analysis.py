import math
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

def eigsorted(cov):
    vals, vecs = np.linalg.eigh(cov)
    order = vals.argsort()[::-1]
    return vals[order], vecs[:,order]

# cat_dict ={"北京":"13583","上海":"10307","广东":"13050","浙江":"6507","四川":"4501","江苏":"7096","湖北":"3329","重庆":"2194","陕西":"2400","天津":"1622","湖南":"2226","河南":"2218","辽宁":"2408","山东":"3607","福建":"2277","安徽":"1664","黑龙江":"1147","云南":"1134","吉林":"884","河北":"1526","广西":"1075","江西":"976","山西":"840","香港":"417","贵州":"550","甘肃":"429","澳门":"231","新疆":"490","内蒙古":"662","海南":"312","宁夏":"187","台湾":"195","青海":"144","西藏":"180"}
cat_dict ={"北京":"13583","上海":"10307","浙江":"6507","四川":"4501","江苏":"7096","湖北":"3329","重庆":"2194","陕西":"2400","天津":"1622","湖南":"2226","河南":"2218","辽宁":"2408","山东":"3607","福建":"2277","安徽":"1664","黑龙江":"1147","云南":"1134","吉林":"884","河北":"1526","广西":"1075","江西":"976","山西":"840","香港":"417","贵州":"550","甘肃":"429","澳门":"231","新疆":"490","内蒙古":"662","海南":"312","宁夏":"187","台湾":"195","青海":"144","西藏":"180"}
# dog_dict = {"北京":"19034","上海":"13684","广东":"11720","浙江":"8156","四川":"4993","江苏":"9205","湖北":"4194","陕西":"3226","天津":"2340","重庆":"2287","湖南":"2869","河南":"2546","山东":"4547","辽宁":"2701","福建":"2469","黑龙江":"1324","安徽":"1776","云南":"1283","吉林":"1002","河北":"1672","广西":"1071","江西":"1040","香港":"482","山西":"817","贵州":"542","甘肃":"479","新疆":"497","内蒙古":"649","海南":"344","澳门":"178","宁夏":"195","台湾":"143","西藏":"163","青海":"106"}
dog_dict ={"北京":"19034","上海":"13684","浙江":"8156","四川":"4993","江苏":"9205","湖北":"4194","陕西":"3226","天津":"2340","重庆":"2287","湖南":"2869","河南":"2546","山东":"4547","辽宁":"2701","福建":"2469","黑龙江":"1324","安徽":"1776","云南":"1283","吉林":"1002","河北":"1672","广西":"1071","江西":"1040","香港":"482","山西":"817","贵州":"542","甘肃":"479","新疆":"497","内蒙古":"649","海南":"344","澳门":"178","宁夏":"195","台湾":"143","西藏":"163","青海":"106"}
cat_list = []
dog_list = []
div = 0
avg = 0
cnt = 0
for item in cat_dict:
  dog = int(dog_dict[item])
  cat = int(cat_dict[item])
  cat_list.append(cat)
  dog_list.append(dog)
  tmp = dog - cat
  print(str(dog)+' '+str(cat)+' '+str(tmp)+' '+str(tmp/dog)+' '+str(tmp/cat))
  avg += tmp

  # print(item)
  # print(int(dog_dict[item])-int(cat_dict[item]))
avg = avg/34.0
div = 0.0
for item in cat_dict:
  dog = int(dog_dict[item])
  cat = int(cat_dict[item])
  tmp = dog - cat
  div += (tmp - avg)*(tmp - avg)

div = div/34.0

x = cat_list
y = dog_list

# np.polyfit(x,y)
# nstd = 2
# ax = plt.subplot(111)

# cov = np.cov(x, y)
# vals, vecs = eigsorted(cov)
# theta = np.degrees(np.arctan2(*vecs[:,0][::-1]))
# w, h = 2 * nstd * np.sqrt(vals)
# # ell = Ellipse(xy=(np.mean(x), np.mean(y)),
#               # width=w, height=h,
#               # angle=theta, color='black')
# ell.set_facecolor('none')
# ax.add_artist(ell)

fit = np.polyfit(x,y,1)
fit_fn = np.poly1d(fit)
# fit_fn is now a function which takes in x and returns an estimate for y
print(fit_fn(x))

plt.plot(x, fit_fn(x))
plt.scatter(x,y)
plt.scatter(13050,11720)
plt.show()