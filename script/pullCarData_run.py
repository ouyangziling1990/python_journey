import pymysql
import time
from setting_db import DATABASES
import traceback

FORMAT_TIME = "2018-06-27 00:00:00"

def connectBigDataDB():
    DB = DATABASES['BigDataDB']
    con = pymysql.connect(host=DB['HOST'], user=DB['USER'],
                          passwd=DB['PASSWORD'],
                          db=DB['NAME'], port=DB['PORT'], charset="utf8")  # 以后每次需要数据库连接就是用connection（）函数获取连接就好了
    cur = con.cursor()
    return con, cur

def TaxiDataDB():
    DB = DATABASES['TaxiDataDB']
    con = pymysql.connect(host=DB['HOST'], user=DB['USER'],
                          passwd=DB['PASSWORD'],
                          db=DB['NAME'], port=DB['PORT'], charset="utf8")  # 以后每次需要数据库连接就是用connection（）函数获取连接就好了
    cur = con.cursor()
    return con, cur


def initTaxiLastTime(BIGDATAcon, BIGDATAcur):
    try:
        sql = "select created_time from `taxi_stayed_info` order by created_time desc limit 1"
        BIGDATAcur.execute(sql)
        BIGDATAcon.commit()
        results = BIGDATAcur.fetchall()
        data = results[0][0]
    except:
        data = FORMAT_TIME
    return data

def isEixst(id, tablename, con, cur):
    sql= "select * from `%s` where id =%s" % (tablename, id)
    cur.execute(sql)
    con.commit()
    results = cur.fetchall()
    if len(results) ==0:
        return False
    else:
        return True

def getTaxiInfo(LastTime, oricon, oricur, BIGDATAcon, BIGDATAcur):
    sql = "select id, taxi_plate, taxi_company_id, group_id, facetrack_id_in, facetrack_id_out, createdate_in, createdate_out, interval_seconds, created_time from vehicle_stayed_info where created_time >'%s'" % LastTime
    oricur.execute(sql)
    oricon.commit()
    results = oricur.fetchall()
    for each in results:
        colslist = ['id', 'taxi_plate', 'taxi_company_id', 'channel_id', 'facetrack_id_in', 'facetrack_id_out',
                    'createdate_in' , 'createdate_out', 'interval_seconds', 'created_time', 'status']
        intorstrlist = [0,1,0,0,1,1,1,1,0,1,0]
        intorstr = ["","'"]
        if isEixst(each[0], 'taxi_stayed_info', BIGDATAcon, BIGDATAcur):
            outputsql = "UPDATE `taxi_stayed_info` set "
            for i in range(len(each)):
                if each[i] is not None:
                    outputsql = outputsql + colslist[i]+"=" +intorstr[intorstrlist[i]]+ str(each[i]) + intorstr[intorstrlist[i]] + ","
            sql = outputsql[:-1]+" WHERE id=%s" %each[0]
            BIGDATAcur.execute(sql)
            BIGDATAcon.commit()
        else:
            outputcols=""
            outputValue=""
            for i in range(len(each)):
                if each[i] is not None:
                    outputcols = outputcols + colslist[i]+","
                    outputValue = outputValue +intorstr[intorstrlist[i]]+ str(each[i]) + intorstr[intorstrlist[i]] + ","

            sql = "INSERT INTO `taxi_stayed_info`(" + outputcols[:-1] + ")VALUES(" + outputValue[:-1] + ")"
            BIGDATAcur.execute(sql)
            BIGDATAcon.commit()


def run():
    BIGDATAcon, BIGDATAcur = connectBigDataDB()
    LastTime = initTaxiLastTime(BIGDATAcon, BIGDATAcur)

    BIGDATAcon.close()

    while True:
        Taxicon, Taxicur = TaxiDataDB()
        BIGDATAcon, BIGDATAcur = connectBigDataDB()
        try:
            getTaxiInfo(LastTime, Taxicon, Taxicur, BIGDATAcon, BIGDATAcur)
        except Exception as e:
            traceback.print_exc()
        LastTime = initTaxiLastTime(BIGDATAcon, BIGDATAcur)
        print('SUCC a cycle')
        time.sleep(5)
        Taxicon.close()
        BIGDATAcon.close()
if __name__ == '__main__':
    run()
