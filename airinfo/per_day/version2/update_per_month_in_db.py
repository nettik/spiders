import json

import execjs
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm

from version2.classes.CityInfo import CityInfo
from version2.classes.CityAirInfo import CityAirInfo

connectStr = "mysql+pymysql://root:root@localhost:3306/airinfodb"
engine = create_engine(connectStr, max_overflow=5)
Session = sessionmaker(bind=engine)

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



def main():
    session = Session()
    run_time = execjs.get()
    print(run_time.name)
    ctx = run_time.compile(open('interface.js', encoding='utf-8').read())

    date = "202103"
    city_list = get_city_list()
    for city in tqdm(city_list):
        city_air_info = list()
        html_info = get_response(encryption_params(city, date, ctx))
        item = decode_info(html_info, ctx)
        if item['success']:
            data_list = item['result']['data']['items']
            if len(data_list) > 0:
                for t in data_list:
                    city_air_info.append(CityAirInfo(
                        city,
                        t['time_point'], t['aqi'], t['quality'], t['pm2_5'],
                        t['pm10'], t['so2'], t['co'], t['no2'], t['o3']
                    ))
        if len(city_air_info) > 0:
            try:
                session.add_all(city_air_info)
                session.commit()
            except Exception as e:
                print(e)
                session.rollback()


if __name__ == '__main__':
    main()
