import numpy as np
import pandas as pd
import torch
from sklearn.preprocessing import MinMaxScaler


# 按照递增序列填充对应日期数据
def date_seq(date_scale, data):
    # 去除重复日期的记录，以第一次出现为准
    _, index_date = np.unique(data[:, -1], return_index=True)  # 找出第一次出现的日期id
    data = data[index_date, :]
    distance = np.zeros(date_scale.shape[0])
    for i, x in enumerate(data[:, -1]):
        idx = np.where(date_scale == x)
        distance[idx[0]] = data[i, 1]

    return distance


def data_finetune(data):
    '''
    使用插值方法对数据缺省值进行补充,内插法，如果在两端有数据为0，则将复制两端的最近的数据
    :param data: 1维
    :return: 1维的序列
    https://blog.csdn.net/hfutdog/article/details/87386901
    '''
    # data
    lack_id = np.where(data == 0)[0]  # 记录数据为0的坐标
    id = np.asarray(range(data.shape[0]))  # 形成x坐标
    x = np.delete(id, lack_id)  # 删除缺省值的坐标
    y = np.delete(data, lack_id)  # 删除缺省值的数据（0）
    y_data = np.interp(lack_id, x, y)  # 插值
    data[lack_id] = y_data
    data = np.sort(data)
    return data


def data_increase_seq(data):
    '''
    将逐增序列变为增量序列
    :param data: 1D
    :return: 1D
    '''
    data1 = data[1:]
    data1 = data1 - data[:-1]
    return data1


def data_split(rate, data):
    train_idx = int(data.shape[0] * rate[0]) + 1  # 计算训练集的个数用于划分数据集
    train_data = data[:train_idx, :]
    test_data = data[train_idx:, :]
    return train_data, test_data


def data_split2(rate, data):
    train_idx = int(data.shape[0] * rate[0]) + 1  # 计算训练集的个数用于划分数据集
    val_idx = int(data.shape[0] * rate[1])  # 计算验证集的个数用于划分数据集
    train_data = data[:train_idx]
    val_data = data[train_idx:train_idx + val_idx]
    test_data = data[train_idx + val_idx:]
    return train_data, val_data, test_data


class TrainDataset(torch.utils.data.Dataset):
    def __init__(self, train=True, train_data=None, train_label=None):
        self.train = train
        self.train_data = train_data
        self.train_label = train_label

    def __getitem__(self, index):
        img, label = self.train_data[index], self.train_label[index]
        return img, label, index

    def __len__(self):
        return len(self.train_data)


class TestDataset(torch.utils.data.Dataset):
    def __init__(self, test_data=None, test_label=None):
        self.test_data = test_data
        self.test_label = test_label

    def __getitem__(self, index):
        img, label = self.test_data[index], self.test_label[index]
        return img, label, index

    def __len__(self):
        return len(self.test_data)


def create_input_sequences_batch(input_data, tw):
    # input_data (-1,1) 批量形式
    inout_seq = []
    labels = []
    L = len(input_data)
    for i in range(L - tw):
        train_seq = input_data[i:i + tw, 0]
        train_label = input_data[i + tw:i + tw + 1, 0]
        inout_seq.append(train_seq)
        labels.append(train_label)
    return np.vstack(inout_seq), np.vstack(labels)


# 生成序列样本
def create_input_sequences(input_data, tw):
    inout_seq = []
    L = len(input_data)
    for i in range(L - tw):
        train_seq = input_data[i:i + tw]
        train_label = input_data[i + tw:i + tw + 1]
        inout_seq.append((train_seq, train_label))
    return inout_seq


def weight_moving_average(data, tw):
    wi = np.arange(1, tw + 1)
    wi = wi / wi.sum()
    i = 0
    rolling_data = []
    while i + tw <= data.shape[0]:
        w_data = wi * data[i: i + tw]
        rolling_data.append(w_data.sum())
        i += 1
    rolling_data = np.hstack(rolling_data)
    return rolling_data


# 计算MAE
def compute_mae(org_data, data):
    out = org_data - data
    out = np.abs(out)
    return out.mean()


# 计算MSE
def compute_mse(org_data, data):
    out = org_data - data
    out = out * out
    return out.mean()


# 计算MED
def compute_mad(org_data, data):
    out = org_data - data
    out = np.abs(out)
    return np.median(out)


