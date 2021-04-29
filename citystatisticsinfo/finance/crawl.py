from tqdm import tqdm
import time
import requests
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from finance.classes.accommodation_dining import AccommodationDining
from finance.classes.agriculture import Agriculture
from finance.classes.construction import Construction
from finance.classes.finance import Finance
from finance.classes.gdp import Gdp
from finance.classes.industry import Industry
from finance.classes.primary import Primary
from finance.classes.secondary import Secondary
from finance.classes.tertiary import Tertiary
from finance.classes.transportation import Transportation
from finance.classes.wholesale_retail import WholesaleRetail

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

connectStr = "mysql+pymysql://root:root@localhost:3306/citystatisticsinfodb"
engine = create_engine(connectStr, max_overflow=5)
Session = sessionmaker(bind=engine)

def main():
    finance()


# 地区生产总值
def gdp():
    url = "https://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=reg&colcode=sj&wds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A020101%22%7D%5D&dfwds=%5B%7B%22wdcode%22%3A%22sj%22%2C%22valuecode%22%3A%22LAST20%22%7D%5D&k1={}"
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Host": "data.stats.gov.cn",
        "Referer": "https://data.stats.gov.cn/easyquery.htm?cn=E0103",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
    }
    try:
        r = requests.get(url.format(str(int(round(time.time() * 1000)))), headers=headers, timeout=12, verify=False)
        r.raise_for_status()
        result = {
            "北京市": Gdp("北京市"), "天津市": Gdp("天津市"), "河北省": Gdp("河北省"), "山西省": Gdp("山西省"),
            "内蒙古自治区": Gdp("内蒙古自治区"), "辽宁省": Gdp("辽宁省"), "吉林省": Gdp("吉林省"), "黑龙江省": Gdp("黑龙江省"),
            "上海市": Gdp("上海市"), "江苏省": Gdp("江苏省"), "浙江省": Gdp("浙江省"), "安徽省": Gdp("安徽省"),
            "福建省": Gdp("福建省"), "江西省": Gdp("江西省"), "山东省": Gdp("山东省"), "河南省": Gdp("河南省"),
            "湖北省": Gdp("湖北省"), "湖南省": Gdp("湖南省"), "广东省": Gdp("广东省"), "广西壮族自治区": Gdp("广西壮族自治区"),
            "海南省": Gdp("海南省"), "重庆市": Gdp("重庆市"), "四川省": Gdp("四川省"), "贵州省": Gdp("贵州省"),
            "云南省": Gdp("云南省"), "西藏自治区": Gdp("西藏自治区"), "陕西省": Gdp("陕西省"), "甘肃省": Gdp("甘肃省"),
            "青海省": Gdp("青海省"), "宁夏回族自治区": Gdp("宁夏回族自治区"), "新疆维吾尔自治区": Gdp("新疆维吾尔自治区"), "台湾省": Gdp("台湾省"),
            "香港特别行政区": Gdp("香港特别行政区"), "澳门特别行政区": Gdp("澳门特别行政区")
        }
        data = json.loads(r.text)["returndata"]["datanodes"]
        for item in tqdm(data):
            code = item["code"].split(".")
            year = code[-1]
            region = city_code[code[-2].split("_")[0]]
            data = item["data"]["data"]
            result[region].set_data(year, data)
        session = Session()
        for value in result.values():
            try:
                session.add(value)
                session.commit()
            except Exception as e:
                session.rollback()
                print(e)
    except Exception as e:
        print(e)


