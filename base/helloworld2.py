# -*- coding: utf-8 -*-


def traverse():
    '''
    traverse function
    '''
    for i in range(10):
        print("loop:", i)


def age_game():
    while True:
        my_age = 28
        user_input = int(input("input your guess num: "))
        if user_input == my_age:
            print("congratulations, you got it")
        elif user_input < my_age:
            print('Oop, think bigger')
        else:
            print("think smaller")


def generater():
    a = []
    for i in range(10):
        a.append(i)
    b = [i + 1 for i in range(10)]
    print(b)
    g = (x * x for x in range(10))
    print(g)
    for i in g:
        print(i)
    pass


def main():
    generater()


if __name__ == "__main__":
    main()
