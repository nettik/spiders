from queue import Queue
import fund_infoV2.classes.ParseThread as ParseThread
import fund_infoV2.classes.DownloadThread as DownloadThread
import fund_infoV2.classes.SaveThread as SaveThread


class ThreadPool:
    def __init__(self, download_thread_num, parse_thread_num, save_thread_num):
        self.download_thread_num = download_thread_num
        self.parse_thread_num = parse_thread_num
        self.save_thread_num = save_thread_num

        self.download_queue = Queue()
        self.parse_queue = Queue()
        self.save_queue = Queue()

        self.download_threads = []
        self.parse_threads = []
        self.save_threads = []

        self.thread_run_flag = True

    # 创建下载线程、解析线程
    def create_thread(self):
        # 创建下载线程
        for i in range(self.download_thread_num):
            self.download_threads.append(DownloadThread.DownloadThread(self, self.thread_run_flag))
        # 创建解析线程
        for i in range(self.parse_thread_num):
            self.parse_threads.append(ParseThread.ParseThread(self, self.thread_run_flag))
        # 创建存库线程
        for i in range(self.save_thread_num):
            self.save_threads.append(SaveThread.SaveThread(self, self.thread_run_flag))

    # 启动下载线程、解析线程
    def start_thread(self):
        for index in range(self.download_thread_num):
            self.download_threads[index].start()
        for index in range(self.parse_thread_num):
            self.parse_threads[index].start()
        for index in range(self.save_thread_num):
            self.save_threads[index].start()

    # 添加、获取、完成下载任务
    def put_download_task(self, url):
        self.download_queue.put(url)

    def get_download_task(self):
        return self.download_queue.get(block=False)

    def download_task_done(self):
        self.download_queue.task_done()

    # 添加、获取、完成解析任务
    def put_parse_task(self, html):
        self.parse_queue.put(html)

    def get_parse_task(self):
        return self.parse_queue.get(block=False)

    def parse_task_done(self):
        self.parse_queue.task_done()

    # 添加、获取、完成保存任务
    def put_save_task(self, sql):
        self.save_queue.put(sql)

    def get_save_task(self):
        return self.save_queue.get(block=False)

    def save_task_done(self):
        self.save_queue.task_done()

    # 等待所有线程结束
    def wait_all_task_done(self):
        self.download_queue.join()
        self.parse_queue.join()
        self.save_queue.join()

        for index in range(self.download_thread_num):
            self.download_threads[index].set_run_flag(False)

        for index in range(self.parse_thread_num):
            self.parse_threads[index].set_run_flag(False)

        for index in range(self.save_thread_num):
            self.save_threads[index].set_run_flag(False)

        for index in range(self.download_thread_num):
            self.download_threads[index].join()

        for index in range(self.parse_thread_num):
            self.parse_threads[index].join()

        for index in range(self.save_thread_num):
            self.save_threads[index].join()

        print("All work completed")