# 第一产业增加值
def primary():
    url = "https://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=reg&colcode=sj&wds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A020102%22%7D%5D&dfwds=%5B%7B%22wdcode%22%3A%22sj%22%2C%22valuecode%22%3A%22LAST20%22%7D%5D&k1={}"
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Host": "data.stats.gov.cn",
        "Referer": "https://data.stats.gov.cn/easyquery.htm?cn=E0103",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
    }
    try:
        r = requests.get(url.format(str(int(round(time.time() * 1000)))), headers=headers, timeout=12, verify=False)
        r.raise_for_status()
        result = {
            "北京市": Primary("北京市"), "天津市": Primary("天津市"), "河北省": Primary("河北省"), "山西省": Primary("山西省"),
            "内蒙古自治区": Primary("内蒙古自治区"), "辽宁省": Primary("辽宁省"), "吉林省": Primary("吉林省"), "黑龙江省": Primary("黑龙江省"),
            "上海市": Primary("上海市"), "江苏省": Primary("江苏省"), "浙江省": Primary("浙江省"), "安徽省": Primary("安徽省"),
            "福建省": Primary("福建省"), "江西省": Primary("江西省"), "山东省": Primary("山东省"), "河南省": Primary("河南省"),
            "湖北省": Primary("湖北省"), "湖南省": Primary("湖南省"), "广东省": Primary("广东省"), "广西壮族自治区": Primary("广西壮族自治区"),
            "海南省": Primary("海南省"), "重庆市": Primary("重庆市"), "四川省": Primary("四川省"), "贵州省": Primary("贵州省"),
            "云南省": Primary("云南省"), "西藏自治区": Primary("西藏自治区"), "陕西省": Primary("陕西省"), "甘肃省": Primary("甘肃省"),
            "青海省": Primary("青海省"), "宁夏回族自治区": Primary("宁夏回族自治区"), "新疆维吾尔自治区": Primary("新疆维吾尔自治区"), "台湾省": Primary("台湾省"),
            "香港特别行政区": Primary("香港特别行政区"), "澳门特别行政区": Primary("澳门特别行政区")
        }
        data = json.loads(r.text)["returndata"]["datanodes"]
        for item in tqdm(data):
            code = item["code"].split(".")
            year = code[-1]
            region = city_code[code[-2].split("_")[0]]
            data = item["data"]["data"]
            result[region].set_data(year, data)
        session = Session()
        for value in result.values():
            try:
                session.add(value)
                session.commit()
            except Exception as e:
                session.rollback()
                print(e)
    except Exception as e:
        print(e)


# 第二产业增加值
def secondary():
    url = "https://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=reg&colcode=sj&wds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A020103%22%7D%5D&dfwds=%5B%7B%22wdcode%22%3A%22sj%22%2C%22valuecode%22%3A%22LAST20%22%7D%5D&k1={}"
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Host": "data.stats.gov.cn",
        "Referer": "https://data.stats.gov.cn/easyquery.htm?cn=E0103",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
    }
    try:
        r = requests.get(url.format(str(int(round(time.time() * 1000)))), headers=headers, timeout=12, verify=False)
        r.raise_for_status()
        result = {
            "北京市": Secondary("北京市"), "天津市": Secondary("天津市"), "河北省": Secondary("河北省"), "山西省": Secondary("山西省"),
            "内蒙古自治区": Secondary("内蒙古自治区"), "辽宁省": Secondary("辽宁省"), "吉林省": Secondary("吉林省"), "黑龙江省": Secondary("黑龙江省"),
            "上海市": Secondary("上海市"), "江苏省": Secondary("江苏省"), "浙江省": Secondary("浙江省"), "安徽省": Secondary("安徽省"),
            "福建省": Secondary("福建省"), "江西省": Secondary("江西省"), "山东省": Secondary("山东省"), "河南省": Secondary("河南省"),
            "湖北省": Secondary("湖北省"), "湖南省": Secondary("湖南省"), "广东省": Secondary("广东省"), "广西壮族自治区": Secondary("广西壮族自治区"),
            "海南省": Secondary("海南省"), "重庆市": Secondary("重庆市"), "四川省": Secondary("四川省"), "贵州省": Secondary("贵州省"),
            "云南省": Secondary("云南省"), "西藏自治区": Secondary("西藏自治区"), "陕西省": Secondary("陕西省"), "甘肃省": Secondary("甘肃省"),
            "青海省": Secondary("青海省"), "宁夏回族自治区": Secondary("宁夏回族自治区"), "新疆维吾尔自治区": Secondary("新疆维吾尔自治区"), "台湾省": Secondary("台湾省"),
            "香港特别行政区": Secondary("香港特别行政区"), "澳门特别行政区": Secondary("澳门特别行政区")
        }
        data = json.loads(r.text)["returndata"]["datanodes"]
        for item in tqdm(data):
            code = item["code"].split(".")
            year = code[-1]
            region = city_code[code[-2].split("_")[0]]
            data = item["data"]["data"]
            result[region].set_data(year, data)
        session = Session()
        for value in result.values():
            try:
                session.add(value)
                session.commit()
            except Exception as e:
                session.rollback()
                print(e)
    except Exception as e:
        print(e)


