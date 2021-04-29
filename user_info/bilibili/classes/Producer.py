from threading import Thread
import requests
from bilibili.tool import load_cookie
from bilibili.crawl_user_id import crawl_id
import time
from queue import Empty
from bilibili.classes.Filter import Filter


class Producer(Thread):
    cookies = load_cookie()

    def __init__(self, thread_pool, init_userid):
        Thread.__init__(self)
        self.thread_pool = thread_pool
        self._run_flag = True
        self.filter = Filter()
        self.filter.add_in_filter(init_userid)
        self.web_session = requests.session()
        for cookie in Producer.cookies:
            self.web_session.cookies.set(cookie["name"], cookie["value"])

    @property
    def run_flag(self):
        return self._run_flag

    @run_flag.setter
    def run_flag(self, flag):
        self._run_flag = flag

    def run(self):
        while self._run_flag:
            try:
                userid = self.thread_pool.get_producer_task()
                id_list = crawl_id(self.web_session, userid)
                for id_t in id_list:
                    if not self.filter.is_id_in_filter(id_t):
                        self.filter.add_in_filter(id_t)
                        self.thread_pool.put_consumer_task(id_t)
                time.sleep(1)
                self.thread_pool.producer_task_done()
            except Empty:
                pass
            except:
                self.thread_pool.producer_task_done()
