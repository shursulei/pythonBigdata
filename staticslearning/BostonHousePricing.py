#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/28 11:59
# @Author  : shursulei
# @Site    : 
# @File    : BostonHousePricing.py
# @Software: PyCharm

import numpy as np
from  sklearn.datasets import load_boston
from  sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

boston=load_boston()
# print(boston.keys())
# print(boston.feature_names)
# print(boston.DESCR)
print(np.newaxis)
x=boston.data[:,np.newaxis,5]
y=boston.target
lm=LinearRegression()
lm.fit(x,y)
print("方程的确定系数(R^2):%.2f" %lm.score(x,y))
plt.scatter(x,y,color='green') #显示数据点
plt.plot(x,lm.predict(x),color='blue',linewidth=3)#画出回归曲线
plt.xlabel('Average Number of Rooms per Dwelling(RM)')
plt.ylabel('Housing Price')
plt.title('2D Demo of Liner Regression')
plt.show()