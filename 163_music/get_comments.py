"""
@author: Alex
@contact: 1272296763@qq.com or jakinmili@gmail.com
@file: get_comments.py
@time: 2019/9/10 17:38
"""
import os
import requests
import math
import random
from Crypto.Cipher import AES
import codecs
import base64


def get_comments_json(url, data):
    headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
             'Accept-Encoding': 'gzip, deflate',
             'Accept-Language': 'zh-CN,zh;q=0.9',
             'Connection': 'keep-alive',
             'Cookie': 'mail_psc_fingerprint=2587f9673e0b685c9167817fb3f8c29d; nts_mail_user=fs_wsxh@163.com:-1:1; _ga=GA1.2.891188031.1521856993; _ntes_nnid=e4c89acdde4a7abb908528162d68dcea,1543198958139; _ntes_nuid=e4c89acdde4a7abb908528162d68dcea; usertrack=ezq0o1wtqm8u/9xaB4nYAg==; _iuqxldmzr_=32; WM_TID=N3%2BA6%2FjG9r1BAQBRQVMtbbchr7mRIjtQ; __oc_uuid=b7463de0-9d4c-11e9-a277-f3f3233976fd; vjuids=d8086b47c.16bbb7e4bf6.0.09ad6b6683674; vjlast=1562218745.1562218745.30; vinfo_n_f_l_n3=a4c2419f1cbe143d.1.0.1562218744848.0.1562218745070; P_INFO=alexjakin@126.com|1565170896|1|mail126|00&99|null&null&null#gud&440500#10#0#0|&0||alexjakin@126.com; __guid=94650624.3028801420228760000.1568104294123.7378; WM_NI=h86yWJnXVE%2FdsnNikgIPtCZwCuCA%2Fk25BsAvF6a87Kl%2B3jiEZU2HrbPxhAs6Kxe6UB5PxahK82iI1%2FssgQ48kriUFSh3ins7VGVZn0Ca2URR3uST%2F2BsPZBnbCMla%2FrSb0M%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee88f0338c8b96cce280f2bc8fb2d14b978b9bbbf234a594ac84e4499bb8e1abf42af0fea7c3b92aace8fa9ad642ae889aa6ae70b1b2828aea6d8b90bca4d97d81ab8da2ae61f2eb8e94c47e86eaafd9b641b0f5fd8bec4f9a8bfea9f16a94a8a8a2f23e89a8abd7d84af790b882eb41fceea7aab425b1ada9b2b734a9aea7b6c559aceda78ff23d96999abbed3c81bffeb6d15af1ab9db5ae3a82ada0bbc166a29d838de425b28daed1d037e2a3; JSESSIONID-WYYY=Kol38xRaHmX9mMoRykvd7P1Eof%5CAUotUfCiABQymgpDZt9awfCJlGESF%2B7vY3hzkf4iH6lPafWou3WnVzQB37ypp95bqY4d3RPp3k6T%5CIeVxxjO4IjDnW%2B9ahrupCGRieqlIlcRMlioS6yNwC7WAKwHj%2BRyp3Ef3DkDTtlOpYZ4XzjB6%3A1568109975442; monitor_count=8',
             'Host': 'music.163.com',
             'Referer': 'http://music.163.com/',
             'Upgrade-Insecure-Requests': '1',
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/66.0.3359.181 Safari/537.36'}

    try:
        r = requests.post(url, headers=headers, data=data)
        r.encoding = "utf-8"
        if r.status_code == 200:

            # 返回json格式的数据
            return r.json()

    except:
        print("爬取失败!")

# 生成16个随机字符
def generate_random_strs(length):
    """
    用于get_params函数的加密
    :param length:
    :return:
    """
    string = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    # 控制次数参数i
    i = 0
    # 初始化随机字符串
    random_strs  = ""
    while i < length:
        e = random.random() * len(string)
        # 向下取整
        e = math.floor(e)
        random_strs = random_strs + list(string)[e]
        i = i + 1
    return random_strs


# AES加密
def AESencrypt(msg, key):
    """
    用于get_params函数的加密
    :param msg:
    :param key:
    :return:
    """
    # 如果不是16的倍数则进行填充(paddiing)
    padding = 16 - len(msg) % 16
    # 这里使用padding对应的单字符进行填充
    msg = msg + padding * chr(padding)
    # 用来加密或者解密的初始向量(必须是16位)
    iv = '0102030405060708'

    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 加密后得到的是bytes类型的数据
    encryptedbytes = cipher.encrypt(msg)
    # 使用Base64进行编码,返回byte字符串
    encodestrs = base64.b64encode(encryptedbytes)
    # 对byte字符串按utf-8进行解码
    enctext = encodestrs.decode('utf-8')

    return enctext


# RSA加密
def RSAencrypt(randomstrs, key, f):
    """
    用于get_params函数的加密
    :param randomstrs:
    :param key:
    :param f:
    :return:
    """
    # 随机字符串逆序排列
    string = randomstrs[::-1]
    # 将随机字符串转换成byte类型数据
    text = bytes(string, 'utf-8')
    seckey = int(codecs.encode(text, encoding='hex'), 16)**int(key, 16) % int(f, 16)
    return format(seckey, 'x').zfill(256)

# 获取参数
def get_params(page):
    """
    获取post参数
    :param page: 需要请求的页数
    :return:
    """
    # msg = '{"rid":"R_SO_4_1302938992","offset":"0","total":"True","limit":"100","csrf_token":""}'
    offset = (page-1) * 20
    # offset和limit是必选参数,其他参数是可选的,其他参数不影响data数据的生成
    msg = '{"offset":' + str(offset) + ',"total":"True","limit":"20","csrf_token":""}'
    key = '0CoJUm6Qyw8W8jud'
    f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    e = '010001'
    enctext = AESencrypt(msg, key)
    # 生成长度为16的随机字符串
    i = generate_random_strs(16)
    # 两次AES加密之后得到params的值
    encText = AESencrypt(enctext, i)
    # RSA加密之后得到encSecKey的值
    encSecKey = RSAencrypt(i, e, f)
    return encText, encSecKey

def save_comments(comments, songname, page):
    """
    保存写入文件
    :param comments: 请求头的评论数组
    :param songname: 歌曲名字
    :param page: 当前评论页数
    :return:
    """
    filepath = 'comment_data/'+songname + '.txt'
    # if os.path.exists(filepath):
    #     os.remove(filepath)
    for item in comments:
        user = item['user']
        user_name = user['nickname']
        content = item["content"]
        # 处理符号
        content = content.strip().replace('\n', '').replace('/n', '')
        likecount = item["likedCount"]
        # 以追加的模式打开
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write("{},{},{}\n".format(user_name, content, likecount))
        print("写入用户：{}一条评论成功，该评论点赞次数{}".format(user_name, likecount))
    print("第{}页的评论已经写入成功".format(page))


if __name__ == '__main__':
    # 歌曲id号
    songid = 191528
    page = 1
    params, encSecKey = get_params(page)
    # 歌曲名字
    songname = "gouzhong"
    url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_' + str(songid) + '?csrf_token='
    data = {'params': params, 'encSecKey': encSecKey}
    response = get_comments_json(url, data)
    # 总页数
    total = response["total"]
    # 总页数
    pages = math.ceil(total / 20)
    while page <= pages:
        params, encSecKey = get_params(page)
        data = {'params': params, 'encSecKey': encSecKey}
        response = get_comments_json(url, data)
        save_comments(response["comments"], songname, page)
        page += 1