# 按照后面序列的增长规则，往前推前面的数据
def data_fill(metro_dis_seq):
    temp = []
    for i, seq in enumerate(metro_dis_seq):
        idx = np.where(seq != 0)
        temp.append(idx[0][0])
    min_idx = np.max(temp)  # 找出所有列车有数据的最早的日期
    temp = []
    for i, seq in enumerate(metro_dis_seq):
        seqed = seq[min_idx:]
        seqed = data_finetune(seqed)
        temp.append(seqed)
    temp = np.vstack(temp)
    slope = (temp[:, 0] - temp[:, -1]) / temp.shape[1]
    for i in range(metro_dis_seq.shape[1] - temp.shape[1]):
        temp = np.concatenate(((slope + temp[:, 0]).reshape(-1, 1), temp), axis=1)
    temp = temp[:, 380:]
    for i in range(temp.shape[0]):
        if temp[i, 0] < 0:
            idx = np.where(temp[i, :] > 0)
            idx = idx[0][0]
            data = np.linspace(0, temp[i, idx + 1], idx)
            temp[i, :idx] = data
    return temp


def single_metro_data_interpolation(data, time_scale):
    '''
    :param data: 单辆列车的里程数据
    :param time_scale: 此列车的时间坐标
    :return:
    '''
    lack_id = np.where(data <= 0)[0]  # 记录数据小于等于0的坐标
    unlack_id = np.where(data != 0)[0]  # 记录数据正常的时间坐标
    if lack_id.size != 0:
        if lack_id[0] == 0:
            lack_id = np.delete(lack_id, 0)
        #  处理最后一个值缺少的数据
        if lack_id[-1] + 1 == data.shape[0]:
            data[-1] = (data[unlack_id[-1]] - data[unlack_id[-2]]) / (unlack_id[-1] - unlack_id[-2]) * (
                    lack_id[-1] - unlack_id[-1]) + data[unlack_id[-1]]
            lack_id = np.delete(lack_id, -1)
        id = np.asarray(range(data.shape[0]))  # 形成x坐标
        x = np.delete(id, lack_id)  # 删除缺省值的坐标
        y = np.delete(data, lack_id)  # 删除缺省值的数据（0）
        y_data = np.interp(lack_id, x, y)  # 插值
        data[lack_id] = y_data
        out = np.sort(data)
    return out


def creat_data_interpolation(data_seq):
    '''
    用于通过插值方法生成缺少的数据
    :param data_seq: 输入需要插值的序列，按照每一行为一个列车，每一列为连续日期
    :return: out_data修改完成的数据,out_id，缺少的id的列表
    '''
    out_data = []
    out_lack_id = []
    out_wrong_id = []
    for i in range(data_seq.shape[0]):
        data = data_seq[i, :]
        lack_id = np.where(data <= 0)[0]  # 记录数据为0的坐标
        out_lack_id.append(lack_id)  # 记录原始缺少数据的id和小于0的数据的id
        unlack_id = np.where(data != 0)[0]
        # 判断里程值倒增长
        unlack_data = data[unlack_id]
        ngt = unlack_data[1:] - unlack_data[:-1]
        ngt_id = np.where(ngt < 0)[0]
        if ngt_id.size != 0:  # 如果有倒增长序列
            print('有倒增长序列')
            print(ngt_id.size)
            ngt_id += 1
            data[unlack_id[ngt_id]] = 0  # 将倒增长的数据处理为缺失
            out_wrong_id.append([i, unlack_id[ngt_id]])
            lack_id = np.where(data <= 0)[0]

        else:
            print('序列正常增长')
            print(ngt_id.size)

        # 删除第一个日期就缺少的id
        if lack_id[0] == 0:
            lack_id = np.delete(lack_id, 0)
        #  处理最后一个值缺少的数据
        if lack_id[-1] + 1 == data.shape[0]:
            data[-1] = (data[unlack_id[-1]] - data[unlack_id[-2]]) / (unlack_id[-1] - unlack_id[-2]) * (
                    lack_id[-1] - unlack_id[-1]) + data[unlack_id[-1]]
            lack_id = np.delete(lack_id, -1)
        id = np.asarray(range(data.shape[0]))  # 形成x坐标
        x = np.delete(id, lack_id)  # 删除缺省值的坐标
        y = np.delete(data, lack_id)  # 删除缺省值的数据（0）
        y_data = np.interp(lack_id, x, y)  # 插值
        data[lack_id] = y_data
        data = np.sort(data)
        out_data.append(data)
        # plt.plot(data, 'red')
        # plt.scatter(unlack_id, data[unlack_id])
        # plt.show()
    return np.vstack(out_data), out_lack_id, out_wrong_id


def accumulation_sum(data, increase_data):
    '''
    用于将里程增量转为里程值
    :param data: 最后一个里程值
    :param increase_data: 增量序列
    :return:
    '''
    increase_data = np.clip(increase_data, a_min=0, a_max=np.max(increase_data))  # 保证输出的增长值不小于0
    increase_data = increase_data.reshape(-1)
    increase_data = np.cumsum(increase_data)  # 累加反向求里程序列
    increase_data += data
    return increase_data
