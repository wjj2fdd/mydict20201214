"""
dict 客户端
发起请求，展示结果
"""
from socket import *

ADDR = ("127.0.0.1", 8000)


# 创建网络连接
def main():
    s = socket()
    s.connect(ADDR)
    while True:
        print("""
        ========================welcome========================
        1.注册        2.登录        3.退出
        =======================================================
        """)
        cmd = input("输入选项：")
        if cmd == "1":
            do_register(s)
        elif cmd == "2":
            pass
        elif cmd == "3":
            pass
        else:
            print("请输入正确命令！")

if __name__ == '__main__':
    main()