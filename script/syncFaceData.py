#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import get_start_time
from utils import set_start_time
from utils import connectDB
from datetime import datetime
import time

time_type_key = 'BIGDATA_FACE_TIME'
db_key = 'CorsfaceDB'
big_data_key = 'BigDataDB'
def getFaceInfo(lastTime, faceCon, faceCur, bigDataCon, bigDataCur):
    sql = "select `id`,`facetrack_id`,`age`,`glasses`,`sex`,`src_id`,`createdate`,`images`,`recognize_id`,`status`,`matched_person_id`,`matched_percent`,`matched_score`, `created_time` from facetrack_info where created_time >'%s' and status = 1" % lastTime
    faceCur.execute(sql)
    faceCon.commit()
    results = faceCur.fetchall()
    print('new capture alarmtrack length:', len(results))

    if len(results) == 0:
        return

    src_ids = set([])
    person_ids = set([])
    for each in results:
        src_ids.add(each[5])
        person_ids.add(str(each[10]))
    camera_id_map = getCamearInfo(src_ids, faceCon, faceCur)
    person_id_map = getPersonInfo(person_ids, faceCon, faceCur)
    sql = "INSERT INTO `facetrack_info`(`id`,`facetrack_id`,`age`,`glasses`,`sex`,`src_id`,`createdate`,`images`,`recognize_id`,`status`,`matched_person_id`, `matched_percent`,`matched_score`,`created_time`,`group_id`, `group_name`,`camera_id`, `camera_name`,`matched_person_name`)VALUES"
    flag = False
    for each in results:
        person_id = each[10]
        print("person_id", person_id)
        person_info = person_id_map.get(person_id)
        if not person_info:
            person_name = ""
            person_group_id = 0
            person_group_name = ""
        else:
            person_name, person_group_id, person_group_name  = person_info[1:]

        src_id = each[5]
        camera_info = camera_id_map.get(src_id)
        if not camera_info:
            camera_id = 0
            camera_name = ""
        else:
            camera_id, camera_name = camera_info[:2]
        if flag:
            sql +=','
        tmp = list(each)
        tmp += [person_group_id, person_group_name, camera_id, camera_name, person_name]
        sql +="('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"% tuple(tmp)
        flag = True
        # print(sql)
        # break
    bigDataCur.execute(sql)
    # executemany
    bigDataCon.commit()

def getCamearInfo(src_ids, faceCon, faceCur):
    camera_id_map = {}
    src_ids_str = ",".join(src_ids)
    sql_location = "select id, camera_name, src_id from camera_info WHERE src_id in ('%s')" % src_ids_str
    faceCur.execute(sql_location)
    faceCon.commit()
    camera_infos = faceCur.fetchall()
    if len(camera_infos) > 0:
        for camera in camera_infos:
            camera_id_map[camera[2]] = camera;
    return camera_id_map

def getPersonInfo(person_ids, faceCon, faceCur):
    person_id_map = {}
    src_ids_str = "','".join(person_ids)
    sql_location = "SELECT p.id, p.name, p.group_id, g.group_name from person_info p left join person_group g on p.group_id = g.id WHERE p.id in ('%s')" % src_ids_str

    faceCur.execute(sql_location)
    faceCon.commit()
    person_infos = faceCur.fetchall()
    print("sql_location", sql_location)
    # print(person_infos)
    if len(person_infos) > 0:
        for camera in person_infos:
            person_id_map[camera[0]] = camera;
    return person_id_map

def main():
    while True:
        faceCon, faceCur = connectDB(db_key)
        bigDataCon, bigDataCur = connectDB(big_data_key)
        lastTime = get_start_time(time_type_key)
        print('lastTime: ', lastTime)
        if not lastTime:
            return
        
        # 获取最新的更新时间
        now = datetime.now()
        now_time = now.strftime("%Y-%m-%d %H:%M:%S")
        try:
            getFaceInfo(lastTime, faceCon, faceCur, bigDataCon, bigDataCur)
            set_start_time(time_type_key, now_time)
        except Exception as e:
            print(e)
            bigDataCon.rollback()
        else:
            pass
        finally:
            pass

        faceCon.close()
        bigDataCon.close()
        print("begin to sleep 10 seconds")
        print("-----------------------------")
        time.sleep(10)

if __name__ == '__main__':
    main()