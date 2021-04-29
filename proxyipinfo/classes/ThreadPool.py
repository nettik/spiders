from queue import Queue
import time
from classes.WorkThread import WorkThread


class ThreadPool:
    def __init__(self, work_thread_num):
        self.work_thread_num = work_thread_num
        self.work_thread = list()
        self.task_queue = Queue()
        self.run_flag = True

    def create_thread(self):
        for i in range(self.work_thread_num):
            self.work_thread.append(WorkThread(self, self.run_flag))

    def start_thread(self):
        for i in range(self.work_thread_num):
            self.work_thread[i].start()

    def put_task(self, ip_info):
        self.task_queue.put(ip_info)

    def get_task(self):
        return self.task_queue.get(block=False)

    def task_done(self):
        self.task_queue.task_done()

    def wait_all_task_down(self):
        while not self.task_queue.empty():
            print("\r剩余任务: " + str(self.task_queue.qsize()),end='')
            time.sleep(5)
        self.task_queue.join()
        for i in range(self.work_thread_num):
            self.work_thread[i].set_run_flag(False)
        for i in range(self.work_thread_num):
            self.work_thread[i].join()
