#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/28 16:34
# @Author  : shursulei
# @Site    : 
# @File    : NaiveByes.py
# @Software: PyCharm

from sklearn import datasets
iris=datasets.load_iris()
print(iris.data)
print(iris.target)
from sklearn.naive_bayes import  GaussianNB #高斯贝叶分类器
clf=GaussianNB()    #设置分类器
clf.fit(iris.data,iris.target)  #训练分类器
y_pred=clf.predict(iris.data)   #预测
print(y_pred)
print("Number of mislabeled points out of a total %d points:%d"%(iris.data.shape[0],
                                                                 (iris.target!=y_pred).sum()))