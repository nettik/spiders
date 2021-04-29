import threading
import queue
import fund_infoV2.classes.DatabaseHandler as DatabaseHandler


class SaveThread(threading.Thread):
    def __init__(self, thread_pool, run_flag):
        threading.Thread.__init__(self)
        self.thread_pool = thread_pool
        self.run_flag = run_flag
        self.db_handler = DatabaseHandler.DatabaseHandler('localhost', 'root', 'root', 'fundinfodb')
        self.db_handler.create_connection()

    def set_run_flag(self, run_flag):
        self.run_flag = run_flag

    def run(self):
        while self.run_flag:
            try:
                sql = self.thread_pool.get_save_task()
                self.db_handler.cursor.execute(sql)
                self.db_handler.conn.commit()
                self.thread_pool.save_task_done()
            except queue.Empty:
                pass
            except:
                self.thread_pool.save_task_done()
