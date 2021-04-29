from tqdm import tqdm
import requests
from requests.exceptions import ConnectTimeout
import json
import time
import fund_infoV2.classes.ThreadPool as ThreadPool
import fund_infoV2.classes.DatabaseHandler as DatabaseHandler
from datetime import datetime
import pandas



def get_fund_id_html(url, page, encoding="utf-8"):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }
    try:
        r = requests.post(url, headers=headers, data={'page': page, 'cat': 'index.htm'}, timeout=1)
        r.raise_for_status()
        r.encoding = encoding
        return r.text
    except ConnectTimeout:
        return ""
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


def save_in_file(db_handler):
    file_path = "D:\\6-baiduyun\\2-数据\\0-基金\\基金数据_{}.xls".format(datetime.now().strftime("%Y%m%d"))
    db_handler.cursor.execute(
        '''
        select fund_id,fund_name,fund_type,fund_tags,build_time,latest_scale,
        since_this_year_rate,last_one_week_rate,last_one_month_rate,
        last_three_month_rate,last_six_month_rate,last_one_year_rate,
        last_two_year_rate,last_three_year_rate from fund_info
        '''
    )
    data = db_handler.cursor.fetchall()
    data_f = pandas.DataFrame(data)
    headers = ['基金编号', '基金名称', '基金类型',
               '基金标签', '成立时间', '基金规模',
               '今年以来收益率', '最近一周收益率',
               '最近一个月收益率', '最近三个月收益率', '最近六个月收益率',
               '最近一年收益率', '最近两年收益率', '最近三年收益率']
    data_f.to_excel(file_path, index=False, header=headers, encoding='utf-8')


def main():
    db_handler = DatabaseHandler.DatabaseHandler('localhost', 'root', 'root', 'fundinfodb')
    db_handler.create_connection()
    db_handler.cursor.execute("delete from fund_info")
    db_handler.conn.commit()

    thread_pool = ThreadPool.ThreadPool(download_thread_num=3, parse_thread_num=4, save_thread_num=2)
    thread_pool.create_thread()
    thread_pool.start_thread()

    root_url = "https://www.howbuy.com/fund/fundranking/ajax.htm"
    pages = 192
    ids = get_fund_info_id(root_url, pages)
    start = time.time()
    for fund_id_index in list(range(len(ids))):
        url = "https://www.howbuy.com/fund/" + ids[fund_id_index]
        thread_pool.put_download_task(url)

    thread_pool.wait_all_task_done()
    end = time.time()
    print(end - start)
    save_in_file(db_handler)


def test():
    url = "http://fund.eastmoney.com/005968.html"
    r = requests.get(url)
    r.encoding = "utf-8"
    with open("a.html","w",encoding="utf-8") as f:
        f.write(r.text)


if __name__ == "__main__":
    test()
