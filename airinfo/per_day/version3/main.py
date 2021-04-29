import time
import traceback
from datetime import datetime, timedelta
from queue import SimpleQueue

import execjs
from tqdm import tqdm

from per_day.version3.classes.CityAirInfo import CityAirInfo

from per_day.version3.common.common_function import get_response, encryption_params, decode_info, get_city_list, Session, \
    retry_city_date


# 获取月份列表
def get_month_list(start_date="201312", end_date="202101"):
    month_list = list()
    date = start_date[:]
    dt = datetime.strptime(start_date, "%Y%m")
    while date <= end_date:
        month_list.append(date)
        dt = dt + timedelta(weeks=3)
        date = datetime.strftime(dt, "%Y%m")
    return sorted(list(set(month_list)))


# 重新下载单个城市所有日期
def retry_city(city, db_session, ctx):
    date_list = get_month_list()
    fail_list = list()
    for date in date_list:
        city_air_info = list()
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
            else:
                fail_list.append({
                    "city": city,
                    "date": date
                })
        else:
            fail_list.append({
                "city": city,
                "date": date
            })
        time.sleep(0.5)
        try:
            db_session.add_all(city_air_info)
            db_session.commit()
        except:
            db_session.rollback()
            fail_list.append({
                "city": city,
                "date": date
            })
    return fail_list


# 增强程序鲁棒性，将报错的数据的参数记录，便于后续再爬取
def main():
    session = Session()
    node = execjs.get()
    ctx = node.compile(open('common/interface.js', encoding='utf-8').read())
    fail_queue = SimpleQueue()

    date_list = get_month_list()
    city_list = get_city_list()[2:]
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
        try:
            session.add_all(city_air_info)
            session.commit()
        except:
            session.rollback()
            fail_queue.put({
                "city": city,
                "date": None
            })
            traceback.print_exc()

    print("需要重新下载的任务数：" + str(fail_queue.qsize()))
    while not fail_queue.empty():
        item = fail_queue.get()
        if item["date"] is None:
            fails = retry_city(item["city"], session, ctx)
            for item in fails:
                fail_queue.put(item)
        else:
            flag = retry_city_date(item["city"], item["date"], session, ctx)
            if not flag:
                fail_queue.put(item)

    session.close()


if __name__ == '__main__':
    main()
