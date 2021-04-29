import json
import execjs
import requests
from datetime import datetime, timedelta
from tqdm import tqdm
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from version2.classes.CityInfo import CityInfo
from version2.classes.CityAirInfo import CityAirInfo
import traceback


def encryption_params(city, date_time, ctx):
    method = 'GETDAYDATA'
    js = 'getEncryptedData("{0}", "{1}", "{2}")'.format(method, city, date_time)
    return ctx.eval(js)


# 解码response对象
def decode_info(info, ctx):
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
    try:
        html_info = requests.post(url, data=data, headers=headers, timeout=12)
        html_info.raise_for_status()
        return html_info.text
    except:
        traceback.print_exc()
        return None


connectStr = "mysql+pymysql://root:root@localhost:3306/airinfodb"
engine = create_engine(connectStr, max_overflow=5)
Session = sessionmaker(bind=engine)


def get_month_list(start_date="201312", end_date="202101"):
    month_list = list()
    date = start_date[:]
    dt = datetime.strptime(start_date, "%Y%m")
    while date <= end_date:
        month_list.append(date)
        dt = dt + timedelta(weeks=3)
        date = datetime.strftime(dt, "%Y%m")
    return sorted(list(set(month_list)))


def get_city_list():
    session = Session()
    city_list = session.query(CityInfo).all()
    return [city.cityName for city in city_list]


# 执行js对请求参数和响应进行加密解密以获取数据
# 可进行多线程优化
def main():
    session = Session()
    node = execjs.get()
    ctx = node.compile(open('interface.js', encoding='utf-8').read())

    date_list = get_month_list()
    city_list = get_city_list()
    for city in tqdm(city_list):
        city_air_info = list()
        for date in date_list:
            html_info = get_response(encryption_params(city, date, ctx))
            if html_info is not None:
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
            time.sleep(0.5)
        try:
            session.add_all(city_air_info)
            session.commit()
        except:
            session.rollback()
            traceback.print_exc()
    session.close()


if __name__ == '__main__':
    main()
