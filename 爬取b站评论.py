import  requests
from  lxml import html
import  re
from  bs4 import BeautifulSoup
import time
import pymysql
from pymysql.converters import escape_string
#响应头
headers={
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
    "referer":"https://t.bilibili.com/"
}
config={
    "host":"127.0.0.1",
    "user":"root",
    "password":"13529146337",
    "database":"bilibili",
}
#对mysql执行sql语句
def mysql_execute(sql,params):
    db = pymysql.connect(**config)
    cursor=db.cursor()
    cursor.execute(sql,params)
    db.commit()
    cursor.close()
    db.close()
#for循环控制翻页
for i in  range(0,1):
    #从抓包工具里得到的网址
    comment_url=f"https://api.bilibili.com/x/v2/reply/main?next={i}&type=17&oid=560233713032161611&mode=3&plat=1&_=1633440097340"
    resp=requests.get(comment_url,headers=headers)
    #得到返回的json文件，从json里提取消息
    data=resp.json()["data"]
    #每页有20条评论，故循环20次
    for j in range(0,1):
        #爬取评论的相关消息
        content=escape_string(data["replies"][j]["content"]["message"])#评论内容
        com_address=escape_string('https://t.bilibili.com/560233713032161611/#reply'+data["replies"][j]['rpid_str']) #评论链接
        username=escape_string(data["replies"][j]['member']['uname'])  #作者名字
        work_out_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(data["replies"][j]['ctime'])) #发布时间（str类型）
        like_num=data["replies"][j]['like'] #点赞数量
        mid=data["replies"][j]['mid']
        space_address=escape_string(f"https://space.bilibili.com/{mid}?spm_id_from=444.42.0.0") #空间地址
        img_address=data["replies"][j]['member']['avatar'] #头像图片下载地址
        img_resp=requests.get(img_address)
        img_data=img_resp.content
        #print(img_address)
        img_name=img_address.split("/")[-1]
        #插入数据库
        sql="insert into comment(content,com_address,username,work_out_time,like_num,space_address,img_data) values(%s,%s,%s,%s,%s,%s,%s)"
        params=[content,com_address,username,work_out_time,like_num,space_address,img_data]
        mysql_execute(sql,params)
        img_resp.close()
    resp.close()