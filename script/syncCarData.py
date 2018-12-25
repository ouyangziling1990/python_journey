#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import get_start_time
from utils import set_start_time
from utils import connectDB
from datetime import datetime
import time

time_type_key = 'BIGDATA_CAR_TIME'
db_key = 'TaxiDataDB'
big_data_key = 'BigDataDB'


def isEixst(id, tablename, con, cur):
    result = None
    sql = "select * from `%s` where id =%s" % (tablename, id)
    cur.execute(sql)
    con.commit()
    car_results = cur.fetchall()
    if len(car_results) == 0:
        result = False
    else:
        result = True
    return result


def getTaxiInfo(LastTime, oricon, oricur, BIGDATAcon, BIGDATAcur):
    sql = "select id, taxi_plate, taxi_company_id, group_id, facetrack_id_in, facetrack_id_out, createdate_in, createdate_out, interval_seconds, created_time from vehicle_stayed_info where created_time >'%s'" % LastTime
    oricur.execute(sql)
    oricon.commit()
    results = oricur.fetchall()
    print('get results length: ', len(results))
    for each in results:
        colslist = ['id', 'taxi_plate', 'taxi_company_id',
          'channel_id', 'facetrack_id_in',
          'facetrack_id_out',
          'createdate_in', 'createdate_out', 'interval_seconds', 'created_time', 'status']
        intorstrlist = [0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0]
        intorstr = ["", "'"]
        sql = ""
        if isEixst(each[0], 'taxi_stayed_info', BIGDATAcon, BIGDATAcur):
            print("update sql car ")
            outputsql = "UPDATE `taxi_stayed_info` set "
            for i in range(len(each)):
                if each[i] is not None:
                    outputsql = outputsql + colslist[i] + "=" + intorstr[
                        intorstrlist[i]] + str(each[i]) + intorstr[intorstrlist[i]] + ","
            sql = outputsql[:-1] + " WHERE id=%s" % each[0]

        else:
            outputcols = ""
            outputValue = ""
            print("car insert ")
            for i in range(len(each)):
                if each[i] is not None:
                    outputcols = outputcols + colslist[i] + ","
                    outputValue = outputValue + \
                        intorstr[intorstrlist[i]] + \
                        str(each[i]) + intorstr[intorstrlist[i]] + ","

            sql = "INSERT INTO `taxi_stayed_info`(" + outputcols[
                :-1] + ")VALUES(" + outputValue[:-1] + ")"
        if sql:
            try:
                BIGDATAcur.execute(sql)
                BIGDATAcon.commit()
            except Exception as e:
                print(e)
                BIGDATAcon.rollback()
            else:
                pass
            finally:
                pass


def main():
    while True:
        carCon, carCur = connectDB(db_key)
        bigDataCon, bigDataCur = connectDB(big_data_key)
        lastTime = get_start_time(time_type_key)
        print('lastTime: ', lastTime)
        if not lastTime:
            return

        # 获取最新的更新时间
        now = datetime.now()
        now_time = now.strftime("%Y-%m-%d %H:%M:%S")

        getTaxiInfo(lastTime, carCon, carCur, bigDataCon, bigDataCur)
        set_start_time(time_type_key, now_time)

        carCon.close()
        bigDataCon.close()
        print("begin to sleep 10 seconds")
        print("-----------------------------")
        time.sleep(10)


if __name__ == '__main__':
    main()
