import  requests
import  json
import  demjson
url="https://movie.douban.com/typerank"
param={
    "type":"24",
    "interval_id":"100:90",
    "action":"",
    "start":"0",
    'limit':"20"
}
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
}
resp=requests.get(url=url,headers=headers,params=param)
print(resp.json())
resp.close()
