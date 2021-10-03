import  requests
from lxml import  etree

url="https://chengdu.zbj.com/search/f/?kw=saas"
resp=requests.get(url)
tree =etree.HTML(resp.text)
root_path=tree.xpath("/html/body/div[6]/div/div/div[2]/div[5]/div[1]/div")
for div in root_path:
    name = "saas".join(div.xpath("./div[1]/div[1]/a[2]/div[2]/div[2]/p/text()"))
    price = div.xpath("./div[1]/div[1]/a[2]/div[2]/div[1]/span[1]/text()")[0].strip("¥")
    print(price)

