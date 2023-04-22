import numpy as np
import sql_tools
import matplotlib.pyplot as plt
import tools
import pymysql
import datetime

time_step = 5  # 时间窗口
conn = pymysql.connect(host='59.110.224.8',
                       port=3306,
                       user='sunbo',
                       password='sunbo123456',
                       database='jyyt',
                       charset='utf8',
                       autocommit=True)
cur = conn.cursor()
data_input = sql_tools.get_data('mileage_history', cur=cur)


def main(data_input, train_id, forcast_date):
    forcast_date = datetime.datetime.strptime(forcast_date, '%Y-%m-%d').date()  # 记录需要预测的最后一个日期，用于计算时间跨度
    date_scale = [np.min(data_input[:, -1]), np.max(data_input[:, -1])]  # 找出所有记录的时间跨度
    time_scale = np.arange(date_scale[0], date_scale[1] + datetime.timedelta(days=1), dtype='datetime64')  # 生成时间坐标
    # 索引对应的列车及其历史里程
    data_idx = np.where(data_input[:, 0] == train_id)
    data = data_input[data_idx[0], :]
    metro_dis_seq = tools.date_seq(time_scale, data)
    metro_dis_seq = tools.single_metro_data_interpolation(metro_dis_seq, time_scale)
    time_step = forcast_date - date_scale[-1]
    forcast_data = forcast_year_data(metro_dis_seq, time_step=time_step.days + 1)

    return forcast_data


def forcast_year_data(data, time_step=1):
    #  生成对应时间段个数的权重
    tw = data.shape[-1] // time_step
    wi = np.arange(1, tw + 1)
    wi = wi / wi.sum()
    wi = wi.reshape(-1, 1)
    increase_year = []  # 记录365天过去里程的增长数据规律
    # 计算每一个时间段中的里程增长数据
    for j in range(tw):
        start_id = data.shape[0] - ((j + 1) * time_step)
        seq = data[start_id:start_id + time_step]
        increase_data = seq[1:] - seq[:-1]
        increase_year.append(increase_data)
    increase_year = np.vstack(increase_year)
    increase_year = np.sum((increase_year * wi), axis=0)  # 里程增长乘以相应的权重
    # 计算预测的时间段中的里程增长数据
    forcast_data = tools.accumulation_sum(data[-1], increase_year)
    return forcast_data


def predict_generate(train_id, deadline):
    print("get predict call,,,,")

    # data_input = sql_tools.get_data('mileage_history', cur=cur)
    # main(data_input, train_id, deadline)
