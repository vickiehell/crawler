import  requests
from lxml import  etree

urllists=[".","/4.","/3.","/2.","/1."]
for i in urllists:
    url=f"https://sise.uestc.edu.cn/xwtz/tzgg/yb{i}htm"
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
    }
    resp=requests.get(url,headers=headers)
    #print(resp.text)
    html=etree.HTML(resp.text)
    news_a=html.xpath("/html/body/div[2]/div[2]/div[2]/div/a")
    #print(news_a)
    for it in news_a:
        a_child_url="".join(it.xpath("./@href"))
        child_url="https://sise.uestc.edu.cn"+a_child_url.split("..")[-1]
        #print(child_url)
        child_resp=requests.get(child_url)
        child_resp.encoding="utf-8"
        child_html=etree.HTML(child_resp.text)

        title="".join(child_html.xpath("/html/body/div[2]/div[2]/div[2]/h1/text()"))
        time="".join(child_html.xpath("/html/body/div[2]/div[2]/div[2]/p/text()")).split(" ")[1]
        content=child_html.xpath("/html/body/div[2]/div[2]/div[2]/div[1]/div")[0]
        html_content=str(etree.tostring(content,pretty_print=True,method="html"),encoding="utf-8")

        with open("html/"+f"标题:{title}-发布时间:{time}.html",mode="w",encoding="utf-8") as f:
            f.write(html_content)
            f.close()
        child_resp.close()

    resp.close()

