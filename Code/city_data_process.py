#coding=utf-8
import csv

cat_dict = {}
# with open('../raw data/CatPeople.csv') as f:
with open('../raw data/DogPeople.csv') as f:
  f_csv = csv.reader(f)
  headers = next(f_csv)
  for row in f_csv:
    name = row[1]
    if name in cat_dict:
      cat_dict[name] += 1
    else:
      cat_dict[name] = 1
cat_dict = sorted(cat_dict.items(), key=lambda kv: kv[1], reverse=True)
with open("t.out","w") as t:
  for item in cat_dict:
    t.write(str(item))
    t.write("\n")

# import requests
# url = 'http://tools.bugcode.cn'
# r = requests.post(url+'/cities/search', {'country': '中国', 'language': 'cn', 'city': '淮安'})
# if r.status_code == 200:
#   print(r)
#   print(r.text)
# else:
#   print(r.status_code)
