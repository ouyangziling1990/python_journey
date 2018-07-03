#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql
import time
from setting_db import DATABASES

def connectDB(DB):
    if not DB:
        return False
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

    if state == False:
        print("database connection failed, sleep 5 seconds and try again then")
        time.sleep(5)
        connectDB(DB)

    return con, cur

def main():
    corsfaceConn, corsfaceCur = connectDB(DATABASES['CorsfaceDB'])

    sql="select created_time from `facetrack_info` order by created_time desc limit 0, 1"
    corsfaceCur.execute(sql)
    corsfaceConn.commit()
    results = corsfaceCur.fetchall()
    print(results)
    corsfaceConn.close()

if __name__=='__main__':
    main()