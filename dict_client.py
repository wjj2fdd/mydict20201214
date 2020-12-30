"""
dict 客户端
发起请求，展示结果
"""
from socket import *

s = socket()
ADDR = ("127.0.0.1", 8000)
s.connect(ADDR)


# 查询单词
def do_query(name):
    while True:
        word = input("单词：")
        if word == "##":  # 结束单词查询
            break
        msg = "Q %s %s" % (name, word)
        s.send(msg.encode())
        # 等待回复
        data = s.recv(2048).decode()
        print(data)


# 查询历史记录
def do_history(name):
    msg = "H %s" % name
    s.send(msg.encode())
    # 等待回复
    while True:
        data = s.recv(2048).decode()
        if data == "O":
            print("查询结束")
            break
        print(data)


# 二级界面
def login(name):
    while True:
        print("""
        ========================query==========================
        1.查单词        2.历史记录       3.注销
        =======================================================
        """)
        cmd = input("输入选项：")
        if cmd == "1":
            do_query(name)
        elif cmd == "2":
            do_history(name)
        elif cmd == "3":
            return
        else:
            print("请输入正确命令！")


# 处注册
def do_register():
    while True:
        name = input("User:")
        passwd = input("passwd:")
        passwd1 = input("passwd again:")
        if (" " in name) or (" " in passwd):
            print("用户名或密码不能有空格")
            continue
        if passwd != passwd1:
            print("两次密码不一致")
            continue
        msg = "R %s %s" % (name, passwd)
        # 发送请求
        s.send(msg.encode())
        # 接受反馈
        data = s.recv(128).decode()
        if data == "OK":
            print("注册成功")
            login(name)
        else:
            print("注册失败")
        return


# 处理登录
def do_login():
    name = input("User:")
    passwd = input("passwd:")
    msg = "L %s %s" % (name, passwd)
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data == "OK":
        print("登录成功")
        login(name)
    else:
        print("登录失败")


# 创建网络连接
def main():
    while True:
        print("""
        ========================welcome========================
        1.注册        2.登录        3.退出
        =======================================================
        """)
        cmd = input("输入选项：")
        if cmd == "1":
            do_register()
        elif cmd == "2":
            do_login()
        elif cmd == "3":
            s.send(b'E')
            print("谢谢使用")
            return
        else:
            print("请输入正确命令！")


if __name__ == '__main__':
    main()
