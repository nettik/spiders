import time
import traceback
from queue import Empty
from threading import Thread

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from bilibili.classes.BUserInfo import BUserInfo
from bilibili.crawl_user_info import get_user_info
from bilibili.tool import load_cookie


class Consumer(Thread):
    connectStr = "mysql+pymysql://root:root@localhost:3306/userinfodb"
    engine = create_engine(connectStr, max_overflow=5)
    session = sessionmaker(bind=engine)
    cookies = load_cookie()

    def __init__(self, thread_pool):
        Thread.__init__(self)
        self.thread_pool = thread_pool
        self._run_flag = True
        self.sess = Consumer.session()
        self.web_session = requests.session()
        for cookie in Consumer.cookies:
            self.web_session.cookies.set(cookie["name"], cookie["value"])

    def __del__(self):
        self.sess.close()
        self.web_session.close()

    @property
    def run_flag(self):
        return self._run_flag

    @run_flag.setter
    def run_flag(self, run_flag):
        self._run_flag = run_flag

    def run(self):
        while self._run_flag:
            try:
                userid = self.thread_pool.get_consumer_task()
                self.thread_pool.put_producer_task(userid)
                user_info = BUserInfo()
                flag = get_user_info(self.web_session, user_info, userid)
                if flag:
                    try:
                        self.sess.add(user_info)
                        self.sess.commit()
                    except:
                        self.sess.rollback()
                        traceback.print_exc()
                time.sleep(1)
                self.thread_pool.consumer_task_done()
            except Empty:
                pass
            except:
                self.thread_pool.consumer_task_done()
                traceback.print_exc()
