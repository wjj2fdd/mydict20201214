"""
dict 服务端部分
处理请求逻辑
"""

from multiprocessing import Process
from socket import *
import signal
import sys
from operation_db import *

# 全局变量
HOST = "0.0.0.0"
PORT = 8000
ADDR = (HOST, PORT)

# 处理注册
def do_register(c,db,data):
    tmp = data.split(" ")
    name = tmp[1]
    passwd = tmp[2]

# 处理客户端请求
def do_request(c, db):
    cur = db.create_cursor() # 生成游标
    while True:
        data = c.recv(1024).decode()
        print(c.getpeername(), ":", data)
        if data[0] == "R":
            do_register(c,db,data)




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
