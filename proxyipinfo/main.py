from tqdm import tqdm
import requests
import time
import re
from classes.IpProxyPool import IpProxyPool
from classes.ThreadPool import ThreadPool
from functools import wraps
import traceback

page_count = 3957

ip_pattern = re.compile('<td data-title="IP">(.+?)</td>')
port_pattern = re.compile('<td data-title="PORT">(\d+?)</td>')
anonymous_pattern = re.compile('<td data-title="匿名度">(.*?)</td>')
proxyType_pattern = re.compile('<td data-title="类型">([A-Z]+?)</td>')
location_pattern = re.compile('<td data-title="位置">(.*?)</td>')


def get_html(url):
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Host": "www.kuaidaili.com"
    }
    try:
        r = requests.get(url, headers=header, timeout=1)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        traceback.print_exc()
        return None


def parse_single_page(raw_html, thread_pool):
    ip_list = ip_pattern.findall(raw_html)
    port_list = port_pattern.findall(raw_html)
    anonymous_list = anonymous_pattern.findall(raw_html)
    proxyType_list = proxyType_pattern.findall(raw_html)
    location_list = location_pattern.findall(raw_html)
    for i in range(len(ip_list)):
        thread_pool.put_task(IpProxyPool(
            ip_list[i], port_list[i], anonymous_list[i],
            proxyType_list[i], location_list[i]
        ))


def timer(func):
    @wraps(func)
    def wrapper():
        start = time.time()
        func()
        print("\r运行时间: " + str(round((time.time() - start) / 60, 1)) + "分钟", end='')

    return wrapper


@timer
def main():
    pattern = "https://www.kuaidaili.com/free/inha/{}/"
    thread_pool = ThreadPool(6)
    thread_pool.create_thread()
    thread_pool.start_thread()
    for index in tqdm(list(range(page_count))):
        raw_html = get_html(pattern.format(str(index + 1)))
        if raw_html is not None:
            parse_single_page(raw_html, thread_pool)
        # time.sleep(1)
    thread_pool.wait_all_task_down()


def test():
    url = "https://www.baidu.com"
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }
    proxy = {
        'http': "http://175.42.158.242:9999"
    }
    r = requests.get(url, headers=header, proxies=proxy, timeout=3)
    r.raise_for_status()
    with open("data.html", 'w') as f:
        f.write(r.text)


if __name__ == '__main__':
    main()
