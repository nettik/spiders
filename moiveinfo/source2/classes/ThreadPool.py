from queue import Queue
from source2.classes.WorkThread import WorkThread
import time


class ThreadPool:

    def __init__(self, thread_num):
        self.task_queue = Queue()
        self.thread_num = thread_num
        self.work_thread = list()

    def create_and_start_thread(self):
        for i in range(self.thread_num):
            self.work_thread.append(WorkThread(self))
        for i in range(self.thread_num):
            self.work_thread[i].start()

    def put_task(self, suffix):
        self.task_queue.put(suffix)

    def get_task(self):
        return self.task_queue.get(block=False)

    def task_done(self):
        self.task_queue.task_done()

    def wait_all_task_done(self):
        while self.task_queue.qsize() > 0:
            print("\r剩余任务: " + str(self.task_queue.qsize()), end='')
            time.sleep(5)
        self.task_queue.join()
        for i in range(self.thread_num):
            self.work_thread[i].run_flag = False
        for i in range(self.thread_num):
            self.work_thread[i].join()
