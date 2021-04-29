import requests
import re
from tqdm import tqdm
import cchardet
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from queue import SimpleQueue
import time
from qilecai.classes.QiLeCai import QiLeCai
import pandas
from bs4 import BeautifulSoup
import html5lib

connectStr = "mysql+pymysql://root:root@localhost:3306/caipiaoinfodb"
engine = create_engine(connectStr, max_overflow=5)
Session = sessionmaker(bind=engine)

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
    "referer": "https://kaijiang.500.com/",
    "cache-control": "max-age=0",
    "accept-language": "zh-CN,zh;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}


def crawl_single_page(url):
    try:
        r = requests.get(url, headers=headers, timeout=12)
        r.raise_for_status()
        encoding = cchardet.detect(r.content)
        r.encoding = encoding["encoding"]
        return r.text
    except:
        return None


def getParam():
    root_url = "https://kaijiang.500.com/qlc.shtml"
    try:
        r = requests.get(root_url, headers=headers, timeout=6)
        r.raise_for_status()
        encoding = cchardet.detect(r.content)
        r.encoding = encoding
        div_pattern = re.compile('<div class="iSelectList">(.*?)</div>', re.DOTALL)
        div = div_pattern.findall(r.text)[0]
        link_pattern = re.compile('(\d+?).shtml')
        return link_pattern.findall(div)
    except Exception as e:
        print(e)
    return list()


date_pattern = re.compile('开奖日期.*?\d{4}年\d{1,2}月\d{1,2}日', re.DOTALL)
red_pattern = re.compile('<li class="ball_red">(\d{1,2})</li>')
blue_pattern = re.compile('<li class="ball_blue">(\d{1,2})</li>')
sale_and_pool_pattern = re.compile('<span class="cfont1.*?">(.*?)</span>', re.S)
tr_pattern = re.compile('<tr align="center">(.*?)</tr>', re.S)
td_pattern = re.compile('<td>\s+(.*?)\s+</td>')


def parse_single_page(param, page, session):
    qi_le_cai = QiLeCai(param)
    date_t = date_pattern.findall(page)
    if len(date_t) > 0:
        qi_le_cai.date = date_t[0].split('：')[-1]
    red_t = red_pattern.findall(page)
    if len(red_t) > 0:
        qi_le_cai.red1 = red_t[0]
        qi_le_cai.red2 = red_t[1]
        qi_le_cai.red3 = red_t[2]
        qi_le_cai.red4 = red_t[3]
        qi_le_cai.red5 = red_t[4]
        qi_le_cai.red6 = red_t[5]
        qi_le_cai.red7 = red_t[6]
    blue_t = blue_pattern.findall(page)
    if len(blue_t) > 0:
        qi_le_cai.blue = blue_t[0]
    sale_and_pool_t = sale_and_pool_pattern.findall(page)
    if len(sale_and_pool_t) > 0:
        qi_le_cai.sale_money = sale_and_pool_t[0]
    soup = BeautifulSoup(page, 'html5lib')
    table_t = soup.select(
        "body > div.wrap > div.kj_main01 > div.kj_main01_right > div.kjxq_box02 > div:nth-child(2) > table:nth-child(3) > tbody")
    if len(table_t) > 0:
        table = table_t[0].prettify()
        lines_list = tr_pattern.findall(table)
        if len(lines_list) > 0:
            for line in lines_list:
                cols = td_pattern.findall(line)
                if "一等奖" in line:
                    qi_le_cai.first_prize_num = cols[1]
                    qi_le_cai.first_prize_money = cols[2]
                elif "二等奖" in line:
                    qi_le_cai.second_prize_num = cols[1]
                    qi_le_cai.second_prize_money = cols[2]
                elif "三等奖" in line:
                    qi_le_cai.third_prize_num = cols[1]
                    qi_le_cai.third_prize_money = cols[2]
    try:
        session.add(qi_le_cai)
        session.commit()
        return True
    except:
        session.rollback()
        return False


def save_in_file(session):
    file_path = "D:\\6-baiduyun\\2-数据\\5-彩票\\七乐彩.xls"
    header_list = ["期号", "日期", "红球1", "红球2", "红球3", "红球4", "红球5", "红球6", "红球7",
                   "蓝球", "本期销量", "一等奖注数", "一等奖单注奖金/元",
                   "二等奖注数", "二等奖单注奖金/元", "三等奖注数", "三等奖单注奖金/元"]
    data_list = session.query(QiLeCai).all()
    data = [item.to_list() for item in data_list]
    df = pandas.DataFrame(data)
    df.to_excel(file_path, index=False, header=header_list)


def main():
    session = Session()
    fail_queue = SimpleQueue()
    params = getParam()
    url_pattern = "https://kaijiang.500.com/shtml/qlc/{}.shtml"
    for param in tqdm(params):
        page = crawl_single_page(url_pattern.format(param))
        time.sleep(0.3)
        if page is not None:
            flag = parse_single_page(param, page, session)
            if not flag:
                fail_queue.put({
                    "param": param,
                    "count": 1
                })
        else:
            fail_queue.put({
                    "param": param,
                    "count": 1
                })
    print("需要重新下载的任务数：" + str(fail_queue.qsize()))
    while not fail_queue.empty():
        item = fail_queue.get()
        if item["count"] > 3:
            continue
        param = item["param"]
        page = crawl_single_page(url_pattern.format(param))
        time.sleep(0.3)
        if page is not None:
            flag = parse_single_page(param, page, session)
            if not flag:
                item["count"] += 1
                fail_queue.put(item)
        else:
            item["count"] += 1
            fail_queue.put(item)
    save_in_file(session)
    session.close()


if __name__ == '__main__':
    main()
