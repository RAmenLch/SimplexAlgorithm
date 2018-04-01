import numpy as np
from SimplexAlgorithm import *
from DualSimplexMethod import *
from SensitivityAnalysisMethod import *


def P88_15():
    cT = np.mat([-5.,5,13,0,0])
    xB = np.mat([
        [2],
        [5]
    ])
    b = np.mat([
        [20.],
        [10]
    ])
    A = np.mat([
        [-1.,1,3,1,0],
        [16,0,-2,-4,1]
    ])
    B = np.mat([
        [1.,0],
        [4,1]
    ])
    qt = QTable(cT,A,b,xB)
    print('(1)')
    db = deltab(qt,1,B)
    print('db:',db)
    db_dualtable(qt.copy(),1,25,B)

    print('(2)')
    db = deltab(qt,2,B)
    print('db:',db)
    print('(3)')
    dnbv = deltacNonbasicVar(qt,3)
    print('dnbv:',dnbv)#2,当c3>15时才会发生改变
    print('(4)')
    dbv = deltacBasicVar(qt,1)
    print('dbv:',dbv)
    dcl_dualtable(qt.copy(),np.mat([-5.,6,13,0,0]))
    print('(5)')
    print(addxcLessThan(qt,B,np.mat([[3],[5]])))
    print('(6)')
    Anj = np.mat([2.,3,5,0,0,1])
    bn = 50
    addA_dualtabe(qt,Anj,bn)

P88_15()
