# class ClassA(object):
# 	x = 1
# 	str = "aaa"
#
# 	def __init__(self, y):
# 		self.y = y
#
# 	@classmethod
# 	def fun1(cls):
# 		cls.x = 3
#
# a = ClassA(2)
# print(a.x, a.y)
#
# b = ClassA(3)
# b.x = 2
# print(ClassA.x, a.x, b.x)
# ClassA.X = 3
# print(ClassA.x, a.x)
# ClassA.fun1()
# print(ClassA.x, a.x)
#
# print(a.str)
# ClassA.str = "bbb"
# print(b.str)

#---------------------------------------------------------
# class C1(object):
#     class_variable = 1
#
#
# class C2(object):
#     class_variable = []
#
#
# object1 = C1()
# object2 = C2()
#
# print(C1.class_variable)
# # 1
# print(object1.class_variable)
# # 1
# object1.class_variable = 20
# print(object1.class_variable)
# print(C1.class_variable)

#----------------------------------------------------------------
# class ClassA(object):
# 	x = 1
# 	str = "aaa"
#
# 	def __init__(self, yaaaaa):
# 		self.yaaaaa = yaaaaa
#
# 	@classmethod
# 	def fun1(cls):
# 		cls.x = 3
#
# class ClassB(ClassA):
# 	def __init__(self,yaaaaa,z):
# 		super().__init__(yaaaaa)
# 		self.z = z
#
# 	def fun2(self):
# 		z = self.yaaaaa
#
# b = ClassB(1,2)
# print(b.x, b.y, b.z )


# -----------------------------------------
# class ClassA:
# 	a = 1
# 	def __init__(self,a):
# 		self.a = a
#
# class ClassB(ClassA):
# 	def __init__(self):
# 		pass
#
# 	def fun1(self,a):
# 		c = self.a + a
# 		print(c)
#
# b = ClassB()
# print(b.fun1(1))


#--------------------------------------------
# def fun(str1):
#     str1 = "bbb"
#
# str = "aaaaa"
# fun(str)
# print("str is {}".format(str))

#-------------------------------------------

# file = open("mps_snesim.txt")
# line = file.readline().replace(" ", "").rstrip('\n')# q去除空格
# datas = []
# while line:
#     print(line, end = '')
#     for data in line.split('#'):
#         datas.append(data)
#     line = file.readline().replace(" ", "").rstrip('\n')
#
# print(datas)
# file.close()

#--------------------------------------------------
#
# def read_line_configuration(path, list):
#     file = open(path, 'r')
#     line = file.readline().replace(" ", "").rstrip('\n')  # q去除空格
#     while line:
#         for word in line.split('#'):
#             list.append(word)
#         line = file.readline().replace(" ", "").rstrip('\n')
#
# data = []
# read_line_configuration("mps_snesim.txt", data)
# print(data[47])
#

# -----------------------------------------------
# def load_data_from_petrel_LAS_file(filepath):
#     file = open(filepath, 'r')
#     param_list = []
#     flag = False
#     while 1:
#         lines = file.readlines(100000)
#         if not lines:
#             break
#         for line in lines:
#             print(line)
#             # if 'Ascii' in line:
#             #     flag = True
#             #     continue
#             # if flag:
#             #     line = line.replace('\n', '')
#             #     list_array = line.split(' ')
#             #     list_array = [i for i in list_array if i != '']
#             #     param_list.append(list_array)
#     file.close()
#     # print(len(param_list))
#     return param_list
#
# load_data_from_petrel_LAS_file("mps_snesim.txt")

