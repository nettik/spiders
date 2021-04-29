import time

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pandas import DataFrame
from tqdm import tqdm
import time

from natural_resource.classes.petroleum import Petroleum
from natural_resource.classes.coal import Coal
from natural_resource.classes.forest import Forest
from natural_resource.classes.forest_rate import ForestRate
from natural_resource.classes.gas import Gas
from natural_resource.classes.grass import Grass
from natural_resource.classes.ground_water_resource import GroundWaterResource
from natural_resource.classes.iron import Iron
from natural_resource.classes.surface_water_resource import SurfaceWaterResource
from natural_resource.classes.water_resource import WaterResource
from natural_resource.classes.water_resource_per import WaterResourcePer
from natural_resource.classes.water_supply import WaterSupply
from natural_resource.classes.water_use import WaterUse
from natural_resource.classes.water_use_agriculture import WaterUseAgriculture
from natural_resource.classes.water_use_industry import WaterUseIndustry
from natural_resource.classes.water_use_life import WaterUseLife
from natural_resource.classes.water_use_per import WaterUsePer

file_path = "D:\\6-baiduyun\\2-数据\\6-城市统计数据\\1-资源与环境\\{}.xls"

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


def crawl(url):
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Host": "data.stats.gov.cn",
        "Referer": "https://data.stats.gov.cn/easyquery.htm?cn=E0103",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
    }
    try:
        r = requests.get(url, headers=headers, timeout=30, verify=False)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(e)
        return None


def parse(data_json, resource):
    result = dict()
    for city in city_code.values():
        obj = eval(resource + "('" + city + "')")
        result[city] = obj
    data = data_json.get("returndata").get("datanodes")
    for item in data:
        code = item["code"].split(".")
        year = code[-1]
        region = city_code[code[-2].split("_")[0]]
        data = item["data"]["data"]
        result[region].set_data(year, data)
    session = Session()
    # try:
    #     session.query(eval(resource)).delete()
    #     session.commit()
    # except Exception as e:
    #     session.rollback()
    #     print(e)
    # finally:
    #     time.sleep(0.5)
    for value in result.values():
        try:
            session.add(value)
            session.commit()
        except Exception as e:
            session.rollback()
            print(resource + "exception")


def param():
    param_dict = {
        "Petroleum_石油储量(万吨)": "https://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=reg&colcode=sj&wds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A0C0101%22%7D%5D&dfwds=%5B%5D&k1={}",
        "Coal_煤炭储量(亿吨)": "https://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=reg&colcode=sj&wds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A0C0103%22%7D%5D&dfwds=%5B%5D&k1={}",
        "Gas_天然气储量(亿立方米)": "https://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=reg&colcode=sj&wds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A0C0102%22%7D%5D&dfwds=%5B%5D&k1={}",
        "Iron_铁矿储量(亿吨)": "https://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=reg&colcode=sj&wds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A0C0104%22%7D%5D&dfwds=%5B%5D&k1={}",
        "WaterResource_水资源总量(亿立方米)": "https://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=reg&colcode=sj&wds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A0C0301%22%7D%5D&dfwds=%5B%5D&k1={}",
        "SurfaceWaterResource_地表水资源总量(亿立方米)": "https://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=reg&colcode=sj&wds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A0C0302%22%7D%5D&dfwds=%5B%5D&k1={}",
        "GroundWaterResource_地下水资源总量(亿立方米)": "https://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=reg&colcode=sj&wds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A0C0303%22%7D%5D&dfwds=%5B%5D&k1={}",
        "WaterResourcePer_人均水资源量(立方米每人)": "https://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=reg&colcode=sj&wds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A0C0305%22%7D%5D&dfwds=%5B%5D&k1={}",
        "WaterSupply_供水总量(亿立方米)": "https://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=reg&colcode=sj&wds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A0C0401%22%7D%5D&dfwds=%5B%5D&k1={}",
        "WaterUse_用水总量(亿立方米)": "https://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=reg&colcode=sj&wds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A0C0405%22%7D%5D&dfwds=%5B%5D&k1={}",
        "WaterUseAgriculture_农业用水总量(亿立方米)": "https://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=reg&colcode=sj&wds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A0C0406%22%7D%5D&dfwds=%5B%5D&k1={}",
        "WaterUseIndustry_工业用水总量(亿立方米)": "https://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=reg&colcode=sj&wds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A0C0407%22%7D%5D&dfwds=%5B%5D&k1={}",
        "WaterUseLife_生活用水总量(亿立方米)": "https://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=reg&colcode=sj&wds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A0C0408%22%7D%5D&dfwds=%5B%5D&k1={}",
        "WaterUsePer_人均用水量(立方米每人)": "https://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=reg&colcode=sj&wds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A0C040A%22%7D%5D&dfwds=%5B%5D&k1={}",
        "Forest_森林面积(万公顷)": "https://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=reg&colcode=sj&wds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A0C0A02%22%7D%5D&dfwds=%5B%5D&k1={}",
        "ForestRate_森林覆盖率": "https://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=reg&colcode=sj&wds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A0C0A04%22%7D%5D&dfwds=%5B%5D&k1={}",
        "Grass_草原总面积(千公顷)": "https://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=reg&colcode=sj&wds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A0C0D01%22%7D%5D&dfwds=%5B%5D&k1={}"
    }
    return param_dict


def save_in_file(clasz, file_name):
    header_list = ["地区", "2020年", "2019年", "2018年", "2017年", "2016年", "2015年", "2014年", "2013年",
                   "2012年", "2011年", "2010年", "2009年", "2008年", "2007年", "2006年", "2005年",
                   "2004年", "2004年", "2002年", "2001年", "2000年"]
    session = Session()
    data = session.query(eval(clasz)).all()
    data_list = [item.to_list() for item in data]
    df = DataFrame(data_list)
    df.to_excel(file_path.format(file_name), index=False, header=header_list)


def main():
    param_dict = param()
    for item in tqdm(param_dict.items()):
        url = item[1].format(str(int(time.time() * 1000)))
        data_json = crawl(url)
        if data_json is not None and data_json.get("returncode") == 200:
            parse(data_json, item[0].split("_")[0])
            save_in_file(item[0].split("_")[0], item[0].split("_")[1])
        time.sleep(1)


if __name__ == '__main__':
    main()
