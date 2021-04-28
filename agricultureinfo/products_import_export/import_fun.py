from urllib.parse import quote
import json
import requests
import cchardet

def crawl_import(year, month):
    url = "http://zdscxx.moa.gov.cn:8080/nyb/oldncpjck"
    data = {
        "year": year,
        "month": month,
        "item": quote("进口金额")
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


def parse_import(data_str):
    data_obj = json.loads(data_str)
    if data_obj["message"] == "success":
        foreign_data = data_obj["result"]["echarts"]["series"][0]["data"]
        china_data = data_obj["result"]["data"]["value"]
        return foreign_data, china_data
    return None, None