# 第三产业增加值
def tertiary():
    url = "https://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=reg&colcode=sj&wds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A020104%22%7D%5D&dfwds=%5B%7B%22wdcode%22%3A%22sj%22%2C%22valuecode%22%3A%22LAST20%22%7D%5D&k1={}"
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Host": "data.stats.gov.cn",
        "Referer": "https://data.stats.gov.cn/easyquery.htm?cn=E0103",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
    }
    try:
        r = requests.get(url.format(str(int(round(time.time() * 1000)))), headers=headers, timeout=12, verify=False)
        r.raise_for_status()
        result = {
            "北京市": Tertiary("北京市"), "天津市": Tertiary("天津市"), "河北省": Tertiary("河北省"), "山西省": Tertiary("山西省"),
            "内蒙古自治区": Tertiary("内蒙古自治区"), "辽宁省": Tertiary("辽宁省"), "吉林省": Tertiary("吉林省"), "黑龙江省": Tertiary("黑龙江省"),
            "上海市": Tertiary("上海市"), "江苏省": Tertiary("江苏省"), "浙江省": Tertiary("浙江省"), "安徽省": Tertiary("安徽省"),
            "福建省": Tertiary("福建省"), "江西省": Tertiary("江西省"), "山东省": Tertiary("山东省"), "河南省": Tertiary("河南省"),
            "湖北省": Tertiary("湖北省"), "湖南省": Tertiary("湖南省"), "广东省": Tertiary("广东省"), "广西壮族自治区": Tertiary("广西壮族自治区"),
            "海南省": Tertiary("海南省"), "重庆市": Tertiary("重庆市"), "四川省": Tertiary("四川省"), "贵州省": Tertiary("贵州省"),
            "云南省": Tertiary("云南省"), "西藏自治区": Tertiary("西藏自治区"), "陕西省": Tertiary("陕西省"), "甘肃省": Tertiary("甘肃省"),
            "青海省": Tertiary("青海省"), "宁夏回族自治区": Tertiary("宁夏回族自治区"), "新疆维吾尔自治区": Tertiary("新疆维吾尔自治区"), "台湾省": Tertiary("台湾省"),
            "香港特别行政区": Tertiary("香港特别行政区"), "澳门特别行政区": Tertiary("澳门特别行政区")
        }
        data = json.loads(r.text)["returndata"]["datanodes"]
        for item in tqdm(data):
            code = item["code"].split(".")
            year = code[-1]
            region = city_code[code[-2].split("_")[0]]
            data = item["data"]["data"]
            result[region].set_data(year, data)
        session = Session()
        for value in result.values():
            try:
                session.add(value)
                session.commit()
            except Exception as e:
                session.rollback()
                print(e)
    except Exception as e:
        print(e)


# 农林牧渔增加值
def agriculture():
    url = "https://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=reg&colcode=sj&wds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A020105%22%7D%5D&dfwds=%5B%7B%22wdcode%22%3A%22sj%22%2C%22valuecode%22%3A%22LAST20%22%7D%5D&k1={}"
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Host": "data.stats.gov.cn",
        "Referer": "https://data.stats.gov.cn/easyquery.htm?cn=E0103",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
    }
    try:
        r = requests.get(url.format(str(int(round(time.time() * 1000)))), headers=headers, timeout=12, verify=False)
        r.raise_for_status()
        result = {
            "北京市": Agriculture("北京市"), "天津市": Agriculture("天津市"), "河北省": Agriculture("河北省"), "山西省": Agriculture("山西省"),
            "内蒙古自治区": Agriculture("内蒙古自治区"), "辽宁省": Agriculture("辽宁省"), "吉林省": Agriculture("吉林省"), "黑龙江省": Agriculture("黑龙江省"),
            "上海市": Agriculture("上海市"), "江苏省": Agriculture("江苏省"), "浙江省": Agriculture("浙江省"), "安徽省": Agriculture("安徽省"),
            "福建省": Agriculture("福建省"), "江西省": Agriculture("江西省"), "山东省": Agriculture("山东省"), "河南省": Agriculture("河南省"),
            "湖北省": Agriculture("湖北省"), "湖南省": Agriculture("湖南省"), "广东省": Agriculture("广东省"), "广西壮族自治区": Agriculture("广西壮族自治区"),
            "海南省": Agriculture("海南省"), "重庆市": Agriculture("重庆市"), "四川省": Agriculture("四川省"), "贵州省": Agriculture("贵州省"),
            "云南省": Agriculture("云南省"), "西藏自治区": Agriculture("西藏自治区"), "陕西省": Agriculture("陕西省"), "甘肃省": Agriculture("甘肃省"),
            "青海省": Agriculture("青海省"), "宁夏回族自治区": Agriculture("宁夏回族自治区"), "新疆维吾尔自治区": Agriculture("新疆维吾尔自治区"), "台湾省": Agriculture("台湾省"),
            "香港特别行政区": Agriculture("香港特别行政区"), "澳门特别行政区": Agriculture("澳门特别行政区")
        }
        data = json.loads(r.text)["returndata"]["datanodes"]
        for item in tqdm(data):
            code = item["code"].split(".")
            year = code[-1]
            region = city_code[code[-2].split("_")[0]]
            data = item["data"]["data"]
            result[region].set_data(year, data)
        session = Session()
        for value in result.values():
            try:
                session.add(value)
                session.commit()
            except Exception as e:
                session.rollback()
                print(e)
    except Exception as e:
        print(e)


