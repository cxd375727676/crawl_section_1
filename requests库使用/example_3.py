import requests
import os

url = "http://image.nationalgeographic.com.cn/2017/0211/20170211061910157.jpg"  # 图片资源
r = requests.get(url)

path = os.path.join(os.getcwd(), 'output', 'crawl_image.jpg')
with open(path, "wb") as f:
    f.write(r.content)    # r.content 是二进制
