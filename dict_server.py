"""
dict 服务端部分
处理请求逻辑
"""

from multiprocessing import Process
from socket import *
import signal
import sys
from operation_db import *
import time

# 全局变量
HOST = "0.0.0.0"
PORT = 8000
ADDR = (HOST, PORT)


# 处理登录
def do_login(c, db, data):
    tmp = data.split(" ")
    name = tmp[1]
    passwd = tmp[2]
    if db.entry(name, passwd):
        c.send(b"OK")
    else:
        c.send(b"FAIL")


# 处理注册
def do_register(c, db, data):
    tmp = data.split(" ")
    name = tmp[1]
    passwd = tmp[2]
    if db.register(name, passwd):
        c.send(b"OK")
    else:
        c.send(b"FAIL")


# 处理单词查询和插入历史记录
def do_query(c, db, data):
    tmp = data.split(" ")
    name = tmp[1]
    word = tmp[2]
    # 插入历史记录
    db.insert_history(name, word)
    # 查单词 没查到返回None
    mean = db.query(word)
    if not mean:
        c.send("没有找到该单词".encode())
    else:
        msg = "%s : %s" % (word, mean)
        c.send(msg.encode())


# 处理记录记录查询
def do_history(c, db, data):
    tmp = data.split(" ")
    name = tmp[1]
    result = db.history(name)
    print(result)
    if not result:
        c.send("没有历史记录".encode())
    else:
        for i in result:
            msg = " ".join(i)
            c.send(msg.encode())
            c.send("\n".encode())
        time.sleep(0.5)
        c.send("O".encode())


# 处理客户端请求
def do_request(c, db):
    cur = db.create_cursor()  # 生成游标
    while True:
        data = c.recv(1024).decode()
        print(c.getpeername(), ":", data)
        if not data or data[0] == "E":
            # db.close()
            c.close()
            sys.exit("客户端退出")
        elif data[0] == "R":
            do_register(c, db, data)
        elif data[0] == "L":
            print("收到用户登录请求")
            do_login(c, db, data)
        elif data[0] == "Q":
            do_query(c, db, data)
        elif data[0] == "H":
            do_history(c, db, data)
        else:
            return


# 网络连接
def main():
    # 创建数据库链接对象
    db = Database()

    # 创建tcp套接字
    s = socket()
    # 程序关闭端口释放
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(5)

    # 处理僵尸进程(linux)
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    # windows
    # signal.signal(signal.SIGINT, signal.SIG_IGN)

    # 等待客户端链接
    print("listen the port 8000")
    while True:
        try:
            c, addr = s.accept()
            print("connect from", addr)
        except KeyboardInterrupt:
            s.close()
            db.close()
            sys.exit("服务器退出")
        except Exception as e:
            print(e)
            continue
        # 创建子进程
        p = Process(target=do_request, args=(c, db))
        # 父进程结束子进程跟着结束
        p.daemon = True
        p.start()


if __name__ == '__main__':
    main()
