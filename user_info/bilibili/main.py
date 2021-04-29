from bilibili.classes.ThreadPool import ThreadPool
import time


def main():
    thread_pool = ThreadPool(3)
    thread_pool.init_work("39089645")
    thread_pool.start_thread()
    time.sleep(30)
    thread_pool.wait_all_task_done()


if __name__ == '__main__':
    main()
