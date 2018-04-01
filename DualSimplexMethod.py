import numpy as np
from SimplexAlgorithm import QTable
from SimplexAlgorithm import AConv

#求sigma与vt的倒数的非向量乘法(其中若sigma,vt有0值或vt有正值,结果为MAXNUM)
def dual_Sigma_MUL_vtReciprocal(sigma,vt):
    MAXNUM = 2*16
    MINDECI = 10**-6
    if np.min(vt) >= 0:
        print(vt,'!!!!!!!!!!!!!!!!!!!!!!!某改!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    elif np.max(sigma) > 0:
        print('验证数为正不应该使用对偶单纯形')
    else:
        theta = np.zeros(vt.shape)
        for i in range(vt.shape[1]):
            if abs(sigma[:,i] - 0) < MINDECI or abs(vt[:,i] - 0) < MINDECI or vt[:,i] > 0:
                theta[:,i] = np.array([MAXNUM])
            else:
                theta[:,i] = sigma[:,i]/vt[:,i]
        return theta

#对偶单纯形的每一次迭代
def dualTableMethod_Step(qt):
    minx = np.argmin(qt.b)
    xi = np.argmin(dual_Sigma_MUL_vtReciprocal(qt.getsigma(),qt.A[minx,:]))
    print('退出者:xb第',minx+1,'行,换入者:x'+str(xi+1))
    qt.xB[minx] = xi
    Y = xi
    X = minx
    qt = AConv(qt,X,Y)
    return qt

def dualTableMethod(qt):
    print(qt)
    print('--------------------')
    c = 0
    while  np.min(qt.b) < 0 and c<5:
        qt = dualTableMethod_Step(qt)
        print(qt)
        print('--------------------')
        c+=1




if __name__ == '__main__':
    cT = np.mat([-1.,-2,-3,0,0,0])

    A = np.mat([[-2.,1,-1,1,0,0]
               ,[1,1,2,0,1,0]
               ,[0,1,-1,0,0,1]])
    b = np.mat([[-4.]
               ,[8]
               ,[2]])
    xB = np.mat([[4]
                ,[5]
                ,[6]])

    qt = QTable(cT,A,b,xB)
    dualTableMethod(qt)




'''

cT = np.mat([-5.,5,8,0,0])
xB = np.mat([[2]
            ,[5]])
b = np.mat([[20.]
           ,[10]])
A = np.mat([[-1.,1,3,1,0]
          ,[16,0,-2,-4,1]])
'''
