# -*- coding: utf-8 -*-
'''
author ziling
simple code for parse html string
'''

from bs4 import BeautifulSoup
from crawler_requests import getHtmlText

def main():
    url ="http://www.baidu.com"
    html_doc = getHtmlText(url)
    soup = BeautifulSoup(html_doc, 'html.parser')
    print(soup.title)
    # print(soup.prettify())


if __name__ == "__main__":
    main()
