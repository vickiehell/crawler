import requests

session=requests.session()
url="https://passport.17k.com/ck/user/login"
data={
    "loginName":"18064931725",
    "password":"w13529146337"
}
session.post(url,data=data)
resp=session.get("https://user.17k.com/ck/author/shelf?page=1&appKey=2406394919")
resp.encoding="utf-8"
print(resp.json())