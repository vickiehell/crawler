import  requests
wd=input("请输入一个名词")
url =f"https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd={wd}"
dic={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"}
resp = requests.get(url,headers=dic)
print(resp)
print(resp.text)

