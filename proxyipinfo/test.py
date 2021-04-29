from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm
import requests
from requests.exceptions import ConnectTimeout
from requests.models import HTTPError
import time
import re
import subprocess as  sp
from classes.IpProxyPool import IpProxyPool

page_count = 3808
connectStr = "mysql+pymysql://root:root@localhost:3306/utildb"
engine = create_engine(connectStr, max_overflow=5)
Session = sessionmaker(bind=engine)

ip_pattern = re.compile('<td data-title="IP">(.+?)</td>')
port_pattern = re.compile('<td data-title="PORT">(\d+?)</td>')
anonymous_pattern = re.compile('<td data-title="匿名度">(.*?)</td>')
proxyType_pattern = re.compile('<td data-title="类型">([A-Z]+?)</td>')
location_pattern = re.compile('<td data-title="位置">(.*?)</td>')

lose_package_pattern = re.compile(u"丢失 = (\d+)", re.IGNORECASE)
average_time_pattern = re.compile(u"平均 = (\d+)", re.IGNORECASE)


# def check_ip_v1(ip):
#     cmd = "ping -n 3 -w 3 {}"
#     process = sp.Popen(cmd.format(ip), stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
#     out = process.stdout.read().decode('gbk')
#     lose_package = lose_package_pattern.findall(out)
#     if len(lose_package) == 0:
#         lose = 3
#     else:
#         lose = int(lose_package[0])
#     if lose > 2:
#         return -1
#     else:
#         average_time = average_time_pattern.findall(out)
#         if len(average_time) == 0:
#             return -1
#         else:
#             return int(average_time[0])


def check_ip_v2(ip, port):
    url = "https://www.howbuy.com/fund/005928/"
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }
    proxy = {
        'http': "http://{}:{}".format(ip, port)
    }
    try:
        r = requests.get(url, headers=header, proxies=proxy, timeout=3)
        r.raise_for_status()
        if r.status_code != 200:
            return -1
        else:
            return 0
    except Exception:
        return -1


def get_html(url):
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }
    try:
        r = requests.get(url, headers=header, timeout=1)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except (HTTPError, ConnectTimeout):
        return ""


def parse_single_page(raw_html):
    result = []
    ip_list = ip_pattern.findall(raw_html)
    port_list = port_pattern.findall(raw_html)
    anonymous_list = anonymous_pattern.findall(raw_html)
    proxyType_list = proxyType_pattern.findall(raw_html)
    location_list = location_pattern.findall(raw_html)
    for i in range(len(ip_list)):
        flag = check_ip_v2(ip_list[i], port_list[i])
        if flag == 0:
            result.append(IpProxyPool(
                ip_list[i], port_list[i], anonymous_list[i],
                proxyType_list[i], location_list[i], -1
            ))
        # average_time = check_ip_v1(ip_list[i])
        # if average_time == -1:
        #     continue
        # else:
        #     result.append(IpProxyPool(
        #         ip_list[i], port_list[i], anonymous_list[i],
        #         proxyType_list[i], location_list[i], average_time
        #     ))
    return result


def main():
    session = Session()
    pattern = "https://www.kuaidaili.com/free/inha/{}/"
    for index in tqdm(list(range(page_count))[300:400]):
        raw_html = get_html(pattern.format(str(index + 1)))
        data = parse_single_page(raw_html)
        if len(data) > 0:
            try:
                session.add_all(data)
                session.commit()
            except:
                session.rollback()
        time.sleep(1)


def test():
    url = "https://www.howbuy.com/fund/005928/"
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }
    proxy = {
        'http': "http://119.119.116.252:9000"
    }
    # try:
    r = requests.get(url, headers=header, proxies=proxy, timeout=3)
    r.raise_for_status()
    print("normal: " + str(r.status_code))
    # except ConnectTimeout:
    #     print("timeout")


if __name__ == '__main__':
    main()
