
# insert into table(id,name) values(0,'张三');
#
# sql = """select * from mileage_history"""
# sql = """DROP TABLE IF EXISTS forcast_picture"""# 新建表格
# sql = """create table forcast_picture (train_id char(20) not null,PICTURE  mediumblob)"""# 查询创建新表
# sql = """create table mileage_test_input (train_id char(20) not null,last_name  char(20))""" # 创建新表中的元素
# sql = """insert into forcast_picture values ('CD17025','data')""" # 插入数据


# pic_path = r"D:\04项目\01-20220329 列车检运一体化反馈材料\07_检运一体化项目进展及案例20221026\预测里程图片.jpg"
# sql = """select * from fost_picture"""
# pic = open(pic_path, "rb")
# data = base64.b64encode(pic.read())
# sql = """insert into forcast_picture(train_id,PICTURE) values ('CD17022',"%s")""" % (str(data))  # 插入图片的base64数据
# sql = """select * from fost_picture"""
# value = cur.fetchall()  # 获取 所有数据
import numpy as np


def get_data(list_name, cur):
    sql = """select * from %s""" % list_name
    cur.execute(sql)
    value = cur.fetchall()  # 获取 所有数据
    return np.vstack(value)