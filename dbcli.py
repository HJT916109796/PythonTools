# !/usr/bin/env python           
# coding  : utf-8 
# Date    : 2018-05-06 10:22:58
# Author  : b4zinga
# Email   : b4zinga@outlook.com
# Function: database command line tool.

# TODO    : add oracle/mongodb/postgresql/Sybase/...


import re
import sys
import socket
import pymysql
import pymssql
import argparse
from prettytable import PrettyTable


class DB:
    def __init__(self, host, port, user, passwd):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd

        self.db = self.conn()

    def conn(self):
        pass
    
    def exec(self, sql):
        table = PrettyTable()
        self.cursor = self.db.cursor()
        rows = self.cursor.execute(sql)
        results = self.cursor.fetchall()
        for result in results:
            table.add_row(result)
        if not table.get_string() == '++\n||\n++\n++':
            print(table)


    def close(self):
        self.db.close()



class MsSql(DB):
    """Sql Server.
    sql example:
        >>> c = db.cursor()
        >>> c.execute("use master")  # default database
        >>> c.execute("select * from spt_values")
        >>> print(c.fetchall())

    show all databases: SELECT Name FROM Master..SysDatabases ORDER BY Name
    show all tables   : SELECT Name FROM DatabaseName..SysObjects Where XType='U' ORDER BY Name 
          XType='U'   : 表示所有用户表; 
          XType='S'   : 表示所有系统表;
    """
    def __init__(self, host, port, user, passwd):
        super().__init__(host, port, user, passwd)

    def conn(self):
        db = pymssql.connect(server=self.host, port=int(self.port), user=self.user, password=self.passwd)
        return db



class MySql(DB):
    """MySQL.
    """
    def __init__(self, host, port, user, passwd):
        super().__init__(host, port, user, passwd)

    def conn(self):
        db = pymysql.connect(host=self.host, port=int(self.port), user=self.user, password=self.passwd, charset='utf8')
        return db


class Redis(DB):
    """Redis.
    """
    def __init__(self, host, port, user, passwd):
        super().__init__(host, port, user, passwd)

    def conn(self):
        sock = socket.socket()
        try:
            sock.connect((self.host, int(self.port)))
        except Exception as err:
            print(err)
            sys.exit(0)
        return sock

    def exec(self, sql):
        if sql=='':
            return
        sql = self.makeCmd(sql)
        try:
            self.db.send(sql.encode())
            while True:
                recv = self.db.recv(1024)
                print(self.handleRecv(recv))
                if len(recv)<1024:  # 循环接收1024, 如果长度小于1024则默认后面已经无内容,break
                    break
        except Exception as err:
            print(err)

    @staticmethod
    def makeCmd(cmd):
        command = "*"
        cmd = cmd.split()
        command = command + str(len(cmd)) + '\r\n'
        for c in cmd:
            command = command + '$' + str(len(c)) + '\r\n' + c + '\r\n'
        return command

    @staticmethod
    def handleRecv(recvdate):
        recvdate = recvdate.decode()
        if recvdate.startswith('*'):
            recvdate=recvdate[2:].strip('\r\n')
        recvdate = re.sub('\$\d+\\r\\n', '', recvdate)
        return recvdate




def cmdLineParser():
    parser = argparse.ArgumentParser(description='database command line helper.',
                                     usage='\n\tpython {} -h ip -u username -p password -P port [mysql|mssql|redis]'.format(sys.argv[0]),
                                     epilog="\tPowerd by b4zinga.  <b4zinga@outlook.com>",
                                     add_help=False)

    
    parser.add_argument("-h", "--host", help="the host to connect")
    parser.add_argument("-u", "--user", help="username")
    parser.add_argument("-p", "--pwd", help="password")
    parser.add_argument("-P", "--port", help="port")

    parser.add_argument("server", type=str, choices=['mysql', 'mssql', 'redis',])

    parser.add_argument("--help", action="help", help="show help message and exit")

    if len(sys.argv) == 1:
        sys.argv.append('--help')
    args = parser.parse_args()

    return args


def cli():
    args = cmdLineParser()

    if not args.host:
        print('[-] please specify the host.')
        sys.exit(0)

    mydb = ""
    if args.server == 'mysql':
        if not args.port:
            args.port = 3306
        mydb = MySql(args.host, args.port, args.user, args.pwd)

    elif args.server == 'mssql':
        if not args.port:
            args.port = 1433
        mydb = MsSql(args.host, args.port, args.user, args.pwd)

    elif args.server == 'redis':
        if not args.port:
            args.port = 6379
        mydb = Redis(args.host, args.port, args.user, args.pwd)
        if args.pwd:
            mydb.exec("auth "+args.pwd)

    while True:
        cmd = input(">")
        if cmd == "exit":
            break

        try:
            mydb.exec(cmd)

        # mysql err
        except pymysql.err.InterfaceError as mysqlExitErr:
            break
        except pymysql.err.InternalError as mysqlInternalErr:
            print(mysqlInternalErr)
            continue
        except pymysql.err.ProgrammingError as mysqlSyntaxErr:
            print(mysqlSyntaxErr)
            continue
        # mssql err
        except pymssql.ProgrammingError as mssqlSyntaxErr:
            print(mssqlSyntaxErr)
            continue
        except pymssql.OperationalError as mssqlErr:
            continue

        except Exception as err:
            print(err)
    
    mydb.close()
    print('\n\tByeBye ~~\n')



if __name__ == "__main__":    
    cli()
