#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/28 15:50
# @Author  : shursulei
# @Site    : 
# @File    : BPlearning.py
# @Software: PyCharm

import numpy as np
from numpy import random
import math
import copy
import sklearn.datasets
import matplotlib.pyplot as plt

trainingSet, trainingLables = sklearn.datasets.make_moons(400, noise=0.20)
plt.scatter(trainingSet[trainingLables == 1][:, 0], trainingSet[trainingLables == 1][:, 1], s=40, c='r', marker='x',
            cmap=plt.cm.Spectral)
plt.scatter(trainingSet[trainingLables == 0][:, 0], trainingSet[trainingLables == 0][:, 1], s=40, c='y', marker='+',
            cmap=plt.cm.Spectral)
plt.show()
