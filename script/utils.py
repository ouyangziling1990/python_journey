#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql
import time
from setting_db import DATABASES
from setting_db import persistence_time_path
from setting_db import INIT_TIME
import os
import json


def connectDB(DB_type):
    if not DB_type:
        return False
    DB = DATABASES[DB_type]
    state = True
    con = ""
    cur = ""
    try:
        con = pymysql.connect(host=DB['HOST'], user=DB['USER'],
                              passwd=DB['PASSWORD'],
                              db=DB['NAME'], port=DB['PORT'], charset="utf8")
        cur = con.cursor()
    except Exception as e:
        print(e)
        state = False
    else:
        pass
    finally:
        pass

    if state is False:
        print("database connection failed, sleep 5 seconds and try again then")
        time.sleep(5)
        connectDB(DB)

    return con, cur


def get_start_time(type_str):
    if not type_str:
        return None
    # 从持久化的文件中获取最新的时间。 不包括保存最新时间。
    # 采用json保存两个系统的起始时间，然后更新。
    return_str = INIT_TIME
    exist = os.path.exists(persistence_time_path)
    if not exist:
        return return_str
        # time_obj = {}
        # time_obj[type_str] = INIT_TIME
        # with open(persistence_time_path, 'w') as f:
        #     f.write(json.dumps(time_obj))
        # return return_str

    with open(persistence_time_path, 'r') as f:
        time_str = f.read()
        obj = json.loads(time_str)
        if type_str in obj:
            return_str = obj[type_str]
    return return_str


def set_start_time(type_str, time_str):
    if not type_str:
        return None
    time_save = {}
    exist = os.path.exists(persistence_time_path)
    if not exist:
        time_save[type_str] = time_str
        with open(persistence_time_path, 'w') as f:
            f.write(json.dumps(time_save))
    else:
        with open(persistence_time_path, 'r') as f:
            time_save = json.loads(f.read())
        with open(persistence_time_path, 'w') as f:
            time_save[type_str] = time_str
            f.write(json.dumps(time_save))


def main():
    corsfaceConn, corsfaceCur = connectDB(DATABASES['CorsfaceDB'])

    sql = "select created_time from `facetrack_info`"
    + "order by created_time desc limit 0, 1"
    corsfaceCur.execute(sql)
    corsfaceConn.commit()
    results = corsfaceCur.fetchall()
    print(results)
    corsfaceConn.close()


if __name__ == '__main__':
    main()