# 工业增加值
def industry():
    url = "https://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=reg&colcode=sj&wds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A020106%22%7D%5D&dfwds=%5B%7B%22wdcode%22%3A%22sj%22%2C%22valuecode%22%3A%22LAST20%22%7D%5D&k1={}"
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Host": "data.stats.gov.cn",
        "Referer": "https://data.stats.gov.cn/easyquery.htm?cn=E0103",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
    }
    try:
        r = requests.get(url.format(str(int(round(time.time() * 1000)))), headers=headers, timeout=12, verify=False)
        r.raise_for_status()
        result = {
            "北京市": Industry("北京市"), "天津市": Industry("天津市"), "河北省": Industry("河北省"), "山西省": Industry("山西省"),
            "内蒙古自治区": Industry("内蒙古自治区"), "辽宁省": Industry("辽宁省"), "吉林省": Industry("吉林省"), "黑龙江省": Industry("黑龙江省"),
            "上海市": Industry("上海市"), "江苏省": Industry("江苏省"), "浙江省": Industry("浙江省"), "安徽省": Industry("安徽省"),
            "福建省": Industry("福建省"), "江西省": Industry("江西省"), "山东省": Industry("山东省"), "河南省": Industry("河南省"),
            "湖北省": Industry("湖北省"), "湖南省": Industry("湖南省"), "广东省": Industry("广东省"), "广西壮族自治区": Industry("广西壮族自治区"),
            "海南省": Industry("海南省"), "重庆市": Industry("重庆市"), "四川省": Industry("四川省"), "贵州省": Industry("贵州省"),
            "云南省": Industry("云南省"), "西藏自治区": Industry("西藏自治区"), "陕西省": Industry("陕西省"), "甘肃省": Industry("甘肃省"),
            "青海省": Industry("青海省"), "宁夏回族自治区": Industry("宁夏回族自治区"), "新疆维吾尔自治区": Industry("新疆维吾尔自治区"), "台湾省": Industry("台湾省"),
            "香港特别行政区": Industry("香港特别行政区"), "澳门特别行政区": Industry("澳门特别行政区")
        }
        data = json.loads(r.text)["returndata"]["datanodes"]
        for item in tqdm(data):
            code = item["code"].split(".")
            year = code[-1]
            region = city_code[code[-2].split("_")[0]]
            data = item["data"]["data"]
            result[region].set_data(year, data)
        session = Session()
        for value in result.values():
            try:
                session.add(value)
                session.commit()
            except Exception as e:
                session.rollback()
                print(e)
    except Exception as e:
        print(e)


