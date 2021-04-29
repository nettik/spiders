import requests
import cchardet
import re
from tqdm import tqdm
from queue import SimpleQueue
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from chaojidaletou.classes.DaLeTou import DaLeTou
import time
import pandas

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
    root_url = "https://kaijiang.500.com/dlt.shtml"
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
red_pattern = re.compile('<li class="ball_red">(\d{2})</li>')
blue_pattern = re.compile('<li class="ball_blue">(\d{2})</li>')
sale_and_pool_pattern = re.compile('<span class="cfont1">(.*?)</span>', re.S)


def parse_single_page(param, page, session):
    da_le_tou = DaLeTou(param)
    date_t = date_pattern.findall(page)
    if len(date_t) > 0:
        da_le_tou.date = date_t[0].split('：')[-1]
    red_t = red_pattern.findall(page)
    if len(red_t) > 0:
        da_le_tou.red1 = red_t[0]
        da_le_tou.red2 = red_t[1]
        da_le_tou.red3 = red_t[2]
        da_le_tou.red4 = red_t[3]
        da_le_tou.red5 = red_t[4]
    blue_t = blue_pattern.findall(page)
    if len(blue_t) > 0:
        da_le_tou.blue1 = blue_t[0]
        da_le_tou.blue2 = blue_t[1]
    sale_and_pool_t = sale_and_pool_pattern.findall(page)
    if len(sale_and_pool_t) > 0:
        da_le_tou.sale_money = sale_and_pool_t[0]
        da_le_tou.pool_money = sale_and_pool_t[1]
    try:
        session.add(da_le_tou)
        session.commit()
        return True
    except:
        session.rollback()
        return False


def save_in_file(session):
    file_path = "D:\\6-baiduyun\\2-数据\\5-彩票\\超级大乐透.xls"
    header_list = ["期号", "日期", "红球1", "红球2", "红球3", "红球4", "红球5", "蓝球1",
                   "蓝球2", "本期销量", "奖池滚存"]
    data_list = session.query(DaLeTou).all()
    data = [item.to_list() for item in data_list]
    df = pandas.DataFrame(data)
    df.to_excel(file_path, index=False, header=header_list)


def main():
    session = Session()
    fail_queue = SimpleQueue()
    params = getParam()
    url_pattern = "https://kaijiang.500.com/shtml/dlt/{}.shtml"
    for param in tqdm(params):
        page = crawl_single_page(url_pattern.format(param))
        time.sleep(0.5)
        if page is not None:
            flag = parse_single_page(param, page, session)
            if not flag:
                fail_queue.put(param)
        else:
            fail_queue.put(param)
    print("需要重新下载的任务数：" + str(fail_queue.qsize()))
    while not fail_queue.empty():
        param = fail_queue.get()
        page = crawl_single_page(url_pattern.format(param))
        time.sleep(0.5)
        if page is not None:
            flag = parse_single_page(param, page, session)
            if not flag:
                fail_queue.put(param)
        else:
            fail_queue.put(param)
    save_in_file(session)
    session.close()


if __name__ == '__main__':
    main()
