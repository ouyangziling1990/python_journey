#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
author ziling
'''

# from selenium import webdriver

# browser = webdriver.Chrome()
# browser.get('http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd=%E4%B8%AD%E5%9B%BD&rsv_pq=c53896ef0003164e&rsv_t=f0fba7rAp8INNgwu3nSzPOJkj9w0MQm3cv5L16yUvQDXWZ4fTG%2B9N18X5m0&rqlang=cn&rsv_enter=1&rsv_sug3=10&rsv_sug1=5&rsv_sug7=100&rsv_sug2=0&inputT=1528&rsv_sug4=2801')
# assert "Python" in browser.title

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("http://www.python.org")
assert "Python" in driver.title
elem = driver.find_element_by_name("q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
# driver.close()
