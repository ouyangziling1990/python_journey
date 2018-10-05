# -*- coding: utf-8 -*-
import mysql.connector
import math

conn = mysql.connector.connect(user='root', password='123456', database='zilingRepo')
cursor = conn.cursor()
cursor.execute('select * from test')
value = cursor.fetchall()
cursor.close()
conn.close()
print(value)

def quadratic(a, b, c):
    if 2*b-4*a*c<0:
        return 
    else:
        x1 = (-b+math.sqrt(b*b-4*a*c))/(2*a)
        x2 = (-b-math.sqrt(b*b-4*a*c))/(2*a)
        return x1, x2

res = quadratic(1,2,1)
print(res)


