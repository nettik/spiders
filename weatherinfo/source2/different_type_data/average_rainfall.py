import requests
import json
from queue import SimpleQueue
import pandas
import time
from source2.tool import header, province_code, get_station_id

failure_count = 2


def get_average_rainfall(station_id):
    result = list()
    url = "http://data.cma.cn/weatherGis/web/dataservice/AppData/list"
    param = {
        "id": "average_rainfall",
        "stationID": station_id
    }
    try:
        r = requests.get(url, params=param, timeout=12, headers=header)
        r.raise_for_status()
        data = json.loads(r.text)
        for item in data:
            result.append({
                "month": item["V04002"],
                "data": item["V13306_701"]
            })
        return result
    except:
        return None


def save_in_file(data):
    file_path = "D:\\6-baiduyun\\2-数据\\8-气候标准值\\平均降水量(1981-2010).xls"
    header_list = ["站点名称", "1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
    df = pandas.DataFrame(data)
    df.to_excel(file_path, index=False, header=header_list)


def main_average_rainfall():
    average_rainfall_list = list()
    task_queue = SimpleQueue()
    for province in province_code:
        task_queue.put({
            "type": "province_code",
            "data": province,
            "count": 0
        })
    while not task_queue.empty():
        if task_queue.qsize() % 10 == 0:
            print("\r剩余任务" + str(task_queue.qsize()), end='')
        task = task_queue.get()
        if task["count"] > failure_count:
            print(task)
            continue
        if task["type"] == "province_code":
            station_id_list = get_station_id(task["data"])
            time.sleep(0.5)
            if station_id_list is None:
                task["count"] += 1
                task_queue.put(task)
            else:
                for item in station_id_list:
                    task_queue.put({
                        "type": "station_id",
                        "data": item["v01301"],
                        "count": 0,
                        "name": item["cname"]
                    })
        else:
            ret = get_average_rainfall(task["data"])
            time.sleep(0.5)
            if ret is not None:
                rainfall_t = [task["name"]]
                for item in ret:
                    rainfall_t.append(item["data"])
                average_rainfall_list.append(rainfall_t)
            else:
                task["count"] += 1
                task_queue.put(task)
    save_in_file(average_rainfall_list)
