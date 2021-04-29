import requests
from bilibili.tool import load_cookie
import traceback
import json


def crawl_id(web_session, userid):
    result = list()
    param = {
        "vmid": userid,
        "pn": "1",
        "ps": "20",
        "order": "desc",
        "jsonp": "jsonp"
    }
    header = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "referer": "",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
    }
    fans_id = crawl_fans_id(web_session, userid, param, header)
    follows_id = crawl_follows_id(web_session, userid, param, header)
    result.extend(fans_id)
    result.extend(follows_id)
    return list(set(result))


# 只抓取前20个粉丝id
def crawl_fans_id(web_session, userid, param, header):
    header["referer"] = "".join(["https://space.bilibili.com/", str(userid), "/fans/fans"])
    url = "https://api.bilibili.com/x/relation/followers"
    web_session.headers = header
    result = list()
    try:
        r = web_session.get(url, params=param, timeout=6)
        r.raise_for_status()
        data = json.loads(r.text)
        if data.get("code") == 0:
            user_list = data.get("data").get("list")
            for user in user_list:
                result.append(user.get("mid"))
        return result
    except:
        traceback.print_exc()
        return None


# 只抓取前20个关注id
def crawl_follows_id(web_session, userid, param, header):
    header["referer"] = "".join(["https://space.bilibili.com/", str(userid), "/fans/follow"])
    url = "https://api.bilibili.com/x/relation/followings"
    web_session.headers = header
    result = list()
    try:
        r = web_session.get(url, params=param, timeout=6)
        r.raise_for_status()
        data = json.loads(r.text)
        if data.get("code") == 0:
            user_list = data.get("data").get("list")
            for user in user_list:
                result.append(user.get("mid"))
        return result
    except:
        traceback.print_exc()
        return None


if __name__ == '__main__':
    web_session = requests.session()
    cookies = load_cookie()
    for cookie in cookies:
        web_session.cookies.set(cookie["name"], cookie["value"])
    crawl_id(web_session, "22805154")
