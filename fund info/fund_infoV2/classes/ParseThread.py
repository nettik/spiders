import threading
from bs4 import BeautifulSoup
import queue
import fund_infoV2.classes.FundInfo as FundInfo



class ParseThread(threading.Thread):
    def __init__(self, thread_pool, run_flag):
        threading.Thread.__init__(self)
        self.thread_pool = thread_pool
        self.run_flag = run_flag

    def set_run_flag(self, run_flag):
        self.run_flag = run_flag

    def parse_single_html(self,html):
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

            return fund_info
        except:
            pass

    def run(self):
        while self.run_flag:
            try:
                raw_html = self.thread_pool.get_parse_task()
                html = BeautifulSoup(raw_html, "html5lib")
                fund_info = self.parse_single_html(html)
                sql = "insert into fund_info values" + "(" + fund_info.to_insert_sql() + ")"
                self.thread_pool.put_save_task(sql)
                self.thread_pool.parse_task_done()
            except queue.Empty:
                pass
            except:
                self.thread_pool.parse_task_done()
