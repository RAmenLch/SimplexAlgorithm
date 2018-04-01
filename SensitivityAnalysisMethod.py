import numpy as np
from SimplexAlgorithm import QTable, AConv
from DualSimplexMethod import *
'''
判断灵敏度结果,并解决系数修改问题

异常懒得写,全都是print,略略略

未解决的问题:
    非基变量参数ck修改导致最优解改变
    新增一个变量xn+1,cn+1为目标函数系数,p为约束向量,导致最优解改变

'''




#修改非基变量参数ck
#k为x的下标[计算机下标]
def _deltacNonbasicVar(qt,k):
    delta_ck = -float(qt.getsigma()[:,k])
    return delta_ck

#修改非基变量参数ck
#k为x的下标[数学下标]
#返回deltac使最优解不变的上界
def deltacNonbasicVar(qt,k):
    k = k -1
    return _deltacNonbasicVar(qt,k)



#修改基变量参数cl
#l为xB的行数[计算机下标]
#返回deltac使最优解不变的区间
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
#返回deltac使最优解不变的区间
def deltacBasicVar(qt,l):
    l = l - 1
    return _deltacBasicVar(qt,l)

#修改右端参数br
#r为b的下标[计算机下标]
#B为原最优解在原问题A下的矩阵
#返回deltab使最优解不变的区间
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
#B为原最优解在原问题A下的矩阵
#返回deltab使最优解不变的区间
def deltab(qt,r,B):
    r = r - 1
    return _deltab(qt,r,B)


#修改约束条件A系数aij,不可以是基变量的系数
#i,j为a的计算机下标
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
#i,j为a的数学下标
def deltaa(qt,i,j):
    i -= 1
    j -= 1
    return _deltaa(qt,i,j)


#添加一个变量xn+1,限制条件向量为p,求cn+1的上界
def addxcLessThan(qt,B,p):
    cLessThan = qt.getcB().T * B.I * p
    return float(cLessThan)



#当deltab能改变最优解时,qt为原最优解表格,r为更改的br下标,dbr为deltabr,B为原最优解在原问题A下的矩阵(原最优可行基)
def db_dualtable(qt,r,dbr,B):
    r = r - 1
    db = np.zeros(qt.b.shape)
    db[r,:] = dbr
    #修改原问题br只有使表格的b发生改变
    newb = qt.b + B.I * db
    #深拷贝防止迭代改变原QTable
    newqt = QTable(qt.cT.copy(),qt.A.copy(),newb,qt.xB.copy()+1)
    #打印出新表的迭代过程
    dualTableMethod(newqt)

#cl指基变量的参数,本函数只解决基变量参数改变导致最优解改变的问题
#revisedcT表示改变后的cT
#这个函数八成有bug,因为只考虑了dcl_setp()只运行一次的情况,并不知道是否应是如此
def dcl_dualtable(qt,revisedcT):
    qt.cT = revisedcT
    print(qt)
    print('--------------------')
    #cl改变会导致n-m个检验数(sigma)发生改变,此时需要将其中大于0的检验数对应变量为进基变量
    qt = dcl_setp(qt)
    print(qt)
    print('--------------------')
    while  np.min(qt.b) < 0 :
        qt = dualTableMethod_Step(qt)
        print(qt)
        print('--------------------')

#将其中大于0的检验数对应变量为进基变量
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

#qt为原最优解表格
#Anj为新增约束
#bn为新增右端常数
#新增一个约束,在qt的基础上重新计算
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
