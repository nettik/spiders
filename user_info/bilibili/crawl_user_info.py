import json
import traceback

import requests

from bilibili.classes.BUserInfo import BUserInfo
from bilibili.tool import load_cookie


def get_user_info(web_session, user_info, user_id):
    header = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "origin": "https://space.bilibili.com",
        "referer": "".join(["https://space.bilibili.com/", str(user_id), "/"]),
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
    }
    web_session.headers = header
    flag = get_base_info(web_session, user_info, user_id)
    if flag:
        get_fans_follows(web_session, user_info, user_id)
        get_likes_articles_archives(web_session, user_info, user_id)
        get_tags(web_session, user_info, user_id)
    return flag


# 基本信息（生日、等级、id、名称、性别、个性签名）
def get_base_info(web_session, user_info, userid):
    param = {
        "mid": userid,
        "jsonp": "jsonp"
    }
    url = "https://api.bilibili.com/x/space/acc/info"
    try:
        r = web_session.get(url, params=param, timeout=6)
        r.raise_for_status()
        data = json.loads(r.text)
        if data.get("code") == 0:
            data_t = data.get("data")
            user_info.set_birthday(data_t.get("birthday"))
            user_info.set_level(data_t.get("level"))
            user_info.set_userid(userid)
            user_info.set_name(data_t.get("name"))
            user_info.set_gender(data_t.get("sex"))
            user_info.set_sign(data_t.get("sign"))
        return True
    except:
        traceback.print_exc()
        return False


# 粉丝和关注数
def get_fans_follows(web_session, user_info, userid):
    param = {
        "vmid": userid,
        "jsonp": "jsonp"
    }
    url = "https://api.bilibili.com/x/relation/stat"
    try:
        r = web_session.get(url, params=param, timeout=6)
        r.raise_for_status()
        data = json.loads(r.text)
        if data.get("code") == 0:
            user_info.set_fans(data.get("data").get("follower"))
            user_info.set_follows(data.get("data").get("following"))
    except:
        traceback.print_exc()


# 播放阅读获赞数
def get_likes_articles_archives(web_session, user_info, userid):
    param = {
        "mid": userid,
        "jsonp": "jsonp"
    }
    url = "https://api.bilibili.com/x/space/upstat"
    try:
        r = web_session.get(url, params=param, timeout=6)
        r.raise_for_status()
        data = json.loads(r.text)
        if data.get("code") == 0:
            user_info.set_likes(data.get("data").get("likes"))
            user_info.set_articles(data.get("data").get("article").get("view"))
            user_info.set_archives(data.get("data").get("archive").get("view"))
    except:
        traceback.print_exc()


# 标签
def get_tags(web_session, user_info, userid):
    param = {
        "mid": userid,
        "jsonp": "jsonp"
    }
    url = "https://api.bilibili.com/x/space/acc/tags"
    try:
        r = web_session.get(url, params=param, timeout=6)
        r.raise_for_status()
        data = json.loads(r.text)
        if data.get("code") == 0:
            tag_list = data.get("data")[0].get("tags")
            if tag_list is not None:
                user_info.set_tags(",".join(tag_list))
    except:
        traceback.print_exc()


if __name__ == '__main__':
    user_info = BUserInfo()
    web_session = requests.session()
    cookies = load_cookie()
    for cookie in cookies:
        web_session.cookies.set(cookie["name"], cookie["value"])
    get_user_info(web_session, user_info, "22805154")
