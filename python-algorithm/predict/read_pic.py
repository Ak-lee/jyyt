import numpy as np
import pymysql
import base64
import sql_tools
import matplotlib.pyplot as plt
import datetime
import io

conn1 = pymysql.connect(host='localhost',
                        port=3306,
                        user='root',
                        password='980825',
                        database='mileage',
                        charset='utf8',
                        autocommit=True)
cur1 = conn1.cursor()

sql = """select * from forcast_picture"""
cur1.execute(sql)
value = cur1.fetchall()
value = np.vstack(value)
for i in range(value.shape[0]):
    pic_data = base64.b64decode(value[i,1])
    file = open("./output/output_pic/tupian%s.png" % i, "wb")
    file.write(pic_data)

cur1.close()