#-----------------------------------------
# class ClassA():
#     grade = 1
#     def __init__(self, age):
#         print("运行父类的构造函数")
#         self.age = age
#
#     def setname(self):
#         self.name = "ZRH"
#
# class ClassB(ClassA):
#     def __init__(self):
#         print("运行子类的构造函数")
#
#     def getname(self):
#         return self.name
#         # return super().name
#
#     def getage(self):
#         return self.age
#
#     def getgrade(self):
#         return super().grade
#
# # python里面，要是子类构造函数没有调用父类的构造函数，
# # 那么子类将无法访问父类构造函数里的实例变量,因为实例变量不能初始化
# # 但是子类可以访问父类其他函数定义的实例变量，因为可以子类可以任意调用父类其他成员函数
# # 但是构造函数只会运行一次
#
# # 父类的实例变量可以直接用self.实例变量访问，而不能用super(）访问
# # super()可以理解为直接用父类的名字进行调用，因此只能访问父类的方法和类变量
# b = ClassB()
# b.setname()
# print(b.getname())
# # print(b.getage())
# print(b.getgrade())
#-------------------------------------------------------------------
# import random
#
# random.seed(1)
# for i in range(1, 10):
#     print(int(random.randint(1, 100)))

# ----------------------------------------------------------------
# str1 = "ti/ti_cb_4x4_40_\\40_1.dat"
# # str2 = "/"
#
# def find_last(search, target):
#     # Find the first occurrence of target
#     pos = search.find(target)
#
#     # If you found something, keep looking for it until you don't
#     # find it again
#     while pos >= 0:
#         # You found target once; now look for the next occurrence
#         next_pos = search.find(target, pos + 1)
#         if next_pos == -1:
#             # no more targets, so stop looking
#             break
#         pos = next_pos
#     return pos
#
# found1 = find_last(str1, "/")
# found2 = find_last(str1, "\\")
# found = found1 if found1 > found2 else found2
#
# output_filename = "./" + str1[found + 1:]
# print(output_filename)
# ---------------------
# class ClassA():
#     def __init__(self, a):
#         self.a = a
#
#     def fun(self):
#         self.b = 1
#
#
# a = ClassA(2)
# a.fun()
# print(a.b)

# ------------------
# def fun(a):
#     a = 2
#
# # list = [1,2]
# # fun(list)
# a = 1
# fun(a)
# print(a)

#---------------------------------------
# class ClassA():
#     def __init__(self):
#         print("运行父类的构造函数")
#         self.age = 1  # 实例变量
#
# class ClassB(ClassA):
#     # 1 子类重写父类构造函数，但 显式调用父类构造函数
#     def __init__(self):
#         print("运行子类的构造函数")
#         super().__init__()
#     #
#     # 2 子类重写父类构造函数，但 不显式调用父类构造函数
#     # def __init__(self):
#     #     print("运行子类的构造函数")
#
#     # 3
#     # 啥都不写，自动调用父类构造函数
#
#     def fun(self):
#         print(self.age)
#
# b = ClassB()
# b.fun()

#--------------------------
# for i in range(10, -1, -1):
#     print(i)

#------------------------------
# from abc import ABC, abstractmethod
#
#
# class Base(ABC):
#
#
#     def __init__(self):
#         pass
#
#     @abstractmethod
#     def get(self):
#         print("Base.get()")
#
#
#
# class Derive1(Base):
#     pass
#     # def get(self):
#     #     print("Derive1.get()")
#
#
# class Derive2(Derive1):
#     def get(self):
#         print("Derive2.get()")
#
#
# if __name__ == '__main__':
#     b = Derive2()
#     b.get()

# ---------------------------------
import functools
#
# list = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
# list2 = list
# list2.append(25)
# print(list)
# list.sort(key=functools.cmp_to_key())
# from random import *
#
# random_direction = randint(0, 5)
# print(random_direction)
# import numpy as np
#
#
# def fun(list):
#     list = np.full((3, 3), 3)
#     print(list)
#
# list1 = []
# fun(list1)
# print(list1)
#----------------------------
# list1 = [1, 2, 3]
# list2 = []
# list2 = list1
# list1.append(4)
# print(list2)
# --------------------
# list1 = [1,2]
# list2 = [3,4]
# list1.append(list2)
# print(list1)
#--------------------------
str=' '.join(line.split())