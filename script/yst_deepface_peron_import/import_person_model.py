#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author ziling
# date 2018-07-03
# use zizhuyuan as example, 
# the container containes imgs as name_idcard_1.png see 杨治甫_410126197405096512_1.jpg
# 

from ../util/utils import connectDB
from deepface_api import cropface
DB_KEY = 'YANJIAO_DB'
WEBSITE_PATH = '/home/user/Corsface'
IMAGE_STORE_PATH = '/static/Upload/person/import/'
DATA_PATH = './imgs/zizhuyuan'
DEEPFACE_URL = 'http://192.168.14.4:8000'
DEEPFACE_APP_KEY= '2f0c6101_9b82_4459_8e0a_91fda474f166'

con, cur = connectDB(DB_KEY)

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
    '''
        use identity code to get sex info.
    '''
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
    image_path = DATA_PATH + '/' + person_info

    if not os.path.exists(image_path):
        return "not"

    # check person is exists or not
    cur.execute("SELECT person_id FROM person_info where id_card = '%s'" % (id_card))
    results = cur.fetchall()
    person_id = ""
    if len(results):
        if img_type == 2:
            # 对于有证件照的图片则已经被添加完毕，直接返回。
            return
        person_id = results[0][0]

    file = open(image_path, 'rb')
    base64_image = str(base64.b64encode(file.read()), encoding='utf-8')
    file.close()

    if if_crop == 1:
        base64_image, sex = cropface(base64_image, DEEPFACE_URL, DEEPFACE_APP_KEY)
        if (not base64_image or base64_image == 'error'):
            if base64_image == 'error':
                print("add error %s" % person_info)
                error_list.append(person_info)
            return False
    sex = get_sex(id_card)
    
    image_name = str(uuid.uuid1()) + '.jpg'
    image_path = IMAGE_STORE_PATH + image_name

    with open(WEBSITE_PATH + image_path, 'wb') as g:
        g.write(base64.b64decode(base64_image))

    
    if not len(results):
        person_id = str(uuid.uuid1())
        cur.execute("insert into person_info " \
            "(person_id, group_id, gender, name, id_card, face_image, isdeleted, created_time, updated_time) " \
            " values('%s', %s, %s, '%s', '%s', '%s', 0, now(), now())" % (person_id, 1, sex, person_name, id_card, image_path))
        con.commit()
        print('>>> %s created successful...' % person_info)
    
    try:
        cur.execute("INSERT INTO person_image(person_id, image_id, face_image, isdeleted, created_time) values('%s', '%s', '%s', 0, now())" % (person_id, str(uuid.uuid1()), image_path))
        con.commit()
    except Exception as e:
        print(e)
    else:
        pass
    finally:
        pass


def main():
    path = WEBSITE_PATH + IMAGE_STORE_PATH;
    if not os.path.exists(path):
        os.makedirs(path)
    
    createPerson(1)
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