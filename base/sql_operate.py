# -*- coding: utf-8 -*-
import MySQLdb
conn = MySQLdb.connect(
    host='192.168.1.172',
    user='root', password='123456', database='zilingRepo')
cursor = conn.cursor()
cursor.execute("select * \
 from polls_choice")
results = cursor.fetchall()
cursor.close()
conn.close()
for row in results:
    print(row)
