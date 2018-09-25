#!/usr/bin/env python
# coding: utf-8
# Date  : 2018-08-13 13:34:12
# Author: b4zinga
# Email : b4zinga@outlook.com
# Func  : proxy pool
# usage : proxies = getProxies()

import re
import requests


headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }

def getXiCi():
    """get the proxies info from xici"""
    url = "http://www.xicidaili.com/"
    req = requests.get(url, headers=headers, timeout=5)
    # ip 端口 服务器地址 是否匿名 类型 存活时间 验证时间
    regex = '<td>(\d+\.\d+\.\d+\.\d+).*?(\d+).*?<td>(\w+).*?">(\w+).*?<td>(\S+)</td>.*?(\d+\w+).*?(\d+\w+)</td>'
    items = re.compile(regex, re.S).findall(req.text)
    return items


def getKuaiDaiLi():
    """get the proxies from kuaidaili"""
    url = "https://www.kuaidaili.com/free/inha/2/"
    req = requests.get(url, headers=headers, timeout=5)
    regex = '<tr>.*?IP">(.*?)<.*?PORT">(\d+).*?匿名度">(.*?)<.*?类型">(.*?)<'
    items = re.compile(regex, re.S).findall(req.text)
    return items


def getProxies():
    """return a list of proxies."""
    proxies = []

    info = getXiCi()

    for i in info:
        tmp={}
        tmp[str(i[4]).lower()] =  i[0] + ":" + i[1]
        proxies.append(tmp)

    return proxies


if __name__ == '__main__':
    print(getProxies())