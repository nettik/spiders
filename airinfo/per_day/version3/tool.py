import os
import time
from queue import SimpleQueue

import execjs
import pandas
from tqdm import tqdm

from per_day.version3.classes.CityAirInfo import CityAirInfo
from per_day.version3.common.common_function import Session, get_city_list, get_response, encryption_params, decode_info, \
    retry_city_date


def retry(city, date, ctx):
    city_air_info = list()
    html_info = get_response(encryption_params(city, date, ctx))
    if html_info is not None:
        item = decode_info(html_info, ctx)
        if item["success"]:
            data_list = item['result']['data']['items']
            if len(data_list) > 0:
                for t in data_list:
                    city_air_info.append(
                        [t['time_point'], t['aqi'], t['quality'], t['pm2_5'],
                         t['pm10'], t['so2'], t['co'], t['no2'], t['o3']])
        else:
            return False
    else:
        return False
    if len(city_air_info) > 0:
        append_to_file(city, city_air_info)
    return True


def append_to_file(city, city_air_info):
    path = "D:\\6-baiduyun\\2-数据\\3-空气质量\\{}.xls"
    header_list = ["日期", "aqi", "质量等级", "PM2.5", "PM10", "SO2", "CO", "NO2", "O3"]
    file = path.format(city)
    if os.path.exists(file):
        df = pandas.read_excel(file, header=None)
        temp = pandas.DataFrame(city_air_info)
        df = df.append(temp, ignore_index=True)
        df.to_excel(file, index=False, header=False)
    else:
        df = pandas.DataFrame(city_air_info)
        df.to_excel(file, index=False, header=header_list)


def save_in_file():
    path = "D:\\6-baiduyun\\2-数据\\3-空气质量\\{}.xls"
    header_list = ["日期", "aqi", "质量等级", "PM2.5", "PM10", "SO2", "CO", "NO2", "O3"]
    session = Session()
    city_list = get_city_list()
    for city in tqdm(city_list):
        data = session.query(CityAirInfo).filter(CityAirInfo.cityName == city).all()
        if len(data) == 0:
            continue
        data_list = [info.to_list() for info in data]
        df = pandas.DataFrame(data_list)
        df.to_excel(path.format(city), header=header_list, index=False)
    session.close()


def update_in_db(date, session, ctx):
    city_list = get_city_list()
    fail_queue = SimpleQueue()
    for city in tqdm(city_list):
        city_air_info = list()
        html_info = get_response(encryption_params(city, date, ctx))
        if html_info is not None:
            item = decode_info(html_info, ctx)
            if item["success"]:
                data_list = item['result']['data']['items']
                if len(data_list) > 0:
                    for t in data_list:
                        city_air_info.append(CityAirInfo(
                            city,
                            t['time_point'], t['aqi'], t['quality'], t['pm2_5'],
                            t['pm10'], t['so2'], t['co'], t['no2'], t['o3']
                        ))
            else:
                fail_queue.put({
                    "city": city,
                    "date": date
                })
        else:
            fail_queue.put({
                "city": city,
                "date": date
            })
        time.sleep(0.5)
        if len(city_air_info) > 0:
            try:
                session.add_all(city_air_info)
                session.commit()
            except:
                session.rollback()
                fail_queue.put({
                    "city": city,
                    "date": date
                })
    print("需要重新下载的任务数：" + str(fail_queue.qsize()))
    while not fail_queue.empty():
        item = fail_queue.get()
        flag = retry_city_date(item["city"], item["date"], session, ctx)
        if not flag:
            fail_queue.put(item)


def update_in_file(date, ctx):
    city_list = get_city_list()
    fail_queue = SimpleQueue()
    for city in tqdm(city_list):
        city_air_info = list()
        html_info = get_response(encryption_params(city, date, ctx))
        if html_info is not None:
            item = decode_info(html_info, ctx)
            if item["success"]:
                data_list = item['result']['data']['items']
                if len(data_list) > 0:
                    for t in data_list:
                        city_air_info.append(
                            [t['time_point'], t['aqi'], t['quality'], t['pm2_5'],
                             t['pm10'], t['so2'], t['co'], t['no2'], t['o3']])
            else:
                fail_queue.put({
                    "city": city,
                    "date": date
                })
        else:
            fail_queue.put({
                "city": city,
                "date": date
            })
        if len(city_air_info) > 0:
            append_to_file(city, city_air_info)
        time.sleep(0.5)
    while not fail_queue.empty():
        item = fail_queue.get()
        flag = retry(item["city"], item["date"], ctx)
        if not flag:
            fail_queue.put(item)


def update():
    date = "202103"
    session = Session()
    run_time = execjs.get()
    ctx = run_time.compile(open('common/interface.js', encoding='utf-8').read())
    update_in_db(date, session, ctx)
    # update_in_file(date, ctx)
    session.close()


if __name__ == '__main__':
    save_in_file()
