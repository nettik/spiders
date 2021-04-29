import requests
import re
import json
from tqdm import tqdm
from fund_infoV3.classes.Tool import Tool


def check_ip(ip, port):
    url = "https://ip.cn/api/index?ip=&type=0"
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
        'referer': "https://ip.cn/",
        'accept-language': "zh-CN,zh;q=0.9",
        'accept': "application/json, text/javascript, */*; q=0.01"
    }
    proxy = {
        'https': "http://{}:{}".format(ip, port)
    }
    # proxy = {
    #     'https': "http://115.221.243.160:9999"
    # }
    try:
        r = requests.get(url, headers=header, proxies=proxy, timeout=3)
        r.raise_for_status()
        req_ip = r.json()["ip"]
        if req_ip == ip:
            return 0
        return -1
    except:
        return -1


def test2():
    ips = ["115.221.243.160", "123.57.84.116", "175.42.122.175", "175.42.128.34", "175.43.59.22", "182.92.113.148"]
    ports = ["9999", "8118", "9999", "9999", "9999", "8118"]
    cnt = 0
    for i in tqdm(range(len(ips))):
        res = check_ip(ips[i], ports[i])
        if res == 0:
            print(ips[i], ports[i])


def replace_cgczbl_stock(cgczbl):
    return cgczbl.replace("\'", "\"").replace("zqmc", "\"zqmc\"").replace("zqdm", "\"zqdm\"").replace("zjbl",
                                                                                                      "\"zjbl\"").replace(
        "ccdb", "\"ccdb\"").replace("jsrq", "\"jsrq\"").replace("cgjzdList", "CgjzdList").replace("cgjzd",
                                                                                                  "\"cgjzd\"")


# 债券型
def replace_cgczbl_bond(cgczbl):
    return cgczbl.replace("\'", "\"").replace("zqmc", "\"zqmc\"").replace("zqdm", "\"zqdm\"").replace("zjbl",
                                                                                                      "\"zjbl\"").replace(
        "ccdb", "\"ccdb\"").replace("jsrq", "\"jsrq\"").replace("czjzdList", "CzjzdList").replace("czjzd",
                                                                                                  "\"czjzd\"")


def replace_zcpz(zcpz):
    return zcpz.replace("\'", "\"").replace("name", "\"name\"").replace("y", "\"y\"")


def replace_hypz(hypz):
    return hypz.replace("\'", "\"").replace("jjzc", "\"jjzc\"").replace("data", "\"data\"").replace("name",
                                                                                                    "\"name\"").replace(
        "tly", "\"x\"").replace("y", "\"y\"")


def parse_single_html(html):
    name_list = Tool.name_pattern.findall(html)
    if len(name_list) > 0:
        name = name_list[0]

    id_list = Tool.id_pattern.findall(html)
    if len(id_list) > 0:
        fundid = id_list[0]

    type_list = Tool.type_pattern.findall(html)
    if len(type_list) > 0:
        type = type_list[0]

    tag_list = Tool.tag_str_pattern.findall(html)
    if len(tag_list) > 0:
        tags = Tool.tag_pattern.findall(tag_list[0])

    build_time_list = Tool.build_time_pattern.findall(html)
    if len(build_time_list) > 0:
        build_time = build_time_list[0]

    latest_scale_list = Tool.latest_scale_pattern.findall(html)
    if len(latest_scale_list) > 0:
        latest_scale = latest_scale_list[0]

    income_list = Tool.income_str_pattern.findall(html)
    if len(income_list) > 0:
        incomes = Tool.income_pattern.findall(income_list[0])

    sharp_rate_list = Tool.sharp_rate_str_pattern.findall(html)
    if len(sharp_rate_list) > 0:
        sharp_rates = Tool.sharp_rate_pattern.findall(sharp_rate_list[0])


def main():
    url = "https://www.howbuy.com/fund/003834/"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
        'Accept-Language': "zh-CN,zh;q=0.9",
        'Referer': 'https://www.howbuy.com/fund/trade/',
        'Host': 'www.howbuy.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
    r = requests.get(url, headers=headers, timeout=3)
    r.encoding = "utf-8"
    parse_single_html(r.text)


def test1():
    url_pattern = "https://static.howbuy.com/??/upload/auto/script/fund/jzzs_{}.js,/upload/auto/script/fund/jjjl_{}.js,/upload/auto/script/fund/data_{}.js?"
    fundid = "003834"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
        'Accept-Language': "zh-CN,zh;q=0.9",
        'Referer': 'https://www.howbuy.com/',
        'Host': 'static.howbuy.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': '*/*'
    }
    r = requests.get(url_pattern.format(fundid, fundid, fundid), headers=headers, timeout=3)
    r.encoding = "utf-8"
    js = r.text
    # 持股持债比例
    cgczbl_pattern = re.compile("gpzhListData = ({.*?});")
    # 资产配置
    zcpz_pattern = re.compile("hyPieData = ({.*?});")
    # 行业配置
    hypz_pattern = re.compile("zcPieData = ({.*?});")

    cgczbl_dict = json.loads(replace_cgczbl_stock(cgczbl_pattern.findall(js)[0]))
    cgcz_list = cgczbl_dict[cgczbl_dict["lastDate"]]
    cgcz_str = cgczbl_dict["lastDate"] + ":"
    for item in cgcz_list:
        cgcz_str = cgcz_str + (item["zqmc"] + "," + item["zqdm"] + "," + str(item["zjbl"])) + ";"
    cgcz_str = cgcz_str.rstrip(";")

    zcpz_dict = json.loads(replace_zcpz(zcpz_pattern.findall(js)[0]))
    zcpz_list = zcpz_dict[zcpz_dict["lastDate"]]
    zcpz_str = zcpz_dict["lastDate"] + ":"
    for item in zcpz_list:
        zcpz_str = zcpz_str + (item["name"] + "," + str(round(item["y"], 2))) + ";"
    zcpz_str = zcpz_str.rstrip(";")

    hypz_dict = json.loads(replace_hypz(hypz_pattern.findall(js)[0]))
    hypz_list = hypz_dict[hypz_dict["lastDate"]]["data"]
    hypz_str = hypz_dict["lastDate"] + ":"
    for item in hypz_list:
        hypz_str = hypz_str + (item["name"] + "," + str(round(item["y"], 2))) + ";"
    hypz_str = hypz_str.rstrip(";")

    a = 1


if __name__ == '__main__':
    test2()
