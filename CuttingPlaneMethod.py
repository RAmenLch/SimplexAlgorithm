from SimplexAlgorithm import *
from DualSimplexMethod  import *
import numpy as np


def addCP(qt,a,xB,b):
    A00 = np.zeros((qt.A.shape[0],1))
    qt.A = np.hstack([qt.A,A00])
    qt.A = np.vstack([qt.A,a])
    qt.cT = np.hstack([qt.cT,np.mat([0])])
    qt.xB = np.vstack([qt.xB,np.mat([xB-1])])
    qt.b = np.vstack([qt.b,np.mat([b])])
    return qt


if __name__ == '__main__':
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
    qt = addCP(qt,np.mat([0,0,-5,-5,1]),5,-4)
    dualTableMethod(qt)
    print(qt.getMaxf())
    print("==========================================")
    qt = addCP(qt,np.mat([0,0,0,0,-26/30,1]),6,-0.2)
    dualTableMethod(qt)
    print(qt.getMaxf())
    print("==========================================")
    qt = addCP(qt,np.mat([0,0,0,0,0,-0.19230769,1]),6,-0.96153846)
    dualTableMethod(qt)
    print(qt.getMaxf())
