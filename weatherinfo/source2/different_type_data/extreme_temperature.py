import requests
import json
from queue import SimpleQueue
import pandas
import time
from source2.tool import header, province_code, get_station_id

failure_count = 2


def get_extreme_temperature(station_id):
    result = list()
    url = "http://data.cma.cn/weatherGis/web/dataservice/AppData/list"
    param = {
        "id": "extreme_temperature",
        "stationID": station_id
    }
    try:
        r = requests.get(url, params=param, timeout=12, headers=header)
        r.raise_for_status()
        data = json.loads(r.text)
        for item in data:
            result.append({
                "month": item["V04002"],
                "min": item["V12012"],
                "max": item["V12011"]
            })
        return result
    except:
        return None


def save_in_file(genre, data):
    file_path = "D:\\6-baiduyun\\2-数据\\8-气候标准值\\月极端气温({})(1981-2010).xls"
    header = ["站点名称", "1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
    df = pandas.DataFrame(data)
    df.to_excel(file_path.format(genre), index=False, header=header)


def main_extreme_temperature():
    max_temperature = list()
    min_temperature = list()
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
            ret = get_extreme_temperature(task["data"])
            time.sleep(0.5)
            if ret is not None:
                max_t = [task["name"]]
                min_t = [task["name"]]
                for item in ret:
                    max_t.append(item["max"])
                    min_t.append(item["min"])
                max_temperature.append(max_t)
                min_temperature.append(min_t)
            else:
                task["count"] += 1
                task_queue.put(task)
    save_in_file("最高", max_temperature)
    save_in_file("最低", min_temperature)
