from threading import Thread
import requests
from queue import Empty
import json
import time
import traceback
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fund_infoV3.classes.Tool import Tool
from fund_infoV3.classes.FundInfo import FundInfo


class WorkThread(Thread):
    connectStr = "mysql+pymysql://root:root@localhost:3306/fundinfodb"
    engine = create_engine(connectStr, max_overflow=5)
    session = sessionmaker(bind=engine)

    def __init__(self, thread_pool):
        Thread.__init__(self)
        self.thread_pool = thread_pool
        self._run_flag = True
        self.sess = WorkThread.session()

    def __del__(self):
        self.sess.close()

    @property
    def run_flag(self):
        return self._run_flag

    @run_flag.setter
    def run_flag(self, run_flag):
        self._run_flag = run_flag

    def get_html(self, fundid):
        try:
            url = Tool.html_url_pattern.format(fundid)
            r = requests.get(url, headers=Tool.html_header, timeout=6)
            r.raise_for_status()
            r.encoding = "utf-8"
            return r.text
        except:
            traceback.print_exc()
            return ""

    def get_js(self, fundid):
        try:
            url = Tool.js_url_pattern.format(fundid, fundid, fundid)
            r = requests.get(url, headers=Tool.js_header, timeout=6)
            r.raise_for_status()
            r.encoding = "utf-8"
            return r.text
        except:
            traceback.print_exc()
            return ""

    def parse_js(self, js, fund_info):
        try:
            zcpz_t = Tool.zcpz_pattern.findall(js)
            if len(zcpz_t) > 0:
                zcpz_dict = json.loads(Tool.replace_zcpz(zcpz_t[0]))
                zcpz_list = zcpz_dict[zcpz_dict["lastDate"]]
                zcpz_str = zcpz_dict["lastDate"] + ":"
                for item in zcpz_list:
                    zcpz_str = zcpz_str + (item["name"] + "," + str(round(item["y"], 2))) + ";"
                fund_info.zcpz = zcpz_str.rstrip(";")

            hypz_t = Tool.hypz_pattern.findall(js)
            if len(hypz_t) > 0:
                hypz_dict = json.loads(Tool.replace_hypz(hypz_t[0]))
                hypz_list = hypz_dict[hypz_dict["lastDate"]]["data"]
                hypz_str = hypz_dict["lastDate"] + ":"
                for item in hypz_list:
                    hypz_str = hypz_str + (item["name"] + "," + str(round(item["y"], 2))) + ";"
                fund_info.hypz = hypz_str.rstrip(";")

            cgczbl_t = Tool.cgczbl_pattern.findall(js)
            if len(cgczbl_t) > 0 and fund_info.jjlx in ["指数型", "QDII", "混合型", "股票型"]:
                cgczbl_dict = json.loads(Tool.replace_cgczbl_stock(cgczbl_t[0]))
                cgcz_list = cgczbl_dict[cgczbl_dict["lastDate"]]
                cgcz_str = cgczbl_dict["lastDate"] + ":"
                if len(cgcz_list) > 10:
                    for item in cgcz_list[0:10]:
                        cgcz_str = cgcz_str + (item["zqmc"] + "," + item["zqdm"] + "," + str(item["zjbl"])) + ";"
                else:
                    for item in cgcz_list:
                        cgcz_str = cgcz_str + (item["zqmc"] + "," + item["zqdm"] + "," + str(item["zjbl"])) + ";"
                fund_info.cgczbl = cgcz_str.rstrip(";")
            elif len(cgczbl_t) > 0 and fund_info.jjlx == "债券型":
                cgczbl_dict = json.loads(Tool.replace_cgczbl_bond(cgczbl_t[0]))
                cgcz_list = cgczbl_dict[cgczbl_dict["lastDate"]]
                cgcz_str = cgczbl_dict["lastDate"] + ":"
                if len(cgcz_list) > 10:
                    for item in cgcz_list[0:10]:
                        cgcz_str = cgcz_str + (item["zqmc"] + "," + item["zqdm"] + "," + str(item["zjbl"])) + ";"
                else:
                    for item in cgcz_list:
                        cgcz_str = cgcz_str + (item["zqmc"] + "," + item["zqdm"] + "," + str(item["zjbl"])) + ";"
                fund_info.cgczbl = cgcz_str.rstrip(";")
            return fund_info
        except:
            return fund_info

    def parse_html(self, html=""):
        try:
            fund_info = FundInfo()
            name_list = Tool.name_pattern.findall(html)
            if len(name_list) > 0:
                fund_info.jjmc = name_list[0]

            id_list = Tool.id_pattern.findall(html)
            if len(id_list) > 0:
                fund_info.jjbh = id_list[0]

            type_list = Tool.type_pattern.findall(html)
            if len(type_list) > 0:
                fund_info.jjlx = type_list[0]

            tag_list = Tool.tag_str_pattern.findall(html)
            if len(tag_list) > 0:
                tags = Tool.tag_pattern.findall(tag_list[0])
                tag_str = ""
                for tag in tags:
                    tag_str = tag_str + tag + ","
                fund_info.jjbq = tag_str.rstrip(',')

            build_time_list = Tool.build_time_pattern.findall(html)
            if len(build_time_list) > 0:
                fund_info.clsj = build_time_list[0]

            latest_scale_list = Tool.latest_scale_pattern.findall(html)
            if len(latest_scale_list) > 0:
                fund_info.jjgm = latest_scale_list[0]

            income_list = Tool.income_str_pattern.findall(html)
            if len(income_list) > 0:
                incomes = Tool.income_pattern.findall(income_list[0])
                if len(incomes) > 0:
                    fund_info.jnsyl = float(Tool.income_rate_pattern.findall(incomes[0])[0].rstrip('%')) if incomes[0] != "--" else 0
                    fund_info.yzsyl = float(Tool.income_rate_pattern.findall(incomes[1])[0].rstrip('%')) if incomes[1] != "--" else 0
                    fund_info.yysyl = float(Tool.income_rate_pattern.findall(incomes[2])[0].rstrip('%')) if incomes[2] != "--" else 0
                    fund_info.sysyl = float(Tool.income_rate_pattern.findall(incomes[3])[0].rstrip('%')) if incomes[3] != "--" else 0
                    fund_info.lysyl = float(Tool.income_rate_pattern.findall(incomes[4])[0].rstrip('%')) if incomes[4] != "--" else 0
                    fund_info.ynsyl = float(Tool.income_rate_pattern.findall(incomes[5])[0].rstrip('%')) if incomes[5] != "--" else 0
                    fund_info.lnsyl = float(Tool.income_rate_pattern.findall(incomes[6])[0].rstrip('%')) if incomes[6] != "--" else 0
                    fund_info.snsyl = float(Tool.income_rate_pattern.findall(incomes[7])[0].rstrip('%')) if incomes[7] != "--" else 0

            sharp_rate_list = Tool.sharp_rate_str_pattern.findall(html)
            if len(sharp_rate_list) > 0:
                sharp_rates = Tool.sharp_rate_pattern.findall(sharp_rate_list[0])
                if len(sharp_rates) > 0:
                    fund_info.ynxpl = float(sharp_rates[0]) if sharp_rates[0] != "--" else 0
                    fund_info.lnxpl = float(sharp_rates[1]) if sharp_rates[1] != "--" else 0
                    fund_info.snxpl = float(sharp_rates[2]) if sharp_rates[2] != "--" else 0
            return fund_info
        except:
            traceback.print_exc()
            return None

    def run(self):
        while self._run_flag:
            try:
                fundid = self.thread_pool.get_task()
                html = self.get_html(fundid)
                time.sleep(1)
                if html != "":
                    fund_info_html = self.parse_html(html)
                    if fund_info_html is not None:
                        if fund_info_html.jjlx not in ["指数型", "QDII", "混合型", "股票型", "债券型"]:
                            try:
                                self.sess.add(fund_info_html)
                                self.sess.commit()
                            except:
                                self.sess.rollback()
                                traceback.print_exc()
                        else:
                            js = self.get_js(fundid)
                            time.sleep(1)
                            if js != "":
                                fund_info_js = self.parse_js(js, fund_info_html)
                                try:
                                    self.sess.add(fund_info_js)
                                    self.sess.commit()
                                except:
                                    self.sess.rollback()
                                    traceback.print_exc()
                self.thread_pool.task_done()
            except Empty:
                pass
            except:
                self.thread_pool.task_done()
