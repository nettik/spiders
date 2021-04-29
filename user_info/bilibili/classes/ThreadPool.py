from queue import Queue
import time

from bilibili.classes.Consumer import Consumer
from bilibili.classes.Producer import Producer


class ThreadPool:

    def __init__(self, consumer_thread_num):
        self.consumer_queue = Queue()
        self.consumer_thread_num = consumer_thread_num
        self.consumer_thread = list()

        self.producer_queue = Queue()
        self.producer_thread = None

    def init_work(self, init_userid):
        self.put_consumer_task(init_userid)
        self.create_thread(init_userid)

    def create_thread(self, init_userid):
        for i in range(self.consumer_thread_num):
            self.consumer_thread.append(Consumer(self))
        self.producer_thread = Producer(self, init_userid)

    def start_thread(self):
        for i in range(self.consumer_thread_num):
            self.consumer_thread[i].start()
        self.producer_thread.start()

    def put_producer_task(self, userid):
        self.producer_queue.put(userid)

    def get_producer_task(self):
        return self.producer_queue.get(block=False)

    def producer_task_done(self):
        self.producer_queue.task_done()

    def put_consumer_task(self, userid):
        self.consumer_queue.put(userid)

    def get_consumer_task(self):
        return self.consumer_queue.get(block=False)

    def consumer_task_done(self):
        self.consumer_queue.task_done()

    def wait_all_task_done(self):
        # while self.consumer_queue.qsize() > 0:
        #     print("\r剩余任务: " + str(self.consumer_queue.qsize()), end='')
        #     time.sleep(5)

        self.consumer_queue.join()
        self.producer_queue.join()
        for i in range(self.consumer_thread_num):
            self.consumer_thread[i].run_flag = False
        for i in range(self.consumer_thread_num):
            self.consumer_thread[i].join()

        self.producer_thread.run_flag = False
        self.producer_thread.join()
