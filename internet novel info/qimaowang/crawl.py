import re

import cchardet
import requests
from selenium import webdriver
from tqdm import tqdm

from qimaowang.classes.ThreadPool import ThreadPool

ul_pattern = re.compile('<ul.*?"qm-pic-txt.*?</ul>', re.DOTALL)
id_pattern = re.compile('<a href="/shuku/(.*?)/">')


def get_cookie():
    url = "https://www.qimao.com/shuku/a-a-a-a-a-a-a-click-1/"
    driver = webdriver.Chrome()
    driver.get(url)
    cookies = driver.get_cookies()
    return cookies


def get_session(cookies):
    headers = {
        "Referer": "https://www.qimao.com/",
        "Host": "www.qimao.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
    }
    session = requests.Session()
    session.headers = headers
    for item in cookies:
        session.cookies.set(item["name"], item["value"])
    return session


def crawl(url, session):
    try:
        r = session.get(url, timeout=12)
        r.raise_for_status()
        encoding = cchardet.detect(r.content)
        r.encoding = encoding["encoding"]
        return r.text
    except Exception as e:
        print(e)
        return ""


def get_novel_id(session):
    pages = 666
    url_pattern = "https://www.qimao.com/shuku/a-a-a-a-a-a-a-click-{}/"
    id_list = list()
    for i in tqdm(range(pages)):
        html = crawl(url_pattern.format(str(i + 1)), session)
        # time.sleep(0.5)
        if html != "":
            ul_tag = ul_pattern.findall(html)
            if len(ul_tag) > 0:
                # id_t = id_pattern.findall(ul_tag[0])
                # print("第" + str(i) + "页" + str(len(id_t)))
                id_list.extend(id_pattern.findall(ul_tag[0]))
    return id_list


def main():
    cookies = get_cookie()
    session = get_session(cookies)
    thread_pool = ThreadPool(thread_num=4, cookies=cookies)
    id_list = get_novel_id(session)
    session.close()
    for id_t in id_list:
        thread_pool.put_task(id_t)
    thread_pool.create_and_start_thread()
    thread_pool.wait_all_task_done()


if __name__ == '__main__':
    main()
