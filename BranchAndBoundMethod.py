from SimplexAlgorithm import *
from DualSimplexMethod  import *
import numpy as np





def BABM():
    pass


if __name__ == '__main__':
    M = 10**8
    cT = np.mat([1.,1,0,0])
    A = np.mat([
        [2.,1,1,0],
        [4,5,0,1],
    ])
    b = np.mat([6.,20]).T
    xB = np.mat([3,4]).T
    qt = QTable(cT,A,b,xB)
    tableMethod(qt)
    print(qt.getMaxf())
    print("==========================================")
    qt.A = np.hstack([qt.A,np.mat([0,0]).T])
    qt.A = np.vstack([qt.A,np.mat([0,0,-25,-5,1])])
    qt.cT = np.mat([1,1,0,0,0])
    qt.xB = np.vstack([qt.xB,np.mat([4])])
    qt.b = np.vstack([qt.b,np.mat([-18])])
    dualTableMethod(qt)
    print(qt.getMaxf())
