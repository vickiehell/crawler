import  requests
import time
import pymysql
from pymysql.converters import escape_string
#响应头
headers={
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
    "referer":"https://t.bilibili.com/"
}
#mysql连接参数
config={
    "host":"127.0.0.1",
    "user":"root",
    "password":"13529146337",
    "database":"bilibili",
}
#对mysql执行sql插入语句
def mysql_insert(sql,params):
    db = pymysql.connect(**config)
    cursor=db.cursor()
    try:
        cursor.execute(sql,params)
    except Exception as e:
        print(e)
    else:
        db.commit()
    cursor.close()
    db.close()
#从数据库中查询id=id的数据并显示
def mysql_id_select(id):
    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql="select content,com_address,username,work_out_time,like_num,space_address from comment where id=%s"
    try:
        cursor.execute(sql,id)
    except:
        print("error")
    else:
        result=cursor.fetchall()
        for i in range(0,6):
            if result!=():
                print(result[0][i])
            else:
                print("无此id对应数据")
                break
    cursor.close()
    db.close()
#从数据库中查找对应内容的id
def mysql_content_select(text):
    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql=f"select id from comment where content='{text}'"
    try:
        cursor.execute(sql)
    except:
        print("error")
    else:
        if cursor.fetchone()==():
            print("无此内容")
        else:
            print(cursor.fetchone()[0])
    cursor.close()
    db.close()
#下载id对应的头像图片到本地/img文件夹下
def img_dowload(id):
    db = pymysql.connect(**config)
    cursor = db.cursor()
    cursor.execute(f"select img_data from comment where id={id}")
    result=cursor.fetchall()[0][0]
    with open("img/"+id,"wb") as f:
        f.write(result)
        f.close()
    cursor.close()
    db.close()
#爬取b站评论，获取相关信息
def b_crawler():
    # for循环控制翻页
    for i in  range(0,5):
        #从抓包工具里得到的网址
        comment_url=f"https://api.bilibili.com/x/v2/reply/main?next={i}&type=17&oid=560233713032161611&mode=3&plat=1&_=1633440097340"
        resp=requests.get(comment_url,headers=headers)
        #得到返回的json文件，从json里提取消息
        data=resp.json()["data"]
        #每页有20条评论，故循环20次
        for j in range(0,20):
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
            img_data=img_resp.content#图片二进制代码
            #img_name=img_address.split("/")[-1]
            #数据导入数据库
            sql="insert into comment(content,com_address,username,work_out_time,like_num,space_address,img_data) values(%s,%s,%s,%s,%s,%s,%s)"
            params=[content,com_address,username,work_out_time,like_num,space_address,img_data]
            mysql_insert(sql,params)
            img_resp.close()
        resp.close()
#主函数调用
if __name__ == '__main__':
    #b_crawler() #调用一次即可
    selec=input("是否进行查询:yes/no\n")
    if selec=="yes":
        flag=1
        while flag!=0:
            choice=int(input("请选择你要进行的操作:\n1.id查询(返回除图片以外的所有信息)\n"
                             "2.内容查询（返回内容对应数据id\n3."))
            if choice==1:
                id=int(input("输入id"))
                mysql_id_select(id)
            elif choice==2:
                text=input("输入内容")
                mysql_content_select(text)
            else:
                print("error!no this option!")
            flag=int(input("输入0退出，输入1继续查询"))
        else:
            print("已经退出查询")
    elif selec=="no":
        pass
    else:
        print("no this option")
    print("OVER!!!")


