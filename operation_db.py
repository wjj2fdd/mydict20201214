"""
dict 项目用于处理数据
"""
import pymysql


# 编写功能类 提供给服务端使用

class Database:
    def __init__(self, host="localhost", port=3306, user="root", passwd="123456", database="mydict", charset="utf8"):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.database = database
        self.charset = charset
        self.connect_db()  # 链接数据库

    def connect_db(self):
        self.db = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                                  database=self.database, charset=self.charset)

    # 创建游标
    def create_cursor(self):
        self.cur = self.db.cursor()

    # 关闭数据库
    def close(self):
        self.cur.close()
        self.db.close()