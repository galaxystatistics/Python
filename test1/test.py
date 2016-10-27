

# -*- coding:utf-8 -*-
# bupt_absinth

# 类名中的每个单词的首字母大写，其它小写
# 私有属性前必须使用两个下划线为前缀
# self相关于Java语言中的this关键字，表示本类
# 方法名的首字母小写，其后每个单词的首字母要大写
# 对象名用小写字母
# 函数名首字母小写，后面每个单词的首字母大写

# pip install 包名称




import random

def equalseNum(num):
    if(num==6):
        print(1)
    else:
        print(0)

num=random.randrange(1,9)
print('num = '+str(num))
print(equalseNum(num))

# TODO
class MyClass:
    __username=""
    def __init__(self,username):
        self.__username=username
    def getUserName(self):
        return self.__username

        #    myclass=MyClass('abdata')
#if __name__=="__main__":
#    print(myclass.getUserName())



position = 0
walk = [position]
steps = 1000
for i in xrange(steps):
step = 1 if random.randint(0, 1) else -1
position += step
walk.append(position)