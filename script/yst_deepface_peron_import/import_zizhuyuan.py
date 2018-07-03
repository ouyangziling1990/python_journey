# -*- coding: utf-8 -*-

import argparse
import pymysql
import os
import base64
import requests
import json
import uuid
import time

DEEPFACE_URL = 'http://192.168.14.4:8000'
DEEPFACE_APP_KEY= '2f0c6101_9b82_4459_8e0a_91fda474f166'

DATA_PATH = './imgs/zizhuyuan'
# DATA_PATH = './test'

WEBSITE_PATH = '/home/user/Corsface'
IMAGE_STORE_PATH = '/static/Upload/person/import/'
error_list = []

con = pymysql.connect("localhost", user="root", passwd="123456", port=3306, db="CorsfaceRepo", charset="utf8")
cur = con.cursor()

def cropface(base64, url, app_key):
    payload = {
        "id":1,
        "jsonrpc":"2.0",
        "method":"cropface",
        "params":{
            "appkey":app_key,
            "style": {
            },
            "img":base64
        }
    }
    img, sex = (None, None)
    try:
        response = requests.post(url,data = json.dumps(payload),headers = json.loads('{"content-type": "application/json"}'))
        response = json.loads(response.text)
        print(response)
        result = response['result']
        code = result['code']
        if code == 0:
            img = result['results']['img']
            sex = result['results']['sex']
        else:
            pass
    except Exception as e:
        return 'error', 1
        print(e)
    else:
        pass
    finally:
        pass
    return img, sex

def createPersonGroup(groups):
    print('Creating person group...')
    for group in groups:
        cur.execute("SELECT id FROM person_group where group_name = '%s'" % (group))
        result = cur.fetchall()
        if not len(result):
            cur.execute("INSERT INTO person_group(group_uuid, group_name, alarm_sound_id, remark, created_time) VALUES('%s', '%s', 1, '%s', now())" % (str(uuid.uuid1()), group, group))
            con.commit()
            print('>>> %s created...' % group)
        else:
            print('>>> %s duplicated...' % group)
    return None

def createPerson(if_crop):
    print('Creating person...')

    group_path = DATA_PATH + '/'
    persons = os.listdir(group_path)
    whole_count = len(persons)
    count = 0
    for person_info in persons:
        # print('>>> %s' % person_info)
        count = count + 1
        print(">>> %s in whole person %s, person_info %s" %(count, whole_count, person_info))
        add_one_person(person_info)

def add_one_person(person_info):
    try:
        person_name, id_card, img_index = person_info.split('_')
    except Exception as e:
        print(e)
    else:
        pass
    finally:
        pass
    # 2为证件照，1为实际场景照。
    img_type = 2
    if img_index == '1.jpg':
        # 获取证件照的图片
        person_info2 = person_name + "_" + id_card + "_"+"2.jpg"
        img_type = 1
        # 证件照片
        recognise_img(person_info2, 1, 2)
        recognise_img(person_info, 1, img_type)
    else:
        recognise_img(person_info, 1, img_type)

def get_sex(id_card):
    res = ""
    if not id_card:
        res = -1
    elif len(id_card) == 15:
        res = jo(id_card[14])
    elif len(id_card) == 18:
        res = jo(id_card[16])
    else :
        res = -1
    return res

def jo(num):
    if (int(num)%2) == 1:
        return 2
    else:
        return 1

def recognise_img(person_info, if_crop, img_type):
    person_name, id_card, img_index = person_info.split('_')
    
    # get image base64 str
    image_path = DATA_PATH + '/' + person_info
    if not os.path.exists(image_path):
        return "not"

    file = open(image_path, 'rb')
    base64_image = str(base64.b64encode(file.read()), encoding='utf-8')
    file.close()

    if if_crop == 1:
        base64_image, sex = cropface(base64_image, DEEPFACE_URL, DEEPFACE_APP_KEY)
        if sex == 1:
            sex = 1
        else:
            # Corsface 中女为1
            sex = 2
        if (not base64_image or base64_image == 'error'):
            if base64_image == 'error':
                print("add error %s" % person_info)
                error_list.append(person_info)
            #没有识别结果或者报错，直接返回
            return False
        # 当前识别不准，先都设置成为位置。
    sex = get_sex(id_card)

    
    image_name = str(uuid.uuid1()) + '.jpg'
    image_path = IMAGE_STORE_PATH + image_name

    with open(WEBSITE_PATH + image_path, 'wb') as g:
        g.write(base64.b64decode(base64_image))

    cur.execute("SELECT person_id FROM person_info where id_card = '%s'" % (id_card))
    results = cur.fetchall()
    person_id = ""
    if len(results):
        if img_type == 2:
            # 对于有证件照的图片则已经被添加完毕，直接返回。
            return
        person_id = results[0][0]
    else:
        person_id = str(uuid.uuid1())
        cur.execute("insert into person_info " \
            "(person_id, group_id, gender, name, id_card, face_image, isdeleted, created_time, updated_time) " \
            " values('%s', %s, %s, '%s', '%s', '%s', 0, now(), now())" % (person_id, 1, sex, person_name, id_card, image_path))
        con.commit()
        print('>>> %s created successful...' % person_info)
    print("add person img", person_id)
    cur.execute("INSERT INTO person_image(person_id, image_id, face_image, isdeleted, created_time) values('%s', '%s', '%s', 0, now())" % (person_id, str(uuid.uuid1()), image_path))
    con.commit()

def importPerson(if_crop):
    # groups = os.listdir(DATA_PATH)
    # createPersonGroup(groups)
    createPerson(1)

def main():
    path = WEBSITE_PATH + IMAGE_STORE_PATH;
    if not os.path.exists(path):
        os.makedirs(path)
    

    importPerson(1)
    count = 0
    while len(error_list) != 0:
        add_one_person(error_list.pop(0))
        count = count +1
        if count == 550:
            print("error_list len %s"% len(error_list))
            time.sleep(1)
            count = 0
    con.close()

if __name__ == '__main__':
    main()

