import json
import requests
import re
import traceback
import json
import time
import tqdm

# fund_id = "005660"
url_pattern = "https://static.howbuy.com/??/upload/auto/script/fund/jzzs_{}.js,/upload/auto/script/fund/jjjl_{}.js,/upload/auto/script/fund/data_{}.js"

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Host": "static.howbuy.com",
    "Referer": "https://www.howbuy.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
}

data_pattern = re.compile("navStrListThreeYears:(\[.*?\]),", re.DOTALL)


def get_js(url):
    try:
        r = requests.get(url, headers=headers, timeout=6)
        r.raise_for_status()
        r.encoding = "utf-8"
        return r.text
    except:
        traceback.print_exc()
        return ""


def main():
    id_list = ["005660", "005875", "009057", "000592", "519008", "008955", "010387", "240022", "240009",
               "000601", "000780", "070013", "001475", "004698"]

    for fund_id in tqdm.tqdm(id_list):
        url = url_pattern.format(fund_id, fund_id, fund_id)
        js = get_js(url)
        data = json.loads(data_pattern.findall(js)[0].replace("\'", "\""))
        time.sleep(1)
        with open("{}.txt".format(fund_id), "a", encoding='utf-8') as f:
            for item in data:
                data_list = item.split(",")
                date = data_list[0] + "-" + str(int(data_list[1]) + 1) + "-" + data_list[2]
                # 基金单位净值
                fund_price_per_day = data_list[-4]
                percent = data_list[3]
                f.write(date + " " + fund_price_per_day + " " + percent + "\n")


if __name__ == '__main__':
    main()
