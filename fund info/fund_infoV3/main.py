import time
import requests
from tqdm import tqdm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas
from datetime import datetime
import json
from fund_infoV3.classes.ThreadPool import ThreadPool
from fund_infoV3.classes.FundInfo import FundInfo


def get_fund_id_html(url, page, encoding="utf-8"):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }
    try:
        r = requests.post(url, headers=headers, data={'page': page, 'cat': 'index.htm'}, timeout=6)
        r.raise_for_status()
        r.encoding = encoding
        return r.text
    except:
        return ""


def get_fund_info_id(root_url, pages):
    fund_ids = []
    for page in tqdm(range(1, pages)):
        result = get_fund_id_html(root_url, page)
        if result != "":
            list_result = json.loads(result)['list']
            for index in list(range(len(list_result))):
                fund_ids.append(list_result[index]['jjdm'])
        time.sleep(1)
    return fund_ids


def delete_all_data():
    connectStr = "mysql+pymysql://root:root@localhost:3306/fundinfodb"
    engine = create_engine(connectStr)
    engine.execute("delete from fund_info_new")


def save_in_file():
    connectStr = "mysql+pymysql://root:root@localhost:3306/fundinfodb"
    engine = create_engine(connectStr)
    session = sessionmaker(bind=engine)
    sess = session()
    res = [item.to_list() for item in sess.query(FundInfo).all()]
    df = pandas.DataFrame(res)
    file_path = "D:\\6-baiduyun\\2-数据\\0-基金\\基金数据_{}.xls".format(datetime.now().strftime("%Y%m%d"))
    headers = ['基金编号', '基金名称', '基金类型',
               '基金标签', '成立时间', '基金规模',
               '今年以来收益率', '最近一周收益率',
               '最近一个月收益率', '最近三个月收益率', '最近六个月收益率',
               '最近一年收益率', '最近两年收益率', '最近三年收益率', '一年夏普率',
               '两年夏普率', '三年夏普率', '持股持债比例', '资产配置', '行业配置']
    df.to_excel(file_path, index=False, header=headers, encoding="utf-8")
    sess.close()


def main():
    start = time.time()
    delete_all_data()
    thread_pool = ThreadPool(thread_num=8)
    root_url = "https://www.howbuy.com/fund/fundranking/ajax.htm"
    pages = 192
    ids = get_fund_info_id(root_url, pages)
    for fund_id in ids:
        thread_pool.put_task(fund_id)
    thread_pool.create_and_start_thread()
    thread_pool.wait_all_task_done()
    save_in_file()
    end = time.time()
    print("\r" + str(round((end - start) / 60, 1)) + "分钟")


if __name__ == '__main__':
    main()
