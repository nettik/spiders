from queue import Empty
from threading import Thread

import cchardet
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from qimaowang.classes.NovelInfo import NovelInfo
from qimaowang.classes.Tool import Tool


class WorkThread(Thread):
    connectStr = "mysql+pymysql://root:root@localhost:3306/noveldb"
    engine = create_engine(connectStr, max_overflow=5)
    session_db = sessionmaker(bind=engine)

    def __init__(self, thread_pool, cookies):
        Thread.__init__(self)
        self.thread_pool = thread_pool
        self._run_flag = True
        self.sess = WorkThread.session_db()
        self.web_sess = self.init_web_session(cookies)

    def __del__(self):
        self.sess.close()
        self.web_sess.close()

    @property
    def run_flag(self):
        return self._run_flag

    @run_flag.setter
    def run_flag(self, run_flag):
        self._run_flag = run_flag

    def run(self):
        while self._run_flag:
            try:
                id_t = self.thread_pool.get_task()
                novel_info = self.single_novel_data(id_t)
                if novel_info is not None:
                    try:
                        self.sess.add(novel_info)
                        self.sess.commit()
                    except:
                        self.sess.rollback()
                self.thread_pool.task_done()
            except Empty:
                pass
            except:
                self.thread_pool.task_done()

    def init_web_session(self, cookies):
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

    def single_novel_data(self, novel_id):
        url = "https://www.qimao.com/shuku/{}/".format(novel_id)
        html = self.crawl(url)
        if html != "":
            data = Tool.novel_data_pattern.findall(html)
            if len(data) > 0:
                novel_data = data[0]
                book_name_t = Tool.book_name_pattern.findall(novel_data)
                author_t = Tool.author_pattern.findall(novel_data)
                if len(book_name_t) > 0 and len(author_t) > 0:
                    novel_info = NovelInfo(book_name_t[0], author_t[0])
                    self.set_novel_info(novel_info, novel_data, html)
                    return novel_info
        return None

    def crawl(self, url):
        try:
            r = self.web_sess.get(url, timeout=12)
            r.raise_for_status()
            encoding = cchardet.detect(r.content)
            r.encoding = encoding["encoding"]
            return r.text
        except Exception as e:
            print(e)
            return ""

    def set_novel_info(self, novel_info, novel_data, html):
        rank_t = Tool.rank_pattern.findall(novel_data)
        if len(rank_t) > 0:
            novel_info.rank = rank_t[0]
        state_t = Tool.state_pattern.findall(novel_data)
        if len(state_t) > 0:
            novel_info.state = state_t[0][1]
        book_type_t = Tool.book_type_pattern.findall(novel_data)
        if len(book_type_t) > 0:
            novel_info.book_type = ",".join(book_type_t)
        leading_role_t = Tool.leading_role_pattern.findall(novel_data)
        if len(leading_role_t) > 0:
            novel_info.leading_role = ",".join(leading_role_t[0].replace("&nbsp;&nbsp;&nbsp;", ",").split(",")[0:-1])
        span_t = Tool.span_pattern.findall(novel_data)
        if len(span_t) > 0:
            novel_info.scale = "".join(span_t[0])
            novel_info.reading_num = ("".join(span_t[1])).rstrip("阅读")
            novel_info.popularity = ("".join(span_t[2])).rstrip("人气值")
        introduction_t = Tool.introduction_pattern.findall(html)
        if len(introduction_t) > 0:
            novel_info.introduction = introduction_t[0].replace("\n", "").strip(" ")
