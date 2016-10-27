# !/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "BarRui"

print('The quick brown fox', 'jumps over', 'the lazy dog')
print(100 + 200)
print('100 + 200 =', 100 + 200)
# name = input()
name = 'abdata'
print(name)
print('hello,', name)
# name = input('please enter your name: ')
print('hello,', name)


# print absolute value of an integer:
a = -100

if a >= 0:
    print(a)
else:
    print(-a)

print("I'm OK!")
print('I\'m \"OK\"!')

print('\\\t\\')

print('''line1
... line2
... line3''')


n = 123
f = 456.789
s1 = 'Hello, world'
s2 = 'Hello, \'Adam\''
s3 = r'Hello, "Bart"'
s4 = r'''Hello,
Lisa!'''
print(s4)

s1 = 72
s2 = 85
r = (s2-s1)/s1*100
print('小明成绩提高了%.2s%%' % r)

classmates = ['Michael', 'Bob', 'Tracy']
print(classmates)
len(classmates)

age = 12
if age >= 18:
    print('adult')
else:
    print('teenager')



age = 33
if age >= 18:
    print('your age is', age)
    print('adult')
else:
    print('your age is', age)
    print('teenager')


age = 3
if age >= 18:
    print('adult')
elif age >= 6:
    print('teenager')
else:
    print('kid')



age = 20
if age >= 6:
    print('teenager')
elif age >= 18:
    print('adult')
else:
    print('kid')


if '1':
    print('True')

if '':
    print('True')


s = input('birth: ')
birth = int(s)
if birth < 2000:
    print('00前')
else:
    print('00后')









