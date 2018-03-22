# !/usr/bin/env python           
# coding  : utf-8 
# Date    : 2018-03-21 14:18:48
# Author  : b4zinga
# Email   : b4zinga@outlook.com
# Function: 查询文件夹内所有文件的敏感信息 Sensitive information about all files in a folder

import os
import re


regex_list = [
    # IP address
    '10\.\d+\.\d+\.\d+|192\.\d+\.\d+\.\d+|172\.16\.\d+\.\d+|127\.0\.0\.1',  # '(\d+\.\d+\.\d+\.\d+)', '\w+\.\w+\.\w+',
    # username
    'user=|username=|usr=|xingming=|yonghu=|yonghuming=|ming=|用户名=|名字:',
    'user"=|username"=|usr"=|xingming"=|yonghu"=|yonghuming"=|ming"=',
    
    'user:|username:|usr:|xingming:|yonghu:|yonghuming:|ming:|用户名:|名字:',
    'user":|username":|usr":|xingming":|yonghu":|yonghuming":|ming":',

    # password
    'passowrd=|passwd=|pwd=|pd=|mima=|ma=|paswd=|密码=',
    'passowrd"=|passwd"=|pwd"=|pd"=|mima"=|ma"=|paswd"=',

    'password:|passwd:|pwd:|mima:|mim:|paswd:|密码:',
    'password":|passwd":|pwd":|mima":|mim":|paswd":',
    # phone
    '1\d{10} ',
    # email
    '[\w._%+-]+@[\w.-]+\.[\w]{2,4}',
    # key words
    # 'keys|key|keyword|keywords',
]


def getAllFile(dirs):
    file_list = []
    for root, d , files in os.walk(dirs, topdown=False):
        for name in files:
            file_list.append(os.path.join(root,name))

        # for name in d:
        #     print(os.path.join(root, name))  
    return file_list


def searchInfomation(file, extension=('.js','.css')):
    if not file.endswith(extension):
        f = open(file, 'r', encoding='utf-8')
        txt = f.read()
        f.close()

        for regex in regex_list:
            result = re.findall(regex, txt)
            if result:
                print(file)
                print(set(result))



def main(dirs, showPassFile=False): # showPassFile 默认不显示跳过的文件
    errcount = []
    finishedcount = []
    files = getAllFile(dirs)
    print('\n\n==============================Totally '+str(len(files))+' files==============================\n')
    for file in files:
        try:
            searchInfomation(file)
            finishedcount.append(file)
        except:
            errcount.append(file)

    print('\n\n================================finished files:'+str(len(finishedcount))+'==============================\n')
    print('\n\n==============================unfinished files:'+str(len(errcount))+'==============================\n')
    if showPassFile:
        print(errcount)




if __name__ == '__main__':
    dirs = r'C:\Users\xxx\Desktop\xxx'
    main(dirs=dirs, showPassFile=True)