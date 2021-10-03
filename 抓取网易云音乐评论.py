import  requests
from Crypto.Cipher import AES
from  base64 import  b64encode
import  json
url ="https://music.163.com/weapi/comment/resource/comments/get?csrf_token="
data={
        "csrf_token": "",
        "cursor": "-1",
        "offset": "0",
        "orderType": "1",
        "pageNo": "1",
        "pageSize": "20",
        "rid": "R_SO_4_1842817284",
        "threadId": "R_SO_4_1842817284"
}
e="010001"
f='00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
g="0CoJUm6Qyw8W8jud"
i="2Zn2XtyC1S1inL4w"

def to_16(data):
    pad=16- len(data)%16
    data+= chr(pad)*pad
    return data
def encSeckey():
    return "cbe6a00b7070923d6503552773a0ca616122959de206680346db62c6e88fd7ae7eca3cc671f79527d9ae2b152112c674f53b5c0131d4d38469b737f35590f005804735e8a02feb988c9092402ec23c564ed176b01e3b0e2bc1603649f033e39a439cfafc28f86d5709a82438fac92d45bb92d03f585920d71de0e1aa59538493"
def get_params(data):
    first=enc_params(data,g)
    second=enc_params(first,i)
    return second
def enc_params(data,key):
    iv="0102030405060708"
    data=to_16(data)
    aes=AES.new(key=key.encode("utf-8"),IV=iv.encode("utf-8"),mode=AES.MODE_CBC)
    enc=aes.encrypt(data.encode("utf-8"))
    return  str(b64encode(enc),"utf-8")

resp= requests.post(url,data={
    "params":get_params(json.dumps(data)),
    "encSecKey":encSeckey()
})

print(resp.json()["data"]["comments"])
resp.close()
"""!function() {
    function a(a=16) {
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)
            e = Math.random() * b.length,
            e = Math.floor(e),
            c += b.charAt(e);
        return c
    }
    function b(a, b) {
        var c = CryptoJS.enc.Utf8.parse(b)
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a)
          , f = CryptoJS.AES.encrypt(e, c, {
            iv: d,
            mode: CryptoJS.mode.CBC
        });
        return f.toString()
    }
    function c(a, b, c) {
        var d, e;
        return setMaxDigits(131),
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a)
    }
    function d(d, e, f, g) {# d:数据
        var h = {}
          , i = a(16);
        return h.encText = b(d, g),
        h.encText = b(h.encText, i),
        h.encSecKey = c(i, e, f),
        h
    }"""