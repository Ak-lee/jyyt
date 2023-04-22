import numpy as np
import sql_tools
import matplotlib.pyplot as plt
import tools
import pymysql
import datetime

time_step = 5  # 时间窗口
conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       password='980825',
                       database='mileage',
                       charset='utf8',
                       autocommit=True)
cur = conn.cursor()
data_input = sql_tools.get_data('mileage_history', cur=cur)


def main(data):
    data_input = data
    date_scale = [np.min(data_input[:, -1]), np.max(data_input[:, -1])]  # 找出所有记录的时间跨度
    time_scale = np.arange(date_scale[0], date_scale[1] + datetime.timedelta(days=1), dtype='datetime64')  # 生成时间坐标
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
    metro_dis_seq = tools.data_fill(metro_dis_seq)
    forcast_data = forcast_year_data(metro_dis_seq, time_step=30)

    pass

def forcast_year_data(data, time_step=1):
    forcast_data = []
    for i in range(data.shape[0]):
        data_seq = data[i, :]
        tw = data_seq.shape[-1] // time_step
        wi = np.arange(1, tw)
        wi = wi / wi.sum()
        wi = wi.reshape(-1, 1)
        increase_year = []  # 记录365天过去里程的增长数据
        for j in range(tw - 1):
            start_id = j * time_step
            end_id = (j + 1) * time_step
            increase_data = data_seq[end_id:end_id + time_step] - data_seq[start_id:start_id + time_step]
            increase_year.append(increase_data)
        increase_year = np.vstack(increase_year)
        increase_year = np.sum((increase_year * wi), axis=0)
        forcast_data.append(increase_year + data_seq[-increase_year.shape[0]:])
    return np.vstack(forcast_data)
    pass


def plot_data(data, forcast, tw, date_seq):
    plt.figure()
    plt.title('列车里程同期对比增长（年）')

    plt.plot(data, color='red', label='真实数据')
    x1 = range(tw + 1, data.shape[0] + 1, 1)
    plt.plot(x1, forcast, color='blue', label='预测数据')
    x_ticks = range(0, x1.stop, 5)

    x_ticks_labels = np.arange(date_seq[0], date_seq[-1] + 1, 5)
    x_ticks_labels = np.datetime_as_string(x_ticks_labels)

    plt.xticks(x_ticks, labels=x_ticks_labels, rotation=30)
    plt.rcParams['font.sans-serif'] = ['SimHei']

    plt.xlabel('日期')
    plt.ylabel('里程（Km）')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main(data_input)
