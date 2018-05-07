from sympy import *

def f(x3,x4):
    return -5*x3-5*x4
def f2(x5):
    return -26/30 * x5

init_printing(use_unicode=True)
x1,x2 = symbols("x1 x2")

x3 = 6 - (2*x1+x2)
x4 = 20-(4*x1+5*x2)
x5 = -4 - f(x3,x4)
print(f2(x5))
