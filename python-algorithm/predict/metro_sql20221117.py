import numpy as np
import pymysql
import base64
import sql_tools
import torch
import tools
import argparse
import matplotlib.pyplot as plt
from models.LSTM import LSTM
import torch.nn as nn
from torch.nn import functional as F
from sklearn.preprocessing import MinMaxScaler
import datetime
import io

parser = argparse.ArgumentParser()
parser.add_argument('--lr', type=float, default=0.0001)
parser.add_argument('--n_epoch', type=int, default=10)
parser.add_argument('--split_percentage', type=float, help='训练集，测试集', default=[0.8, 0.2])
parser.add_argument('--batch_size', type=int, help='batch_size', default=5)
parser.add_argument('--slide_path', type=int, help='滑窗长度', default=1)
parser.add_argument('--time_step', type=int, help='窗口长度', default=4)
parser.add_argument('--forcast_day', type=int, help='预测天数', default=7)
parser.add_argument('--data_source', type=str, help='数据源', default=r"./dataset/里程逐增序列.npz")
parser.add_argument('--model_save_path', type=str, help='模型保存位置', default=r"./output/output_models/save_model.pth")
args = parser.parse_args()
#  连接数据库
conn1 = pymysql.connect(host='localhost',
                        port=3306,
                        user='root',
                        password='980825',
                        database='jyyt',
                        charset='utf8',
                        autocommit=True)
conn2 = pymysql.connect(host='localhost',
                        port=3306,
                        user='root',
                        password='980825',
                        database='mileage',
                        charset='utf8',
                        autocommit=True)
cur1 = conn1.cursor()
cur2 = conn2.cursor()
data_input = sql_tools.get_data('mileage_history', cur=cur1)


def evaluate(val_data, model, pred_len):
    # model.eval()
    pred_data = []
    val_data = torch.FloatTensor(val_data).reshape(1, -1)
    for j in range(pred_len):
        with torch.no_grad():
            y_pred = model(val_data)
            pred_data.append(y_pred.item())
            val_data = torch.cat((val_data[0, 1:], y_pred))
            val_data = val_data.reshape(1, -1)
    pred_data = np.asarray(pred_data).reshape(-1, 1)
    return pred_data


def pred_data(args, data):
    increase_seq = data[1:] - data[:-1]
    scaler = MinMaxScaler(feature_range=(-1, 1))  # 归一化到（-1~1）
    increase_seq = scaler.fit_transform(increase_seq.reshape(-1, 1))  # 先将增长序列归一化
    train_input_seq = tools.create_input_sequences(input_data=increase_seq, tw=args.time_step)  # 生成窗口长度为tw 预测点为1的样本
    net = LSTM(input_size=args.time_step, hidden_layer_size=64)
    loss_function = nn.MSELoss()
    optimizer = torch.optim.Adam(net.parameters(), lr=args.lr)
    epochs = args.n_epoch
    for epoch in range(epochs):
        loss_list = []
        net.train()
        net.hidden_cell = None
        for seq, labels in train_input_seq:
            optimizer.zero_grad()
            seq = torch.FloatTensor(seq).reshape(1, -1)
            labels = torch.FloatTensor(labels).reshape(-1)
            y_pred = net(seq)
            net.hidden_cell = None
            single_loss = loss_function(y_pred, labels)
            single_loss.backward()
            optimizer.step()
            loss_list.append(single_loss.item())
        loss_mean = np.mean(loss_list)
        if epoch == 0:
            torch.save(net.state_dict(), "./output/output_models/save_model.pth")
            min_mse = loss_mean
        else:
            if loss_mean < min_mse:
                torch.save(net.state_dict(), "./output/output_models/save_model.pth")
                min_mse = loss_mean
            else:
                pass
    forcast_model = LSTM(input_size=args.time_step, hidden_layer_size=64)
    forcast_model.load_state_dict(torch.load(args.model_save_path))
    forcast_data = evaluate(increase_seq[-args.time_step:], forcast_model, args.forcast_day)
    pred_inverse_data = scaler.inverse_transform(forcast_data)  # 将预测的归一化值转换为里程值
    pred_inverse_data = np.clip(pred_inverse_data, a_min=0, a_max=np.max(pred_inverse_data))  # 保证输出的增长值不小于0
    pred_inverse_data = pred_inverse_data.reshape(-1)
    pred_inverse_data = np.cumsum(pred_inverse_data)  # 累加反向求里程序列
    pred_inverse_data += data[-1]
    return pred_inverse_data, min_mse


