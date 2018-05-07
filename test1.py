import matplotlib.pyplot as plt
import numpy as np


def f1(x1):
    return 6-2*x1
def f2(x1):
    return 4-(4/5)*x1

def f3(x1,b):
    return -x1+b



x1 = np.arange(0, 5, 0.1)


x2z1 = f1(x1)
x2z2 = f2(x1)

plt.figure()
plt.plot(x1, x2z1, color = 'red', linewidth = 1, linestyle = '-')
plt.plot(x1, x2z2, color = 'blue', linewidth = 1, linestyle = '-')
for i in range(5):
    plt.plot(x1, f3(x1,i), color = 'black', linewidth = 1, linestyle = '-')

plt.plot(x1, f3(x1,126/30), color = 'y', linewidth = 1, linestyle = '-')
plt.plot(x1, f3(x1,(109/26)), color = 'black', linewidth = 1, linestyle = '-')

plt.grid(True, linestyle = "-", color = "g", linewidth = "1")

# 设置坐标轴的取值范围
plt.xlim((0,5))
plt.ylim((0,5))

# 设置坐标轴的lable
plt.xlabel('X1 axis')
plt.ylabel('X2 axis')

my_x_ticks = np.arange(0, 5, 0.5)
my_y_ticks = np.arange(0, 5, 0.5)
plt.xticks(my_x_ticks)
plt.yticks(my_y_ticks)

plt.show()
