#!/usr/bin/python3
# -*- coding: utf-8 -*-
#author ziling
#date 2018-06-09
import os
from bs4 import BeautifulSoup
import requests
# from crawler_requests import getHtmlText


def get_url(html_str):
    #get url for each novel
    url_list = []
    soup = BeautifulSoup(html_str, 'lxml')
    category_list = soup.find_all('div', class_='index_toplist mright mbottom')
    # print(category_list)
    for cate in category_list:
        name = cate.find('div', class_='toptab').span.string
        with open('./html/novel_list.csv', 'a+') as f:
            f.write("\nnovel category:{}\n".format(name))
        # general_list = cate.find(style="display:block")
        # print(general_list)
        book_list = cate.find_all('li')
        # 循环遍历出每一个小说的的名字，以及链接
        for book in book_list:
            link = 'https://www.qu.la/' + book.a['href']
            title = book.a['title']
            # 我们将所有文章的url地址保存在一个列表变量里
            url_list.append(link)
            with open('./html/novel_list.csv', 'a') as f:
                f.write("小说名：{:<} \t 小说地址：{:<} \n".format(title, link))
    return url_list

def get_novel_capter_list(url):
    # get url of one novel's capture
    print("get capture list: ", url)
    url_list =[]
    html_str = getHtmlText(url)
    # print(html_str)
    # return
    soup = BeautifulSoup(html_str, 'lxml')
    lista = soup.find_all('dd')
    txt_name = soup.find('h1')
    # print("txt_name:", txt_name)
    if txt_name:
        txt_name = txt_name.get_text()
    else:
        txt_name=""
    # print(txt_name)
    with open('./html/novel/{}.txt'.format(txt_name), "a+") as f:
        f.write('novel title:{}\n'.format(txt_name))
    for url in lista:
        url_list.append('https://www.qu.la/' + url.a['href'])
    # print(url_list, txt_name)
    return url_list, txt_name

def get_one_txt(url, txt_name):
    # get the content of one capter
    print("single capture", url)
    '''
    获取小说每个章节的文本
    并写入到本地
    '''
    html = getHtmlText(url).replace('<br/>', '\n')
    soup = BeautifulSoup(html, 'lxml')
    try:
        txt = soup.find('div', id='content').text.replace(
            'chaptererror();', '')
        title = soup.find('title').text

        with open('./html/novel/{}.txt'.format(txt_name), "a") as f:
            f.write(title + '\n\n')
            f.write(txt)
            print('当前小说：{} 当前章节{} 已经下载完毕'.format(txt_name, title))
    except:
        print('someting wrong')

def save_html(html_str, path="./html/html.text"):
    f = open(path, "w")
    f.write(html_str)
    f.close()

def getHtmlText(url):
    print("getHtml", url)
    headers = {
    'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    }
    r = requests.get(url, timeout=40, headers=headers)
    # r.raise_for_status(),
    # print("encoding", r.apparent_encoding)
    r.encoding = 'utf-8'
    return r.text

def main():
    # print(getHtmlText("http://www.baidu.com"))
    # return

    # get_one_txt("https://www.qu.la//book/11424/22600228.html", "ahag")
    # return
    # get_novel_capter_list("https://www.qu.la//book/38/")
    # return
    #handle the is 
    html_save_path = "./html/html.text"
    url = "https://www.qu.la/paihangbang"
    html_str = ""

    if not os.path.exists(html_save_path):
        print("save html str in ", html_save_path)
        html_str = getHtmlText(url)
        save_html(html_str, html_save_path)
    else:
        print("get html str from ", html_save_path)
        f = open(html_save_path, 'r')
        html_str = f.read()
        f.close
    url_list = get_url(html_str)
    # url singularize
    url_list = list(set(url_list))

    for novel_url in url_list:
        (capter_urls, name) = get_novel_capter_list(novel_url)
        for capture_url in capter_urls:
            get_one_txt(capture_url, name)

if __name__=="__main__":
    main()