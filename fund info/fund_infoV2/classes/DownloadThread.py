import threading
import requests
import queue
import time
import random


class DownloadThread(threading.Thread):
    def __init__(self, thread_pool, flag):
        threading.Thread.__init__(self)
        self.thread_pool = thread_pool
        self.run_flag = flag

    def set_run_flag(self, run_flag):
        self.run_flag = run_flag

    def get_fund_info_html(self, url, encoding="utf-8"):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
            'Accept-Languagnet e': "zh-CN,zh;q=0.9",
            'Referer': 'https://www.howbuy.com/fund/trade/',
            'Host': 'www.howbuy.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        }
        try:
            r = requests.get(url, headers=headers, timeout=1)
            r.raise_for_status()
            r.encoding = encoding
            return r.text
        except:
            return ""

    def run(self):
        while self.run_flag:
            try:
                url = self.thread_pool.get_download_task()
                # time.sleep(0.5)
                raw_html = self.get_fund_info_html(url)
                if raw_html != "":
                    self.thread_pool.put_parse_task(raw_html)
                self.thread_pool.download_task_done()
            except queue.Empty:
                pass
            except:
                self.thread_pool.download_task_done()
