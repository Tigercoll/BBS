import requests
import json

data = list()
response  = requests.get('https://api.weibo.com/2/emotions.json?source=1362404091')
for i in response.json():
    data.append({"alt":i["phrase"],"src":i["icon"]})


print(data)