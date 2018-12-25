#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
author ziling

'''
import os
import json


def io_base():
    '''
for computer, keyboard is the base input.
screen is the base out put
    '''
    print("base out put")
    name = input("input your name: ")
    print(name)


def file_io(path):
    if not path:
        return
# check file is exist or not
    if os.path.exists(path):
        print(path, "is exist")
# write file
    f = open(path, "w")
    f.write("ziling\ntest")
    f.close()
# read file
    f = open(path, "r")
    str = f.read()
    print(str)
    f.close()

    print('### ---- read file line')
    f = open(path, 'r')
    for line in f:
        print(line)
    f.close()


def json_operate():
    '''
dumps(str)
loads(str)

dump(file)
load(file)
    '''
    array = [1, 'simple', 'list']
    str1 = json.dumps(array)
    print(str1)
    f = open('json.text', 'w')
    json.dump(array, f)
    f.close()

    print(json.loads(str1))


def main():
    # io_base()
    # file_io("file.io")
    json_operate()


if __name__ == "__main__":
    main()
