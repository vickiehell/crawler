import  requests
import re
import  csv

f =open("date.csv",mode="w",encoding="utf-8")
csvwrite=csv.writer(f)
for i in range(0,250,25):
    url="https://movie.douban.com/top250?start={num}".format(num=i)
    print(url)
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
    }
    resp = requests.get(url=url,headers=headers)
    page_content=resp.text
    obj=re.compile('<li>.*?<span class="title">(?P<name>.*?)</span>.*?<br>.(?P<year>.*?)&nbsp;/&nbsp.*?<span class="rating_num" property="v:average">'
                   '(?P<score>.*?)</span>.*?<span>(?P<num>.*?)人评价',re.S)
    result=obj.finditer(page_content)
    for it in result:
        dict = it.groupdict()
        dict["year"] = dict["year"].strip()
        csvwrite.writerow(dict.values())
    resp.close()
f.close()


