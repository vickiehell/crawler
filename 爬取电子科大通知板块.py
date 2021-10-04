import  requests
from lxml import  etree
import os
import  time
count=0
urllists=[".","/4.","/3.","/2.","/1."]
for i in urllists:#主页面翻页
    url=f"https://sise.uestc.edu.cn/xwtz/tzgg/yb{i}htm".strip("\n")
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
        "Connection": "close"
    }
    resp=requests.get(url,headers=headers)
    #print(resp.text)
    html=etree.HTML(resp.text)
    news_a=html.xpath("/html/body/div[2]/div[2]/div[2]/div/a")
    #print(news_a)
    for it in news_a:#每页选择消息通知
        a_child_url="".join(it.xpath("./@href"))
        child_url="https://sise.uestc.edu.cn"+a_child_url.split("..")[-1]
        child_resp=requests.get(child_url)
        child_resp.encoding="utf-8"
        child_html=etree.HTML(child_resp.text)
        #提取新闻标题和发布时间
        title="".join(child_html.xpath("/html/body/div[2]/div[2]/div[2]/h1/text()"))
        _time="".join(child_html.xpath("/html/body/div[2]/div[2]/div[2]/p/text()")).split(" ")[1]
        #在当前目录下创建新文件目录用于存放数据
        if count==0:#只创建一次
            os.mkdir("data")
            os.chdir(".\data")
            count+=1
        #创建以发布时间为名称的文件夹存放对应爬取的详细内容，图片和附件
        if not os.path.exists(f"{_time}"):
            os.mkdir(f"{_time}")
        #写入详细内容
        content = child_html.xpath("/html/body/div[2]/div[2]/div[2]/div[1]/div")[0]
        html_content = str(etree.tostring(content, pretty_print=True, method="html"), encoding="utf-8")
        with open(f"{_time}/"+f"{title}.html",mode="w",encoding="utf-8") as f :
            f.write(html_content)
            f.close()
        #写入附件(发现所有附件所在p标签对应的style属性值是固定的)
        if content.xpath("./p[@style='line-height: 16px;']/a/@href"):#判别有附件的通知
            for doc_url in content.xpath("./p[@style='line-height: 16px;']/a/@href"):
                append_doc_url="https://sise.uestc.edu.cn"+doc_url
                #因为一些通知由于时间久远，附件网址已经无法访问了，所以采用异常处理除去无法访问的附件（好像18年9月以前的都不能下载了）
                try:
                    doc_resp=requests.get(append_doc_url)
                except Exception as e:
                    #print("年代久远，文件地址缺失")
                    doc_resp.close()
                else:
                    #doc_name="".join(content.xpath("./p[@style='line-height: 16px;']/a/strong/span/text()"))
                    doc_name=append_doc_url.split("?")[-2].split("/")[-1]
                    if doc_name:
                        with open(f"{_time}/"+r"{}".format(doc_name),"wb") as f_doc:
                            f_doc.write(doc_resp.content)
                            f_doc.close()
                        doc_resp.close()
        #写入图片(仅仅在文件的详细内容里查找标签img，不查找背景图片等)
        if content.xpath(".//img/@src"):
            for img_url in content.xpath(".//img/@src"):
                append_img_url="https://sise.uestc.edu.cn"+img_url
                try:
                    img_resp=requests.get(append_img_url)
                except Exception as er:
                    img_resp.close()
                else:
                    img_name=append_img_url.split("?")[-2].split("/")[-1]
                    if img_name:
                        with open(f"{_time}/"+r"{}".format(img_name),"wb") as f_img:
                            f_img.write(img_resp.content)
                            f_img.close()
                        img_resp.close()
        time.sleep(1)

        child_resp.close()

    resp.close()

