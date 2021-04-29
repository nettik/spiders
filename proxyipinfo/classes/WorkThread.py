import requests
from threading import Thread
import queue
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class WorkThread(Thread):

    def __init__(self, thread_pool, run_flag):
        Thread.__init__(self)
        self.thread_pool = thread_pool
        self.run_flag = run_flag
        self.connectStr = "mysql+pymysql://root:root@localhost:3306/utildb"
        self.engine = create_engine(self.connectStr)
        self.session = sessionmaker(bind=self.engine)()

    def set_run_flag(self, flag):
        self.run_flag = flag

    def check_ip(self, ip, port):
        url = "https://ip.cn/api/index?ip=&type=0"
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
            'referer': "https://ip.cn/",
            'accept-language': "zh-CN,zh;q=0.9",
            'accept': "application/json, text/javascript, */*; q=0.01"
        }
        proxy = {
            'https': "http://{}:{}".format(ip, port)
        }
        try:
            r = requests.get(url, headers=header, proxies=proxy, timeout=3)
            r.raise_for_status()
            req_ip = r.json()["ip"]
            if req_ip == ip:
                return 0
            return -1
        except:
            return -1

    def run(self):
        while self.run_flag:
            try:
                ip_info = self.thread_pool.get_task()
                ret = self.check_ip(ip_info.ip, ip_info.port)
                if ret == 0:
                    try:
                        self.session.add(ip_info)
                        self.session.commit()
                    except:
                        self.session.rollback()
                self.thread_pool.task_done()
            except queue.Empty:
                pass
            except:
                self.thread_pool.task_done()
