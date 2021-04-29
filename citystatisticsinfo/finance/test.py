import time
import requests

city_code = {
    "110000": "北京市", "120000": "天津市", "130000": "河北省", "140000": "山西省",
    "150000": "内蒙古自治区", "210000": "辽宁省", "220000": "吉林省", "230000": "黑龙江省",
    "310000": "上海市", "320000": "江苏省", "330000": "浙江省", "340000": "安徽省",
    "350000": "福建省", "360000": "江西省", "370000": "山东省", "410000": "河南省",
    "420000": "湖北省", "430000": "湖南省", "440000": "广东省", "450000": "广西壮族自治区",
    "460000": "海南省", "500000": "重庆市", "510000": "四川省", "520000": "贵州省",
    "530000": "云南省", "540000": "西藏自治区", "610000": "陕西省", "620000": "甘肃省",
    "630000": "青海省", "640000": "宁夏回族自治区", "650000": "新疆维吾尔自治区", "710000": "台湾省",
    "810000": "香港特别行政区", "820000": "澳门特别行政区"
}


# 地区生产总值
def gdp():
    url = "https://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=reg&colcode=sj&wds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A020101%22%7D%5D&dfwds=%5B%7B%22wdcode%22%3A%22sj%22%2C%22valuecode%22%3A%22LAST20%22%7D%5D&k1={}"
    # url = "https://data.stats.gov.cn/easyquery.htm"
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Host": "data.stats.gov.cn",
        "Referer": "https://data.stats.gov.cn/easyquery.htm?cn=E0103",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
    }
    params = {
        "m": "QueryData",
        "dbcode": "fsnd",
        "rowcode": "reg",
        "colcode": "sj",
        "wds": [{"wdcode": "zb", "valuecode": "A020101"}],
        "dfwds": [{"wdcode": "sj", "valuecode": "LAST20"}],
        "k1": str(int(round(time.time() * 1000)))
    }
    try:
        r = requests.get(url.format(str(int(round(time.time() * 1000)))), headers=headers, timeout=12, verify=False)
        r.raise_for_status()
        data = r.text
        a = 1
    except Exception as e:
        print(e)


# 第一产业增加值
def primary():
    pass


# 第二产业增加值
def secondary():
    pass


# 第三产业增加值
def tertiary():
    pass


# 农林牧渔增加值
def agriculture():
    pass


# 工业增加值
def industry():
    pass


# 建筑业增加值
def construction():
    pass


# 批发和零售业增加值
def wholesale_retail():
    pass


# 交通运输、仓储和邮政增加值
def transportation():
    pass


# 住宿和餐饮增加值
def accommodation_dining():
    pass


# 金融增加值
def finance():
    pass


def test():
    gdp()


if __name__ == '__main__':
    test()
