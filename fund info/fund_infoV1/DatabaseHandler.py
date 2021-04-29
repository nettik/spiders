import pymysql


class DatabaseHandler(object):

    def __init__(self, host, username, password, dbname):
        self.__host = host
        self.__username = username
        self.__password = password
        self.__dbname = dbname
        self.__conn = pymysql.NULL
        self.__cursor = pymysql.NULL

    def __del__(self):
        if self.__conn != pymysql.NULL:
            self.__cursor.close()
        if self.__cursor != pymysql.NULL:
            self.__conn.close()

    @property
    def conn(self):
        return self.__conn

    @property
    def cursor(self):
        return self.__cursor

    @property
    def dbname(self):
        return self.__dbname

    @dbname.setter
    def dbname(self, new_dbname):
        if isinstance(new_dbname, str):
            self.__dbname = new_dbname
        else:
            print("error: 输入类型错误")

    def create_connection(self):
        self.__conn = pymysql.connect(
            self.__host, self.__username,
            self.__password, self.__dbname)
        self.__cursor = self.__conn.cursor()

    def find_all(self, table_name):
        sql = "select * from" + table_name
        self.__cursor.execute(sql)
        data = self.__cursor.fetchall()
        return data
