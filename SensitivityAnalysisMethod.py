import numpy as np
from SimplexAlgorithm import QTable, AConv
from DualSimplexMethod import *
'''
判断灵敏度结果,并解决系数修改问题

异常懒得写,全都是print,略略略

'''




#修改非基变量参数ck
#k为x的下标[计算机下标]
def _deltacNonbasicVar(qt,k):
    delta_ck = -float(qt.getsigma()[:,k])
    return delta_ck

#修改非基变量参数ck
#k为x的下标[数学下标]
#返回deltac的上界
def deltacNonbasicVar(qt,k):
    k = k -1
    return _deltacNonbasicVar(qt,k)



#修改基变量参数cl
#l为xB的行数[计算机下标]
def _deltacBasicVar(qt,l):
    #max = max{sigmaj/a`lj|a`lj>0}
    #min = min{sigmaj/a`lj|a`lj<0}
    #max<delta_cl<min
    max,min = -10**6,10**6
    sigma = qt.getsigma()
    Alj = qt.A[l,:]
    for j in range(sigma.shape[1]):
        if not j in qt.xB and Alj[:,j] != 0:
            temp = sigma[:,j] / Alj[:,j]
            if Alj[:,j] > 0 and max < temp:
                max = temp
            elif Alj[:,j] < 0 and min > temp:
                min = temp
    return (float(max),float(min))

#修改基变量参数cl
#l为xB的行数[数学下标]
def deltacBasicVar(qt,l):
    l = l - 1
    return _deltacBasicVar(qt,l)

#修改右端参数br
#r为b的下标[计算机下标]
def _deltab(qt,r,B):
    #max = max{-b`i/betair|betair>0}
    #min = min{-b`i/betair|betair<0}
    #max<delta_cl<min
    max,min = -10**6,10**6
    beta = B.I
    b = qt.b
    for i in range(b.shape[0]):
        if beta[i,r] != 0:
            temp = -b[i,:]/beta[i,r]
            if beta[i,r] > 0 and max < temp:
                max = temp
            elif beta[i,r] < 0 and min > temp:
                min = temp
    return (float(max),float(min))

#修改右端参数br
#r为b的下标[数学下标]
def deltab(qt,r,B):
    r = r - 1
    return _deltab(qt,r,B)


#修改约束条件A系数aij,不可以是基变量的系数
#ij为a的计算机下标
def _deltaa(qt,i,j):
    if j in qt.xB:
        print('花Q花Q')
    m = qt.b.shape[0]
    y = -qt.getsigma()[:,-m:]
    if y[:,i] > 0:
        lb = qt.getsigma()[:,j] / y[:,i]
        return ('>=',float(lb))
    elif y[:,i] < 0:
        ub = qt.getsigma()[:,j] / y[:,i]
        return ('<=',float(ub))
    else:
        print('?????????????yi为0????????????????')

#修改约束条件A系数aij,不可以是基变量的系数
#ij为a的数学下标
def deltaa(qt,i,j):
    i -= 1
    j -= 1
    return _deltaa(qt,i,j)


#添加一个变量,限制条件向量为p,求c的最大值
def addxcLessThan(qt,B,p):
    cLessThan = qt.getcB().T * B.I * p
    return float(cLessThan)




def db_dualtable(qt,r,dbr,B):
    r = r - 1
    db = np.zeros(qt.b.shape)
    db[r,:] = dbr
    newb = qt.b + B.I * db
    newqt = QTable(qt.cT.copy(),qt.A.copy(),newb,qt.xB.copy()+1)
    #print(newqt)
    dualTableMethod(newqt)


def dcl_dualtable(qt,cT):
    qt.cT = cT
    print(qt)
    print('--------------------')
    qt = dcl_setp(qt)
    print(qt)
    print('--------------------')
    while  np.min(qt.b) < 0 :
        qt = dualTableMethod_Step(qt)
        print(qt)
        print('--------------------')

def dcl_setp(qt):
    minx = np.argmin(qt.b)
    xi = np.argmax(qt.getsigma())
    print('退出者:xb第',minx+1,'行,换入者:x'+str(xi+1))
    qt.xB[minx] = xi
    Y = xi
    X = minx
    print('Y',Y,'X',X)
    qt = AConv(qt,X,Y)
    return qt
def addA_dualtabe(qt,Anj,bn):
    newA1 = np.hstack((qt.A,np.zeros((qt.A.shape[0],1))))
    newA = np.vstack((newA1,Anj))

    newcT = np.hstack((qt.cT,np.zeros((1,1))))

    newb = np.vstack((qt.b,np.mat([bn])))
    newxB = np.vstack((qt.xB,np.mat([qt.A.shape[1]])))
    newqt = QTable(newcT,newA,newb,newxB + 1)
    print(newqt)
    print('--------------------')
    for i in range(qt.xB.shape[0]):
        newqt = AConv(newqt,i,int(qt.xB[i,:]))
    dualTableMethod(newqt)


if __name__ == '__main__':
    cT = np.mat([20.,12,10,0,0])
    xB = np.mat([[1]
                ,[2]])
    b = np.mat([[10.]
               ,[130]])
    A = np.mat([[1,0,9/20,3/20,-1/5]
              ,[0,1,17/20,-1/20,2/5]])
    qt = QTable(cT,A,b,xB)
    B =  np.mat([[8.,4]
               ,[1,3]])
    p = np.mat([[10]
               ,[2.5]])
    print(deltacBasicVar(qt,1))



'''
cT = np.mat([-5.,5,13,0,0])
xB = np.mat([[2.]
            ,[5]])
b = np.mat([[20.]
           ,[10]])
A = np.mat([[-1.,1,3,1,0]
          ,[16,0,-2,-4,1]])
'''
