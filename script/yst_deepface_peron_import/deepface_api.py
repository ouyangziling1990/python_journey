#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author ziling
# date 2018-07-03


def cropface(base64, url, app_key):
    """
    use img base64 to parse face in img
    url, app_key is the deepface param.

    it return img and sex if exists, or None, None for face not exists,
    or Fasle, 1 for error occurs when deepface parse.
    """
    payload = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "cropface",
        "params": {
            "appkey": app_key,
            "style": {
            },
            "img": base64
        }
    }
    img, sex = (None, None)
    try:
        response = requests.post(url, data=json.dumps(
            payload), headers=json.loads('{"content-type": "application/json"}'))
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
