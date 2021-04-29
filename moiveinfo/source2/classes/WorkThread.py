import re
import time
import traceback
from queue import Empty
from threading import Thread

import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from source2.classes.MoiveInfo import MoiveInfo


class WorkThread(Thread):
    connectStr = "mysql+pymysql://root:root@localhost:3306/moiveinfodb"
    engine = create_engine(connectStr, max_overflow=5)
    session = sessionmaker(bind=engine)
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "max-age=0"
    }
    root_url = "https://www.imdb.cn"

    name_pattern = re.compile('<h1>.*?<div>(.*?)</div>', re.S)
    director_pattern = re.compile('<a.*?>(.*?)</a>', re.S)
    editor_pattern = re.compile('<a.*?>(.*?)</a>', re.S)
    leading_role_pattern = re.compile('<a.*?>(.*?)</a>', re.S)
    moive_type_pattern = re.compile('<div class="txt_bottom_r">(.*?)</div>', re.S)
    region_pattern = re.compile('<div class="txt_bottom_r">(.*?)</div>', re.S)
    language_pattern = re.compile('<div class="txt_bottom_r">(.*?)</div>', re.S)
    date_pattern = re.compile('<div class="txt_bottom_r">.*?(\d{4}-\d{2}-\d{2}).*?</div>', re.S)
    duration_pattern = re.compile('<div class="txt_bottom_r">(.*?)</div>', re.S)

    # table_pattern = re.compile('<tbody id="movieBoxoffice">(.*?)</tbody>', re.S)
    # box_office = re.compile('<td>全球累计票房</td')

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

    def get_html(self, suffix):
        url = "".join([WorkThread.root_url, suffix])
        try:
            r = requests.get(url, headers=WorkThread.header, timeout=6)
            r.raise_for_status()
            r.encoding = "utf-8"
            return r.text
        except:
            traceback.print_exc()
            return None

    def get_box_office(self, suffix):
        url = "".join([WorkThread.root_url, suffix, "/", "boxoffice"])
        try:
            r = requests.get(url, headers=WorkThread.header, timeout=6)
            r.raise_for_status()
            r.encoding = 'utf-8'
            html = r.text
            if "暂无收录内容 , 期待你的添加" in html:
                return "--"
            else:
                box_office_soup = BeautifulSoup(html, 'html5lib')
                box_office_tag_list = box_office_soup.select("#movieBoxoffice > tr:nth-child(4) > td:nth-child(2)")
                if len(box_office_tag_list) > 0:
                    return box_office_tag_list[0].text
                return "--"
        except:
            traceback.print_exc()
            return "-1"

    def parse_html(self, html):
        try:
            soup = BeautifulSoup(html, 'html5lib')
            info = soup.find('div', attrs={'class': 'per_txt'}).prettify()
            if info is not None:
                lines_soup = BeautifulSoup(info, 'html5lib')
                lines = lines_soup.find_all('div', attrs={'class': "txt_bottom_item"})
                name = re.search(WorkThread.name_pattern, info).group(1)
                moive_info = MoiveInfo()
                moive_info.set_name(name)
                for line in lines:
                    line_html = line.prettify()
                    if "导演" in line_html:
                        director = re.search(WorkThread.director_pattern, line_html)
                        if director is not None:
                            moive_info.set_director(director.group(1))
                    elif "编剧" in line_html:
                        editor = WorkThread.editor_pattern.findall(line_html)
                        moive_info.set_editor(editor)
                    elif "主演" in line_html:
                        leading_role = WorkThread.leading_role_pattern.findall(line_html)
                        moive_info.set_leading_role(leading_role)
                    elif "类型" in line_html:
                        moive_type = re.search(WorkThread.moive_type_pattern, line_html)
                        if moive_type is not None:
                            moive_info.set_moive_type(moive_type.group(1))
                    elif "制片国家/地区" in line_html:
                        region = re.search(WorkThread.region_pattern, line_html)
                        if region is not None:
                            moive_info.set_region(region.group(1))
                    elif "语言" in line_html:
                        language = re.search(WorkThread.language_pattern, line_html)
                        if language is not None:
                            moive_info.set_language(language.group(1))
                    elif "片长" in line_html:
                        duration = re.search(WorkThread.duration_pattern, line_html)
                        if duration is not None:
                            moive_info.set_duraton(duration.group(1))
                    elif "上映日期" in line_html:
                        date = re.search(WorkThread.date_pattern, line_html)
                        if date is not None:
                            moive_info.set_date(date.group(1))
                return moive_info
            return None
        except:
            traceback.print_exc()
            return None

    def run(self):
        while self._run_flag:
            try:
                suffix = self.thread_pool.get_task()
                html = self.get_html(suffix)
                time.sleep(1)
                if html is not None:
                    moive_info = self.parse_html(html)
                    if moive_info is not None:
                        moive_info.set_box_office(self.get_box_office(suffix))
                        try:
                            self.sess.add(moive_info)
                            self.sess.commit()
                        except:
                            self.sess.rollback()
                            traceback.print_exc()
                self.thread_pool.task_done()
            except Empty:
                pass
            except:
                self.thread_pool.task_done()
