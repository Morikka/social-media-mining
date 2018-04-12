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
dog_dict = {"北京":"19034","上海":"13684","广东":"11720","浙江":"8156","四川":"4993","江苏":"9205","湖北":"4194","陕西":"3226","天津":"2340","重庆":"2287","湖南":"2869","河南":"2546","山东":"4547","辽宁":"2701","福建":"2469","黑龙江":"1324","安徽":"1776","云南":"1283","吉林":"1002","河北":"1672","广西":"1071","江西":"1040","香港":"482","山西":"817","贵州":"542","甘肃":"479","新疆":"497","内蒙古":"649","海南":"344","澳门":"178","宁夏":"195","台湾":"143","西藏":"163","青海":"106"}
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
    # t.write('\"'+ str(items) + '\":\"+' )
    # t.write('\"' + str(items) + '\":\"' + str(province_count[items]-int(dog_dict[items])) +'\",')
    # t.write(str(items))
    t.write("{\"name\":\""+str(items)+"\", \"value\": "+str(province_count[items]-int(dog_dict[items]))+"},")
    t.write('\n')

# import requests
# url = 'http://tools.bugcode.cn'
# r = requests.post(url+'/cities/search', {'country': '中国', 'language': 'cn', 'city': '淮安'})
# if r.status_code == 200:
#   print(r)
#   print(r.text)
# else:
#   print(r.status_code)
