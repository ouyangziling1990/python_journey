#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
author ziling

'''
from bs4 import BeautifulSoup
from crawler_requests import getHtmlText

def get_content(url):
    comments = []
    html = getHtmlText(url)

    if(html ==""):
        return
    # print(html)

    soup = BeautifulSoup(html, 'html.parser')
    liTags = soup.find_all('li', attrs={'class':' j_thread_list clearfix'})
    # print(liTags)
    for li in liTags:
        comment = {}
        try:
            comment['title'] = li.find('a', attrs={'class':'j_th_tit '}).get_text().strip()
            comment['author'] = li.find('span', attrs={'class':'tb_icon_author '}).text.strip()
            comment['last_replay_time'] = li.find('span', attrs={'class':'threadlist_reply_date pull_right j_reply_data'}).text.strip()
            comment['replayCount'] = li.find('span', attrs={'class':'threadlist_rep_num center_text'}).text.strip()

            comments.append(comment)
        except:
            print('error')
            continue

    return comments

def main(baseUrl, deepth):
    url_list = []
    for i in range(0, deepth):
        tmp = baseUrl + "&pn=" + str(50*i)
        url_list.append(tmp)

    for url in url_list:
        print("begin to parser", url)
        content = get_content(url)
        for i in range(len(content)):
            print(content[i])
        # parseInfo(content)


if __name__ == "__main__":
    url ="http://tieba.baidu.com/f?kw=%E7%94%9F%E6%B4%BB%E5%A4%A7%E7%88%86%E7%82%B8&ie=utf-8"
    deepth = 1
    main(url, deepth)