def train(data, args):
    uct_forcast_data = []
    uct_train_mse = []
    for j in range(3):
        print("第%d次训练" % (j + 1))
        forcast_data, train_mse = pred_data(args, data)
        uct_forcast_data.append(forcast_data)
        uct_train_mse.append(train_mse)
    uct_forcast_data = np.vstack(uct_forcast_data)
    uct_train_mse = np.vstack(uct_train_mse)
    return uct_forcast_data, uct_train_mse


def plot_data(data, forcast, mse, start_date, metro_name):
    '''

    :param data: 原始数据
    :param forcast: 预测数据
    :param mse:
    :param time_scale: 传入的时间开始日期
    :param metro_name:  列车名称
    :return:
    '''
    plt.figure(1)
    plt.title(str(metro_name))

    y = np.append(data[-1], np.mean(forcast, axis=0))
    y_min = np.append(data[-1], np.min(forcast, axis=0))
    y_max = np.append(data[-1], np.max(forcast, axis=0))

    x0 = np.arange(data.shape[0])
    x1 = np.arange(data.shape[0] - 1, data.shape[0] + forcast.shape[1])

    end_date = start_date + data.shape[0] + forcast.shape[1]

    x_tick_step = (data.shape[0] + forcast.shape[1]) / 10
    x_ticks = np.arange(0, data.shape[0] + forcast.shape[1], step=int(x_tick_step))
    x_ticks_labels = np.arange(start_date, end_date, step=int(x_tick_step))  # x轴刻度
    x_ticks_labels = np.datetime_as_string(x_ticks_labels)
    plt.xticks(x_ticks, labels=x_ticks_labels, rotation=30)

    plt.plot(x0, data, color='red', label='历史数据')
    plt.plot(x1, y, color='blue', label='预测数据')
    plt.plot(x1, y_min, color='gray')
    plt.plot(x1, y_max, color='gray')
    plt.fill_between(x1, y_min, y_max, color='blue', alpha=0.2)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.xlabel('日期')
    plt.ylabel('里程（Km）')
    plt.legend()

'''    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format='png')
    my_stringIObytes.seek(0)
    my_base64_jpgData = str(base64.b64encode(my_stringIObytes.read()), "utf-8")

    sql = """insert into forcast_picture(train_id,PICTURE) values ("%s","%s")""" % (metro_name, my_base64_jpgData)
    # sql = """insert into forcast_picture(train_id,PICTURE) values ("test1","%s")""" % (my_base64_jpgData)
    cur2.execute(sql)'''


def main(args, data_input):
    # 找出最大最小时间范围
    date_scale = [np.min(data_input[:, -1]), np.max(data_input[:, -1])]
    time_scale = np.arange(date_scale[0], date_scale[1] + datetime.timedelta(days=1), dtype='datetime64')
    # 按照列车划分数据
    metro_ids = np.unique(data_input[:, 0])  # 记录所有不同的列车号
    metro_infos = []  # 记录所有列车对一个的里程和时间
    metro_dis_seq = []  # 生成对应的列车日期，里程矩阵
    metro_forcast_list = []  # 记录生成的预测数据
    for _, metro_id in enumerate(metro_ids):
        index = np.where(data_input[:, 0] == metro_id)
        metro_info = data_input[index[0], :]
        metro_dis_seq.append(tools.date_seq(time_scale, metro_info))
        metro_infos.append(metro_info)
    metro_dis_seq = np.vstack(metro_dis_seq)  # 生成按照时间逐增序列的所有列车的历史里程
    for i, seq in enumerate(metro_dis_seq):
        seq = tools.data_finetune(seq[-93:])
        uct_forcast_data, uct_train_mse = train(data=seq, args=args)
        plot_data(seq, uct_forcast_data, uct_train_mse, time_scale[-seq.shape[0]], metro_name=metro_ids[i])
        # data = base64.b64encode()
        metro_forcast_list.append(np.concatenate((uct_forcast_data, uct_train_mse), axis=1))
        pass
    pass

if __name__ == '__main__':
    main(args, data_input)
    print('end')
    cur1.close()
    cur2.close()
