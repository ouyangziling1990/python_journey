#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
author ziling
simple code for HTTP Get method using python requests
'''
import requests
def getHtmlText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        # print("encoding", r.apparent_encoding)
        r.encoding = 'utf-8'
        return r.text
    except:
        return ""

def main():
    url = "http://www.baidu.com"
    r = getHtmlText(url)
    print(r)

if __name__ == "__main__":
    main()