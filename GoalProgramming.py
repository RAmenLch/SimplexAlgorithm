import SimplexAlgorithm as sa
import numpy as np

__MAXP = 4
P1 = -10**(__MAXP)
P2 = -10**(__MAXP-4)





class GPTable(sa.QTable):
    __MAXP = 20
    P1 = -10**(__MAXP)
    P2 = -10**(__MAXP-5)
    P3 = -10**(__MAXP-10)
    P4 = -10**(__MAXP-15)
    P5 = -10**(__MAXP-20)
    def __init__(self,cxT,cdT,A,b,xB):
        cT = np.hstack([cxT,cdT])
        sa.QTable.__init__(self,cT,A,b,xB)


def GPtableMethod(gpt):
    sa.tableMethod(gpt)



if __name__ == '__main__':
    '''          [ 1, 2,  3,  4,  5,  6,  7,  8,  9, 10]  '''
    '''          [X1,X2,d1+,d1-,d2+,d2-,d3+,d3-,d4+,d4-]  '''

    cxT = np.mat([0.,0,0])
    cdT = np.mat([P1,0,P2,P2])

    A = np.mat([[1., 1,1,0, 0,0,0]
               ,[1,-1,0,1,-1,0,0]
               ,[2, 3,0,0,0,1,-1]])
    b = np.mat([[10]
               ,[4.5]
               ,[6]])
    xB = np.mat([[3]
                ,[4]
                ,[6]])

    gpt = GPTable(cxT,cdT,A,b,xB)
    GPtableMethod(gpt)














'''
cxT = np.mat([0.,0])
#             d1,d1-,d2+,d2-,d3+,d3-,d4+,d4-
cdT = np.mat([GPTable.P1, GPTable.P4, GPTable.P1,2*GPTable.P4,GPTable.P2,0.,0,GPTable.P3])

A = np.mat([[0.,1,1,-1,0,0,0,0,0,0]
           ,[1,0,0,0,1,-1,0,0,0,0]
           ,[4,6,0,0,0,0,1,-1,0,0]
           ,[12,18,0,0,0,0,0,0,1,-1]])
b = np.mat([[9.]
           ,[8]
           ,[60]
           ,[252]])
xB = np.mat([[3]
            ,[5]
            ,[7]
            ,[9]])
'''
