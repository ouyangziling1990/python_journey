#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

# SECURITY WARNING: don't run with debug turned on in production!


DEBUG = False
# MySQL Database parameters

DATABASES = {
    #大数据平台数据库
    'BigDataDB': {
        'NAME': 'CorsfaceRepo',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '192.168.1.33',
        'PORT': 3306,
    },
    # 扰序人员库
    'FaceDataDB': {
        'NAME': 'CorsfaceRepo',
        'USER': 'yunshitu',
        'PASSWORD': '3byghbys',
        'HOST': '172.16.20.201',
        'PORT': 3306,
    },
    #出租车库
    'TaxiDataDB': {
        'NAME': 'CorsfaceRepo',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '192.168.2.60',
        'PORT': 3306,
    },
    # Corsface database
    'CorsfaceDB':{
        'NAME': 'CorsfaceRepo',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '192.168.1.172',
        'PORT': 3306,
    }
}

persistence_time_path = 'persistence_time.md'
INIT_TIME = '2008-06-25 00:00:00'