# 建筑业增加值
def construction():
    url = "https://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=reg&colcode=sj&wds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A020107%22%7D%5D&dfwds=%5B%7B%22wdcode%22%3A%22sj%22%2C%22valuecode%22%3A%22LAST20%22%7D%5D&k1={}"
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Host": "data.stats.gov.cn",
        "Referer": "https://data.stats.gov.cn/easyquery.htm?cn=E0103",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
    }
    try:
        r = requests.get(url.format(str(int(round(time.time() * 1000)))), headers=headers, timeout=12, verify=False)
        r.raise_for_status()
        result = {
            "北京市": Construction("北京市"), "天津市": Construction("天津市"), "河北省": Construction("河北省"), "山西省": Construction("山西省"),
            "内蒙古自治区": Construction("内蒙古自治区"), "辽宁省": Construction("辽宁省"), "吉林省": Construction("吉林省"), "黑龙江省": Construction("黑龙江省"),
            "上海市": Construction("上海市"), "江苏省": Construction("江苏省"), "浙江省": Construction("浙江省"), "安徽省": Construction("安徽省"),
            "福建省": Construction("福建省"), "江西省": Construction("江西省"), "山东省": Construction("山东省"), "河南省": Construction("河南省"),
            "湖北省": Construction("湖北省"), "湖南省": Construction("湖南省"), "广东省": Construction("广东省"), "广西壮族自治区": Construction("广西壮族自治区"),
            "海南省": Construction("海南省"), "重庆市": Construction("重庆市"), "四川省": Construction("四川省"), "贵州省": Construction("贵州省"),
            "云南省": Construction("云南省"), "西藏自治区": Construction("西藏自治区"), "陕西省": Construction("陕西省"), "甘肃省": Construction("甘肃省"),
            "青海省": Construction("青海省"), "宁夏回族自治区": Construction("宁夏回族自治区"), "新疆维吾尔自治区": Construction("新疆维吾尔自治区"), "台湾省": Construction("台湾省"),
            "香港特别行政区": Construction("香港特别行政区"), "澳门特别行政区": Construction("澳门特别行政区")
        }
        data = json.loads(r.text)["returndata"]["datanodes"]
        for item in tqdm(data):
            code = item["code"].split(".")
            year = code[-1]
            region = city_code[code[-2].split("_")[0]]
            data = item["data"]["data"]
            result[region].set_data(year, data)
        session = Session()
        for value in result.values():
            try:
                session.add(value)
                session.commit()
            except Exception as e:
                session.rollback()
                print(e)
    except Exception as e:
        print(e)


# 批发和零售业增加值
def wholesale_retail():
    url = "https://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=reg&colcode=sj&wds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A020108%22%7D%5D&dfwds=%5B%7B%22wdcode%22%3A%22sj%22%2C%22valuecode%22%3A%22LAST20%22%7D%5D&k1={}"
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Host": "data.stats.gov.cn",
        "Referer": "https://data.stats.gov.cn/easyquery.htm?cn=E0103",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
    }
    try:
        r = requests.get(url.format(str(int(round(time.time() * 1000)))), headers=headers, timeout=12, verify=False)
        r.raise_for_status()
        result = {
            "北京市": WholesaleRetail("北京市"), "天津市": WholesaleRetail("天津市"), "河北省": WholesaleRetail("河北省"), "山西省": WholesaleRetail("山西省"),
            "内蒙古自治区": WholesaleRetail("内蒙古自治区"), "辽宁省": WholesaleRetail("辽宁省"), "吉林省": WholesaleRetail("吉林省"), "黑龙江省": WholesaleRetail("黑龙江省"),
            "上海市": WholesaleRetail("上海市"), "江苏省": WholesaleRetail("江苏省"), "浙江省": WholesaleRetail("浙江省"), "安徽省": WholesaleRetail("安徽省"),
            "福建省": WholesaleRetail("福建省"), "江西省": WholesaleRetail("江西省"), "山东省": WholesaleRetail("山东省"), "河南省": WholesaleRetail("河南省"),
            "湖北省": WholesaleRetail("湖北省"), "湖南省": WholesaleRetail("湖南省"), "广东省": WholesaleRetail("广东省"), "广西壮族自治区": WholesaleRetail("广西壮族自治区"),
            "海南省": WholesaleRetail("海南省"), "重庆市": WholesaleRetail("重庆市"), "四川省": WholesaleRetail("四川省"), "贵州省": WholesaleRetail("贵州省"),
            "云南省": WholesaleRetail("云南省"), "西藏自治区": WholesaleRetail("西藏自治区"), "陕西省": WholesaleRetail("陕西省"), "甘肃省": WholesaleRetail("甘肃省"),
            "青海省": WholesaleRetail("青海省"), "宁夏回族自治区": WholesaleRetail("宁夏回族自治区"), "新疆维吾尔自治区": WholesaleRetail("新疆维吾尔自治区"), "台湾省": WholesaleRetail("台湾省"),
            "香港特别行政区": WholesaleRetail("香港特别行政区"), "澳门特别行政区": WholesaleRetail("澳门特别行政区")
        }
        data = json.loads(r.text)["returndata"]["datanodes"]
        for item in tqdm(data):
            code = item["code"].split(".")
            year = code[-1]
            region = city_code[code[-2].split("_")[0]]
            data = item["data"]["data"]
            result[region].set_data(year, data)
        session = Session()
        for value in result.values():
            try:
                session.add(value)
                session.commit()
            except Exception as e:
                session.rollback()
                print(e)
    except Exception as e:
        print(e)


