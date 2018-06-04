#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import numpy as np
from dataset.mnist import load_mnist
from two_layer_net import TwoLayerNet, TwoLayerNetGradient
from optimizer import *
import matplotlib.pyplot as plt

(x_train, t_train), (x_test, t_test) = load_mnist(normalize=True,
                                                  one_hot_label=True)

train_loss_list = []
train_acc_list = []
test_acc_list = []

# ハイパーパラメータ
iters_num = 10000  # 繰り返しの回数を適宜設定
train_size = x_train.shape[0]
batch_size = 100
learning_rate = 0.1

iter_per_epoch = max(train_size / batch_size, 1)

network = TwoLayerNetGradient(input_size=784, hidden_size=50, output_size=10)
# network = TwoLayerNet(input_size=784, hidden_size=50, output_size=10)

# optimizer = SGD()
# optimizer = Momentum()
optimizer = AdaGrad()

for i in range(iters_num):
    # ミニバッチの取得
    batch_mask = np.random.choice(train_size, batch_size)
    x_batch = x_train[batch_mask]
    t_batch = t_train[batch_mask]

    # 勾配の計算
    # grads = network.numerical_gradient(x_batch, t_batch)
    grads = network.gradient(x_batch, t_batch)
    params = network.params
    # パラメータの更新
    optimizer.update(params, grads)

    """
    for key in ('W1', 'b1', 'W2', 'b2'):
        network.params[key] -= learning_rate * grads[key]"""

    # 学習経過の記錄
    loss = network.loss(x_batch, t_batch)
    print(loss)
    train_loss_list.append(loss)

    if i % iter_per_epoch == 0:
        train_acc = network.accuracy(x_train, t_train)
        test_acc = network.accuracy(x_test, t_test)
        train_acc_list.append(train_acc)
        test_acc_list.append(test_acc)
        print("train acc, test acc | " + str(train_acc) + ", " + str(test_acc))

# グラフの描画
makers = {'train': 'o', 'test': 's'}
x = np.arange(len(train_acc_list))
plt.plot(x, train_acc_list, label='train acc')
plt.plot(x, test_acc_list, label='test acc', linestyle='--')
plt.xlabel("epochs")
plt.ylabel("accracy")
plt.ylim(0, 1.0)
plt.legend(loc='lower right')
plt.show()
