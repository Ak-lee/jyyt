import numpy as np
import sql_tools
import matplotlib.pyplot as plt
import tools
import pymysql
import datetime
from scipy.interpolate import interp1d

time_step = 5  # 时间窗口
conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       password='980825',
                       database='mileage',
                       charset='utf8',
                       autocommit=True)
cur = conn.cursor()
data = sql_tools.get_data('mileage_history', cur=cur)


# 找出最大最小时间范围
def time_increase_seq(data_input):
    '''
    :param data_input:所有输入的数据，所有列车在所有天数的里程数（nx3）{列车号，里程值，日期}
    :return:metro_dis_seq列车的里程和日期对应数据，横轴为日期连续坐标，纵轴为不同列车,
            time_scale为上表的日期连续坐标
    '''
    date_scale = [np.min(data_input[:, -1]), np.max(data_input[:, -1])]
    time_scale = np.arange(date_scale[0], date_scale[1] + datetime.timedelta(days=1), dtype='datetime64')
    # 按照列车划分数据
    metro_ids = np.unique(data_input[:, 0])  # 记录所有不同的列车号
    metro_infos = []  # 记录所有列车对一个的里程和时间
    metro_dis_seq = []  # 生成对应的列车日期，里程矩阵
    for _, metro_id in enumerate(metro_ids):
        index = np.where(data_input[:, 0] == metro_id)
        metro_info = data_input[index[0], :]
        metro_dis_seq.append(tools.date_seq(time_scale, metro_info))
        metro_infos.append(metro_info)
    metro_dis_seq = np.vstack(metro_dis_seq)  # 生成按照时间逐增序列的所有列车的历史里程
    return metro_dis_seq, time_scale





def main(data):
    metro_dis_seq, time_scale = time_increase_seq(data)
    metro_dis_fined, _, _ = tools.creat_data_interpolation(metro_dis_seq)
    return metro_dis_fined.astype(int)


if __name__ == '__main__':
    a = main(data)
    cur.close()
