import requests
import json

header = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Host": "data.cma.cn",
    "Referer": "http://data.cma.cn/data/weatherBk.html",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

province_code = ["110", "120", "130", "140", "150", "210", "220", "230", "310", "320", "330", "340",
                 "350", "360", "370", "410", "420", "430", "440", "450", "460", "500", "510", "520", "530",
                 "540", "610", "620", "630", "640", "650"]


def get_station_id(provincecode):
    url = "http://data.cma.cn/weatherGis/web/bmd/stationinfo/getStationSurf"
    param = {
        "provincecode": str(provincecode)
    }
    try:
        r = requests.get(url, params=param, headers=header, timeout=12)
        r.raise_for_status()
        return json.loads(r.text)
    except:
        return None
