import requests


url = "http://www.baidu.com/s"
r = requests.get(url, params={'wd': 'Python'})   # 百度关键字构造url
print(r.request.url)   # 构造的url