# 交通运输、仓储和邮政增加值
def transportation():
    url = "https://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=reg&colcode=sj&wds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A02010A%22%7D%5D&dfwds=%5B%7B%22wdcode%22%3A%22sj%22%2C%22valuecode%22%3A%22LAST20%22%7D%5D&k1={}"
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Host": "data.stats.gov.cn",
        "Referer": "https://data.stats.gov.cn/easyquery.htm?cn=E0103",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
    }
    try:
        r = requests.get(url.format(str(int(round(time.time() * 1000)))), headers=headers, timeout=12, verify=False)
        r.raise_for_status()
        result = {
            "北京市": Transportation("北京市"), "天津市": Transportation("天津市"), "河北省": Transportation("河北省"), "山西省": Transportation("山西省"),
            "内蒙古自治区": Transportation("内蒙古自治区"), "辽宁省": Transportation("辽宁省"), "吉林省": Transportation("吉林省"), "黑龙江省": Transportation("黑龙江省"),
            "上海市": Transportation("上海市"), "江苏省": Transportation("江苏省"), "浙江省": Transportation("浙江省"), "安徽省": Transportation("安徽省"),
            "福建省": Transportation("福建省"), "江西省": Transportation("江西省"), "山东省": Transportation("山东省"), "河南省": Transportation("河南省"),
            "湖北省": Transportation("湖北省"), "湖南省": Transportation("湖南省"), "广东省": Transportation("广东省"), "广西壮族自治区": Transportation("广西壮族自治区"),
            "海南省": Transportation("海南省"), "重庆市": Transportation("重庆市"), "四川省": Transportation("四川省"), "贵州省": Transportation("贵州省"),
            "云南省": Transportation("云南省"), "西藏自治区": Transportation("西藏自治区"), "陕西省": Transportation("陕西省"), "甘肃省": Transportation("甘肃省"),
            "青海省": Transportation("青海省"), "宁夏回族自治区": Transportation("宁夏回族自治区"), "新疆维吾尔自治区": Transportation("新疆维吾尔自治区"), "台湾省": Transportation("台湾省"),
            "香港特别行政区": Transportation("香港特别行政区"), "澳门特别行政区": Transportation("澳门特别行政区")
        }
        data = json.loads(r.text)["returndata"]["datanodes"]
        for item in tqdm(data):
            code = item["code"].split(".")
            year = code[-1]
            region = city_code[code[-2].split("_")[0]]
            data = item["data"]["data"]
            result[region].set_data(year, data)
        session = Session()
        for value in result.values():
            try:
                session.add(value)
                session.commit()
            except Exception as e:
                session.rollback()
                print(e)
    except Exception as e:
        print(e)


