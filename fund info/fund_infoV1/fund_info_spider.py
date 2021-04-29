import requests
from bs4 import BeautifulSoup
import json
import time
from tqdm import tqdm
import fund_infoV1.DatabaseHandler as DatabaseHandler
import fund_infoV1.FundInfo as FundInfo

failure_fund_id = []

count = 0


def get_fund_info_html(url, encoding="utf-8"):
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
    fund_info = FundInfo.FundInfo()
    try:
        # 基金名称
        fund_info.fund_name = \
            html.find('div', attrs={'class': 'gmfund_title_right'}).previous_sibling.previous_sibling.contents[
                1].contents[
                0]
        # print(fund_info.fund_name)

        # 基金编号
        fund_info.fund_id = \
            html.find('div', attrs={'class': 'gmfund_title_right'}).previous_sibling.previous_sibling.contents[
                1].contents[
                1].string.lstrip('(').rstrip(')')
        # print(fund_info.fund_id)

        # 基金类型
        fund_info.fund_type = \
            html.find('div', attrs={'class': 'gmfund_title_right'}).previous_sibling.previous_sibling.contents[
                3].contents[
                1].string
        # print(fund_info.fund_type)

        # 基金标签
        fund_tags_list = html.find('ul', attrs={'class': 'fund_tags'}).contents
        fund_tags = ""
        for tag in fund_tags_list:
            fund_tags = fund_tags + tag.string + "," if tag != "\n" else fund_tags
        fund_info.fund_tags = fund_tags.rstrip(',')
        # print(fund_info.fund_tags)

        # 成立时间
        fund_info.build_time = html.find('div', attrs={'class': 'gmfund_num'}).contents[1].contents[7].contents[
            1].string
        # print(fund_info.build_time)

        # 最新规模
        fund_info.latest_scale = html.find('div', attrs={'class': 'gmfund_num'}).contents[1].contents[5].contents[
            1].string
        # print(fund_info.latest_scale)

        # 收益率
        income = html.find('div', attrs={'id': 'nTab9_0'}).contents[1].contents[1].contents[2].contents
        fund_info.since_this_year_rate = float(income[3].contents[0].string.rstrip('%')) if income[3].contents[
                                                                                                0].string != '--' else 0
        # print(fund_info.since_this_year_rate)
        fund_info.last_one_week_rate = float(income[5].contents[0].string.rstrip('%')) if income[5].contents[
                                                                                              0].string != '--' else 0
        # print(fund_info.last_one_week_rate)
        fund_info.last_one_month_rate = float(income[7].contents[0].string.rstrip('%')) if income[7].contents[
                                                                                               0].string != '--' else 0
        # print(fund_info.last_one_month_rate)
        fund_info.last_three_month_rate = float(income[9].contents[0].string.rstrip('%')) if income[9].contents[
                                                                                                 0].string != '--' else 0
        # print(fund_info.last_three_month_rate)
        fund_info.last_six_month_rate = float(income[11].contents[0].string.rstrip('%')) if income[11].contents[
                                                                                                0].string != '--' else 0
        # print(fund_info.last_six_month_rate)
        fund_info.last_one_year_rate = float(income[13].contents[0].string.rstrip('%')) if income[13].contents[
                                                                                               0].string != '--' else 0
        # print(fund_info.last_one_year_rate)
        fund_info.last_two_year_rate = float(income[15].contents[0].string.rstrip('%')) if income[15].contents[
                                                                                               0].string != '--' else 0
        # print(fund_info.last_two_year_rate)
        fund_info.last_three_year_rate = float(income[17].contents[0].string.rstrip('%')) if income[17].contents[
                                                                                                 0].string != '--' else 0
        # print(fund_info.last_three_year_rate)

        # 基金经理姓名
        fund_info.manager_name = html.find('ul', attrs={'class': 'item_4'}).contents[1].contents[1].string
        # print(fund_info.manager_name)

        # 基金经理工作年限
        fund_info.manager_work_time = \
            html.find('ul', attrs={'class': 'item_4'}).contents[9].contents[0].string.split('：')[
                1]
        # print(fund_info.manager_work_time)

        # 从业年均汇报
        fund_info.average_income_rate_per_work_year = float(
            html.find('ul', attrs={'class': 'item_2'}).contents[1].contents[3].contents[0].string.rstrip('%'))
        # print(fund_info.average_income_rate_per_work_year)

        # 最大盈利
        fund_info.max_increase_rate = float(
            html.find('ul', attrs={'class': 'item_2'}).contents[3].contents[3].contents[0].string.rstrip('%'))
        # print(fund_info.max_increase_rate)

        # 最大回撤
        fund_info.max_decrease_rate = float(
            html.find('ul', attrs={'class': 'item_2'}).contents[5].contents[3].contents[0].string.rstrip('%'))
        # print(fund_info.max_decrease_rate)

        save_in_database(db_handler, fund_info)
    except:
        failure_fund_id.append(fund_info.fund_id)
        print("error: " + fund_info.fund_id + " parse failure")


def save_in_database(db_handler, fund_info_object):
    sql_clause = "insert into fund_info values" + "(" + fund_info_object.to_insert_sql() + ")"
    # print(sql_clause)
    try:
        db_handler.cursor.execute(sql_clause)
        db_handler.conn.commit()
    except:
        failure_fund_id.append(fund_info_object.fund_id)
        print("error: " + fund_info_object.fund_id + " insert failure")


def get_fund_id_html(url, page, encoding="utf-8"):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }
    try:
        r = requests.post(url, headers=headers, data={'page': page, 'cat': 'index.htm'}, timeout=1)
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


def main():
    db_handler = DatabaseHandler.DatabaseHandler('localhost', 'root', 'root', 'fundinfodb')
    db_handler.create_connection()
    db_handler.cursor.execute("delete from fund_info")
    db_handler.conn.commit()
    root_url = "https://www.howbuy.com/fund/fundranking/ajax.htm"
    pages = 192
    ids = get_fund_info_id(root_url, pages)
    for fund_id_index in tqdm(range(len(ids))):
        url = "https://www.howbuy.com/fund/" + ids[fund_id_index]
        raw_html = get_fund_info_html(url)
        if raw_html != "":
            html = BeautifulSoup(raw_html, "html5lib")
            parse_single_html(html, db_handler)
        else:
            pass
        time.sleep(0.5)
    print("failure: " + str(len(failure_fund_id)))


if __name__ == "__main__":
    main()
