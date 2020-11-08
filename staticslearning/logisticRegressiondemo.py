#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/28 13:42
# @Author  : shursulei
# @Site    : 
# @File    : logisticRegressiondemo.py
# @Software: PyCharm

from math import exp
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

class LogisticReressionClassifier:
    def __init__(self, max_iter=5000, learning_rate=0.01):
        self.max_iter = max_iter
        self.learning_rate = learning_rate

    def sigmoid(self, x):
        return 1 / (1 + exp(-x))

    def data_matrix(self, X):
        data_mat = []
        for d in X:
            data_mat.append([1.0, *d])
        return data_mat

    def fit(self, X, y):
        # label = np.mat(y)
        data_mat = self.data_matrix(X)  # m*n
        self.weights = np.ones((len(data_mat[0]), 1), dtype=np.float32)
        for j in range(self.max_iter):
            for iter_ in range(len(self.weights)):
                error = 0
                for i in range(len(X)):
                    result = self.sigmoid(np.dot(data_mat[i], self.weights))
                    error += (result - y[i]) * data_mat[i][iter_]
                self.weights[iter_] = self.weights[iter_] - self.learning_rate * 1 / len(X) * error
        print('LogisticRegression Model(learning_rate={},max_iter={})'.format(
            self.learning_rate, self.max_iter))

    # def f(self, x):
    #     return -(self.weights[0] + self.weights[1] * x) / self.weights[2]

    def score(self, X_test, y_test):
        right = 0
        X_test = self.data_matrix(X_test)
        for x, y in zip(X_test, y_test):
            result = np.dot(x, self.weights)
            if (result > 0 and y == 1) or (result < 0 and y == 0):
                right += 1
        return right / len(X_test)


if __name__ == '__main__':

    # data
    def create_data():
        iris = load_iris()
        # print(iris)
        df = pd.DataFrame(iris.data, columns=iris.feature_names)
        df['label'] = iris.target
        df.columns = ['sepal length', 'sepal width', 'petal length', 'petal width', 'label']
        print(df)
        data = np.array(df.iloc[:100, [0, 1, -1]])
        # print(data)
        return data[:, :2], data[:, -1]

    X, y = create_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    lr_clf = LogisticReressionClassifier()
    lr_clf.fit(X_train, y_train)
    print(lr_clf.score(X_test, y_test))
    x_ponits = np.arange(4, 8)
    y_ = -(lr_clf.weights[1] * x_ponits + lr_clf.weights[0]) / lr_clf.weights[2]
    plt.plot(x_ponits, y_)

    # lr_clf.show_graph()
    plt.scatter(X[:50, 0], X[:50, 1], label='0')
    plt.scatter(X[50:, 0], X[50:, 1], label='1')
    plt.legend()
    plt.show()
