import torch
import torch.nn as nn
import torch.nn.functional as F


class BiLSTM(nn.Module):

    def __init__(self, input_size, hidden_size, output_size):
        super(BiLSTM, self).__init__()
        self.rnn = nn.LSTM(input_size, hidden_size, bidirectional=True, batch_first=True)
        self.linear = nn.Linear(hidden_size * 2, output_size)

    def forward(self, input):
        """
        input : visual feature [batch_size x T x input_size]
        output : contextual feature [batch_size x T x output_size]
        """
        self.rnn.flatten_parameters()
        recurrent, _ = self.rnn(input)  # batch_size x T x input_size -> batch_size x T x (2*hidden_size)
        output = self.linear(recurrent)  # batch_size x T x output_size
        return output


class LSTM(nn.Module):
    def __init__(self, input_size=7, hidden_layer_size=100, output_size=1):
        super().__init__()
        self.hidden_layer_size = hidden_layer_size

        self.lstm = nn.LSTM(input_size, hidden_layer_size, batch_first=False)

        self.linear = nn.Linear(hidden_layer_size, output_size)

        self.hidden_cell = (torch.zeros(1, 1, self.hidden_layer_size),
                            torch.zeros(1, 1, self.hidden_layer_size))
        self.activation = torch.nn.ReLU()
        self.dropout = nn.Dropout(p=0.1)
        # self.activation = torch.nn.Tanh()
        # self.activation = torch.nn.LeakyReLU()

    def forward(self, input_seq):
        lstm_out, self.hidden_cell = self.lstm(input_seq.view(len(input_seq), 1, -1), self.hidden_cell)
        lstm_out = self.activation(lstm_out)
        lstm_out = self.dropout(lstm_out)
        predictions = self.linear(lstm_out.view(len(input_seq), -1))
        return predictions[-1]


class BatchLSTM(nn.Module):
    def __init__(self, input_size=7, hidden_layer_size=100, output_size=1):
        super().__init__()
        self.hidden_layer_size = hidden_layer_size

        self.lstm = nn.LSTM(input_size, hidden_layer_size, batch_first=True, num_layers=2)

        self.linear = nn.Linear(hidden_layer_size, output_size)

        self.hidden_cell = (torch.zeros(1, 1, self.hidden_layer_size),
                            torch.zeros(1, 1, self.hidden_layer_size))
        self.activation = torch.nn.ReLU()
        self.dropout = nn.Dropout(p=0.2)
        # self.activation = torch.nn.Tanh()
        # self.activation = torch.nn.LeakyReLU()

    def forward(self, input_seq):
        lstm_out, self.hidden_cell = self.lstm(input_seq, self.hidden_cell)
        lstm_out = self.activation(lstm_out)
        lstm_out = self.dropout(lstm_out)
        predictions = self.linear(lstm_out.view(len(input_seq), -1))
        return predictions


class Net(nn.Module):
    def __init__(self, input_size=7, hidden_size=100):
        super(Net, self).__init__()
        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size, num_layers=3, batch_first=True)
        self.fc = nn.Linear(in_features=hidden_size, out_features=1)

    def forward(self, x):
        x, _ = self.lstm(x)
        # x = x[:, -1, :]
        x = self.fc(x)
        x = x.view(1)
        return x


class LstmNet(nn.Module):
    """
    pytorch预测模型，包括LSTM时序预测层和Linear回归输出层
    可以根据自己的情况增加模型结构
    """

    def __init__(self, input_size, hidden_size, num_layers):
        super(LstmNet, self).__init__()
        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size,
                            num_layers=num_layers, batch_first=True,
                            bidirectional=False)
        # self.naiveLSTM = NaiveCustomLSTM(input_sz=config.n_features, hidden_sz=config.hidden_size)
        self.activation = torch.nn.LeakyReLU()
        self.linear_out = nn.Linear(in_features=hidden_size, out_features=1)
        self.dropout = nn.Dropout(p=0.2)

    def forward(self, x, hidden=None):
        lstm_out, hidden = self.lstm(x, hidden)
        lstm_out = self.activation(lstm_out)
        lstm_out = self.dropout(lstm_out)
        linear_out = self.linear_out(lstm_out.reshape(len(x), -1))
        return linear_out[-1], hidden

class Classifier(nn.Module):
    def __init__(self, vocabsize, out_dim, embedding_dim=300, hidden_dim=128,
                n_layers=2, bidirectional=False, dropout=float(0.1), pad_inx=None):
        super().__init__()

        # embedding层
        self.embedding = nn.Embedding(vocabsize, embedding_dim, padding_idx=pad_inx)

        # lstm层
        self.lstm = nn.LSTM(
            embedding_dim,
            hidden_dim,
            num_layers = n_layers,
            bidirectional = bidirectional,
            dropout=dropout
        )

        # 全连接层
        num_direction = 2 if bidirectional else 1   # 双向&单向可选
        self.fc = nn.Linear(hidden_dim * n_layers * num_direction, out_dim)
        # 丢弃概率
        self.dropout = nn.Dropout(p=dropout)

    def forward(self, text, text_len):

        embedded = self.embedding(text)
        packed_embedded = nn.utils.rnn.pack_padded_sequence(embedded, text_len)
        packed_output, (h_n, c_n) = self.lstm(packed_embedded)
        h_n = self.dropout(h_n)
        h_n = torch.transpose(h_n, 0, 1).contiguous()
        h_n = h_n.view(h_n.shape[0], -1)
        loggits = self.fc(h_n)

        return loggits