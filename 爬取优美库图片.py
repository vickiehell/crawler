import  requests
from bs4 import BeautifulSoup
import  time

url="https://www.umei.cc/katongdongman/dongmantupian/"
domain="https://www.umei.cc"
resp = requests.get(url)
resp.encoding="utf-8"
#print(resp.text)
page=BeautifulSoup(resp.text,"html.parser")
child_url=page.find("div",class_="TypeList")
#print(child_url)
a_list=child_url.find_all("a")
for a in a_list:
    img_url=domain + a.get("href")
    #print(img_url)
    resp1= requests.get(img_url)
    resp1.encoding="utf-8"
    img_page=BeautifulSoup(resp1.text,"html.parser")
    div=img_page.find("div",class_="ImageBody")
    img =div.find("img")
    src= img.get("src")
    imgname=src.split("/")[-1]
    resp2=requests.get(src)
    with open("img/"+imgname,"wb") as f:
        f.write(resp2.content)
    print("over!")
    resp2.close()
    resp1.close()
    time.sleep(1)
print("all over")
resp.close()