# 住宿和餐饮增加值
def accommodation_dining():
    url = "https://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=reg&colcode=sj&wds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A02010C%22%7D%5D&dfwds=%5B%7B%22wdcode%22%3A%22sj%22%2C%22valuecode%22%3A%22LAST20%22%7D%5D&k1={}"
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Host": "data.stats.gov.cn",
        "Referer": "https://data.stats.gov.cn/easyquery.htm?cn=E0103",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
    }
    try:
        r = requests.get(url.format(str(int(round(time.time() * 1000)))), headers=headers, timeout=12, verify=False)
        r.raise_for_status()
        result = {
            "北京市": AccommodationDining("北京市"), "天津市": AccommodationDining("天津市"), "河北省": AccommodationDining("河北省"), "山西省": AccommodationDining("山西省"),
            "内蒙古自治区": AccommodationDining("内蒙古自治区"), "辽宁省": AccommodationDining("辽宁省"), "吉林省": AccommodationDining("吉林省"), "黑龙江省": AccommodationDining("黑龙江省"),
            "上海市": AccommodationDining("上海市"), "江苏省": AccommodationDining("江苏省"), "浙江省": AccommodationDining("浙江省"), "安徽省": AccommodationDining("安徽省"),
            "福建省": AccommodationDining("福建省"), "江西省": AccommodationDining("江西省"), "山东省": AccommodationDining("山东省"), "河南省": AccommodationDining("河南省"),
            "湖北省": AccommodationDining("湖北省"), "湖南省": AccommodationDining("湖南省"), "广东省": AccommodationDining("广东省"), "广西壮族自治区": AccommodationDining("广西壮族自治区"),
            "海南省": AccommodationDining("海南省"), "重庆市": AccommodationDining("重庆市"), "四川省": AccommodationDining("四川省"), "贵州省": AccommodationDining("贵州省"),
            "云南省": AccommodationDining("云南省"), "西藏自治区": AccommodationDining("西藏自治区"), "陕西省": AccommodationDining("陕西省"), "甘肃省": AccommodationDining("甘肃省"),
            "青海省": AccommodationDining("青海省"), "宁夏回族自治区": AccommodationDining("宁夏回族自治区"), "新疆维吾尔自治区": AccommodationDining("新疆维吾尔自治区"), "台湾省": AccommodationDining("台湾省"),
            "香港特别行政区": AccommodationDining("香港特别行政区"), "澳门特别行政区": AccommodationDining("澳门特别行政区")
        }
        data = json.loads(r.text)["returndata"]["datanodes"]
        for item in tqdm(data):
            code = item["code"].split(".")
            year = code[-1]
            region = city_code[code[-2].split("_")[0]]
            data = item["data"]["data"]
            result[region].set_data(year, data)
        session = Session()
        for value in result.values():
            try:
                session.add(value)
                session.commit()
            except Exception as e:
                session.rollback()
                print(e)
    except Exception as e:
        print(e)


# 金融增加值
def finance():
    url = "https://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=reg&colcode=sj&wds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A02010D%22%7D%5D&dfwds=%5B%7B%22wdcode%22%3A%22sj%22%2C%22valuecode%22%3A%22LAST20%22%7D%5D&k1={}"
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Host": "data.stats.gov.cn",
        "Referer": "https://data.stats.gov.cn/easyquery.htm?cn=E0103",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
    }
    try:
        r = requests.get(url.format(str(int(round(time.time() * 1000)))), headers=headers, timeout=12, verify=False)
        r.raise_for_status()
        result = {
            "北京市": Finance("北京市"), "天津市": Finance("天津市"), "河北省": Finance("河北省"), "山西省": Finance("山西省"),
            "内蒙古自治区": Finance("内蒙古自治区"), "辽宁省": Finance("辽宁省"), "吉林省": Finance("吉林省"), "黑龙江省": Finance("黑龙江省"),
            "上海市": Finance("上海市"), "江苏省": Finance("江苏省"), "浙江省": Finance("浙江省"), "安徽省": Finance("安徽省"),
            "福建省": Finance("福建省"), "江西省": Finance("江西省"), "山东省": Finance("山东省"), "河南省": Finance("河南省"),
            "湖北省": Finance("湖北省"), "湖南省": Finance("湖南省"), "广东省": Finance("广东省"), "广西壮族自治区": Finance("广西壮族自治区"),
            "海南省": Finance("海南省"), "重庆市": Finance("重庆市"), "四川省": Finance("四川省"), "贵州省": Finance("贵州省"),
            "云南省": Finance("云南省"), "西藏自治区": Finance("西藏自治区"), "陕西省": Finance("陕西省"), "甘肃省": Finance("甘肃省"),
            "青海省": Finance("青海省"), "宁夏回族自治区": Finance("宁夏回族自治区"), "新疆维吾尔自治区": Finance("新疆维吾尔自治区"), "台湾省": Finance("台湾省"),
            "香港特别行政区": Finance("香港特别行政区"), "澳门特别行政区": Finance("澳门特别行政区")
        }
        data = json.loads(r.text)["returndata"]["datanodes"]
        for item in tqdm(data):
            code = item["code"].split(".")
            year = code[-1]
            region = city_code[code[-2].split("_")[0]]
            data = item["data"]["data"]
            result[region].set_data(year, data)
        session = Session()
        for value in result.values():
            try:
                session.add(value)
                session.commit()
            except Exception as e:
                session.rollback()
                print(e)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
