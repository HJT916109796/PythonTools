# !/usr/bin/env python
# coding  : utf-8
# Date    : 2018-03-20 13:45:00
# Author  : b4zinga
# Email   : b4zinga@outlook.com
# Function: mini redis-cli tools


import socket
import sys
import re
socket.setdefaulttimeout(3)


def sendCommand(host, port):
    sock = socket.socket()
    try:
        sock.connect((host,port))
    except Exception as err:
        print(err)
        sys.exit(0)

    while True:
        cmd = input('>')
        if cmd == 'exit':
            print('\nByeBye...\n')
            break

        cmd = makeCmd(cmd)

        try:
            sock.send(cmd.encode())
            while True:
                recv = sock.recv(1024)
                print(handleRecv(recv))
                if len(recv)<1024:  # 循环接收1024, 如果长度小于1024则默认后面已经无内容,break
                    break
        except Exception as err:
            print(err)
    
    sock.close()



def makeCmd(cmd):
    command = "*"
    cmd = cmd.split()
    command = command + str(len(cmd)) + '\r\n'
    for c in cmd:
        command = command + '$' + str(len(c)) + '\r\n' + c + '\r\n'
    return command

def handleRecv(recvdate):
    recvdate = recvdate.decode()
    if recvdate.startswith('*'):
        recvdate=recvdate[2:].strip('\r\n')
    recvdate = re.sub('\$\d+\\r\\n', '', recvdate)
    return recvdate



if __name__ == '__main__':
    usage="""
====================================================
        mini redis-cli tools.

Usage:
        redis-cli.py <IP> <port>

        Default ip      127.0.0.1
        Default port    6379

Example:
        redis-cli.py 127.0.0.1 6379
        redis-cli.py 127.0.0.1 \n
        redis-cli.py 192.168.1.133 6378
====================================================

    """
    if '-h' in sys.argv or '--help' in sys.argv or len(sys.argv) > 3:
        print(usage)
        sys.exit(0)

    if len(sys.argv) == 1:
        sys.argv.append('127.0.0.1')

    if len(sys.argv) == 2:
        sys.argv.append(6379)

    sendCommand(sys.argv[1], int(sys.argv[2]))
