import  re
import requests
import  csv

domain="https://www.dytt89.com/"
resp1 = requests.get(domain,verify=False)
resp1.encoding="gb2312"

obj1= re.compile(r'2021必看热片.*?<ul>(?P<ul>.*?)</ul',re.S)
obj2= re.compile(r"<a href='(?P<child_ul>.*?)'",re.S)
obj3= re.compile(r'◎片　　名　(?P<name>.*?)<br />.*?<td style="WORD-WRAP: break-word" bgcolor="#fdfddf"><a '
                 r'href="(?P<download>.*?)"',re.S)
f= open("movie.csv","w",encoding="utf-8")
fwriter=csv.writer(f)
result1=obj1.finditer(resp1.text)
for it in result1:
    result2 = obj2.finditer(it.group("ul"))
    for itt in result2:
        child_url=domain + itt.group("child_ul").strip("/")
        resp2=requests.get(child_url,verify=False)
        resp2.encoding="gb2312"
        result3=obj3.finditer(resp2.text)
        for ittt in result3:
            datadic = ittt.groupdict()
            fwriter.writerow(datadic.values())
        resp2.close()
f.close()
resp1.close()

