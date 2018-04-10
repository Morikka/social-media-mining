#coding=utf-8
import csv
import json

def get_info(name):
  info = {}

  if(name=='北京'):
    info['name'] = name;
    info['ID'] = '110000';
    return info;

  if(name=='天津'):
    info['name'] = name;
    info['ID'] = '120000';
    return info;

  if(name=='上海'):
    info['name'] = name;
    info['ID'] = '310000';
    return info;

  if(name=='重庆'):
    info['name'] = name;
    info['ID'] = '500000';
    return info;

  with open('../Data/json/city_code.json') as f:
    data = json.load(f)
    for i in range(len(data)):
      for j in range(len(data[i]['cities'])):
        city = data[i]['cities'][j]['name'];
        if name==city[:len(name)]: #市 need to remove while 盟 not
          info['name'] = name
          if data[i]['name'][:3]=='黑龙江':
            info['name_prov']='黑龙江'
          elif data[i]['name'][:3]=='内蒙古':
            info['name_prov']='内蒙古'
          elif name=='朝阳':
            info['ID'] = 211300
            info['name_prov'] = '辽宁'
            info['ID_prov'] = '210000'
            break
          else:
            info['name_prov'] = data[i]['name'][:2]
          info['ID_prov'] = data[i]['code']
          # print(name+' '+data[i]['cities'][j]['name'])
          return info
  return info

get_info('烟台')
# get_info('北京')

cat_dict = {}
with open('../raw data/CatPeople.csv') as f:
# with open('../raw data/DogPeople.csv') as f:
  f_csv = csv.reader(f)
  headers = next(f_csv)
  for row in f_csv:
    name = row[1]
    if name in cat_dict:
      cat_dict[name] += 1
    else:
      cat_dict[name] = 1
cat_dict = sorted(cat_dict.items(), key=lambda kv: kv[1], reverse=True)

province_list = []
city_list = []

province_count = {}

with open('t.out','w') as t:
  for item in cat_dict:
    # print(item[0] +' '+str(get_info(item[0])))
    info = get_info(item[0])

    if 'name_prov' in info:
      # print(info['name']+' '+info['name_prov'])
      if info['name_prov'] in province_count:
        province_count[info['name_prov']] += item[1]
      else:
        province_count[info['name_prov']] = item[1]
    elif 'name' in info:
      province_count[info['name']] = item[1]

  # print(province_count)

  for items in province_count:
    t.write("{\"name\":\""+str(items)+"\", \"value\": "+str(province_count[items])+"},")
    t.write('\n')

# import requests
# url = 'http://tools.bugcode.cn'
# r = requests.post(url+'/cities/search', {'country': '中国', 'language': 'cn', 'city': '淮安'})
# if r.status_code == 200:
#   print(r)
#   print(r.text)
# else:
#   print(r.status_code)
