#-*- coding:utf-8 -*-

import numpy as np
import pandas as pd
from pandas import Series, DataFrame

obj = Series([1, 3, 5, 7], index=['a', 'b', 'c', 'd'])
print(obj)

a=obj.values
b=obj.index

a = np.empty([2, 2])
# array([[-9.74499359e+001, 6.69583040e-309], [2.13182611e-314, 3.06959433e-309]])  # random
b = np.empty([2, 2], dtype=int)
# array([[-1073741821, -1067949133], [496041986, 19249760]])  # random
print(a)
print(b)


