import requests
from bs4 import BeautifulSoup
import json
import time
from tqdm import tqdm
import fund_infoV1.DatabaseHandler as DatabaseHandler
import fund_infoV1.FundManager as FundManager


def get_fund_manager_html(url, encoding="utf-8"):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }
    try:
        r = requests.get(url, headers=headers, timeout=1)
        r.raise_for_status()
        r.encoding = encoding
        return r.text
    except:
        return ""


def parse_single_html(html, db_handler):
    try:
        company = html.find('li', attrs={'class': 'score_fat'}).next_sibling.next_sibling.string.strip(' ').split(':')[
            -1].strip(' ')
        if company == "已离任":
            return
    except:
        pass

    fund_manager = FundManager.FundManager()
    try:
        fund_manager.average_income_rate_per_work_year = \
            float(html.find('div', attrs={'class': 'content_des_main'}).previous_sibling.previous_sibling.contents[
                      1].contents[4].contents[7].contents[0].string.rstrip('%'))
        # print(fund_manager.average_income_rate_per_work_year)
    except:
        pass

    try:
        fund_manager.manager_work_time = \
            html.find('div', attrs={'class': 'content_des_main'}).previous_sibling.previous_sibling.contents[
                1].contents[0].contents[7].string
        # print(fund_manager.manager_work_time)
    except:
        pass

    try:
        fund_manager.max_increase_rate = float(
            html.find_all('div', attrs={'class': 'top_right'})[0].contents[1].string.rstrip('%'))
        # print(fund_manager.max_increase_rate)

        fund_manager.max_decrease_rate = float(
            html.find_all('div', attrs={'class': 'top_right'})[1].contents[1].string.rstrip('%'))
        # print(fund_manager.max_decrease_rate)
    except:
        pass

    try:
        fund_manager.manager_name = html.find('div', attrs={'class': 'manager_name'}).string
        # print(fund_manager.manager_name)
        save_in_database(db_handler, fund_manager)
    except:
        print("error: " + fund_manager.manager_name + " parse failure")


def save_in_database(db_handler, fund_manager_object):
    sql_clause = "insert into fund_manager values" + "(" + fund_manager_object.to_insert_sql() + ")"
    try:
        db_handler.cursor.execute(sql_clause)
        db_handler.conn.commit()
    except:
        print("error: " + fund_manager_object.manager_name + " insert failure")


def get_fund__manager_id_html(url, page, encoding="utf-8"):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }
    try:
        r = requests.post(url, headers=headers, data={'page': page, 'orderField': 'rqzs', 'orderType': 'true'},
                          timeout=1)
        r.raise_for_status()
        r.encoding = encoding
        return r.text
    except:
        return ""


def get_fund_manager_id(root_url, pages):
    fund_manager_ids = []
    for page in tqdm(range(1, pages)):
        result = get_fund__manager_id_html(root_url, page)
        if result != "":
            list_result = json.loads(result)['list']
            for index in list(range(len(list_result))):
                fund_manager_ids.append(list_result[index]['rydm'])
        time.sleep(0.5)
    return fund_manager_ids


def main():
    db_handler = DatabaseHandler.DatabaseHandler('localhost', 'root', 'root', 'fundinfodb')
    db_handler.create_connection()
    db_handler.cursor.execute("delete from fund_manager")
    db_handler.conn.commit()
    root_url = "https://www.howbuy.com/fund/manager/ajax.htm"
    pages = 80
    ids = get_fund_manager_id(root_url, pages)
    for id_index in tqdm(range(len(ids))):
        url = "https://www.howbuy.com/fund/manager/" + ids[id_index]
        raw_html = get_fund_manager_html(url)
        if raw_html != "":
            html = BeautifulSoup(raw_html, "html5lib")
            parse_single_html(html, db_handler)
        else:
            pass
        time.sleep(0.5)


if __name__ == "__main__":
    main()
