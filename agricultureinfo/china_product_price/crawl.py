from urllib.parse import quote
import json
import requests
import cchardet

# http://zdscxx.moa.gov.cn:8080/nyb/pc/index.jsp

def crawl(item_type):
    url = "http://zdscxx.moa.gov.cn:8080/nyb/oldncpjck"
    data = {
        "item": quote("item_type")
    }
    header = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "zdscxx.moa.gov.cn:8080",
        "Referer": "http://zdscxx.moa.gov.cn:8080/nyb/pc/index.jsp",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
    }
    try:
        r = requests.post(url, headers=header, timeout=6, data=data)
        r.raise_for_status()
        encoding = cchardet.detect(r.content)
        r.encoding = encoding["encoding"]
        return r.text
    except Exception as e:
        print(e)
        return ""


def main():
    pass


if __name__ == '__main__':
    main()
