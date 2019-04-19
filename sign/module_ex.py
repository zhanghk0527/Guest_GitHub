# -*- coding：utf-8 -*-
'''
Auther: Zhang
Date: 2019-04-19
Describe: 实现计算器基础运算：加、减、乘、除
'''

# 定义类：Calculator
class Calculator():
    # 初始化变量 a 和 b
    def __init__(self,a,b):
        self.a = int(a)
        self.b = int(b)

    def add(self):
        return self.a + self.b

    def sub(self):
        return self.a - self.b

    def mul(self):
        return self.a * self.b

    def div(self):
        return self.a / self.b