import pandas
import execjs
import json
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm
import os
from version2.classes.CityInfo import CityInfo

connectStr = "mysql+pymysql://root:root@localhost:3306/airinfodb"
engine = create_engine(connectStr, max_overflow=5)
Session = sessionmaker(bind=engine)

path = "D:\\6-baiduyun\\2-数据\\3-空气质量\\{}.xls"
header_list = ["日期", "aqi", "质量等级", "PM2.5", "PM10", "SO2", "CO", "NO2", "O3"]


def encryption_params(city, date_time, ctx):
    method = 'GETDAYDATA'
    js = 'getEncryptedData("{0}", "{1}", "{2}")'.format(method, city, date_time)
    return ctx.eval(js)


# 解码response对象
def decode_info(info, ctx):
    # decodeData(data)
    js = 'dSp17P6wE1CFXC6D("{0}")'.format(info)
    data = ctx.eval(js)
    data = json.loads(data)
    return data


def get_response(params):
    url = 'https://www.aqistudy.cn/historydata/api/historyapi.php'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
    }
    data = {
        'hmebd5PRa': params
    }
    html_info = requests.post(url, data=data, headers=headers, timeout=5)
    return html_info.text


def get_city_list():
    session = Session()
    city_list = session.query(CityInfo).all()
    return [city.cityName for city in city_list]


def append_to_file(city, city_air_info):
    file = path.format(city)
    if os.path.exists(file):
        df = pandas.read_excel(file, header=None)
        temp = pandas.DataFrame(city_air_info)
        df = df.append(temp, ignore_index=True)
        df.to_excel(file, index=False, header=False)
    else:
        df = pandas.DataFrame(city_air_info)
        df.to_excel(file, index=False, header=header_list)


def main():
    run_time = execjs.get()
    print(run_time.name)
    ctx = run_time.compile(open('interface.js', encoding='utf-8').read())

    date = "202103"
    city_list = get_city_list()[99:]
    for city in tqdm(city_list):
        city_air_info = list()
        html_info = get_response(encryption_params(city, date, ctx))
        item = decode_info(html_info, ctx)
        if item['success']:
            data_list = item['result']['data']['items']
            if len(data_list) > 0:
                for t in data_list:
                    city_air_info.append(
                        [t['time_point'], t['aqi'], t['quality'], t['pm2_5'],
                         t['pm10'], t['so2'], t['co'], t['no2'], t['o3']])
        if len(city_air_info) > 0:
            append_to_file(city, city_air_info)


if __name__ == '__main__':
    main()
