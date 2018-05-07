import numpy as np



#axis = 0 判断每行的零个数
#axis = 1 判断每列的零个数
def getZeroNums(mt,axis):
    MAXNUM = 10**16
    zeroN = []
    if axis == 0:
        for i in range(mt.shape[0]):
            try:
                sumN = np.sum(mt[i,:]==0.)
                if sumN == 0:
                    sumN == MAXNUM
                zeroN.append(sumN)
            except Exception as e:
                print(i)
                print(mt[i,:])
    elif axis == 1:
        for i in range(mt.shape[1]):
            sumN = np.sum(mt[:,i]==0)
            if sumN == 0:
                sumN == MAXNUM
            zeroN.append(sumN)
    else:
        raise ValueError("axis can only be 0 or 1")
    return zeroN

def setMark(mt):
    while 1:
         zNs0 = getZeroNums(mt,0)
         zNs1 = getZeroNums(mt,1)
         minzNs0 = min(zNs0)
         minzNs1 = min(zNs1)
         for index,zN in enumerate(zNs0):
             if zN == minzNs0:
                 z = np.where(mt[index,:] == 0.)[1]
                 if z:
                     z = int(z[0])
                 else:
                     continue
                 mt[index,z] = -16
                 z0 = np.where(mt[index,:] == 0.)[1].tolist()
                 for i in z0:
                     mt[index,i] = -32
                 z1 = np.where(mt[:,z] == 0.)[0].tolist()
                 for i in z1:
                     mt[i,z] = -32
         for index,zN in enumerate(zNs1):
             if zN == minzNs1:
                 z = np.where(mt[:,index] == 0.)[0]
                 if z:
                     z = int(z[0])
                 else:
                     continue
                 mt[z,index] = -16
                 z0 = np.where(mt[z,:] == 0)[1].tolist()
                 for i in z0:
                     mt[z,i] = -32
                 z1 = np.where(mt[:,index] == 0.)[0].tolist()
                 for i in z1:
                     mt[i,index] = -32
         if np.sum(mt == 0.) == 0:
             break
    return mt

def delMark(mt):
    for i in range(mt.shape[0]):
        for j in range(mt.shape[1]):
            if int(mt[i,j]) == -32 or int(mt[i,j]) == -16:
                mt[i,j] = 0
    return mt


def isOk(mt):
    if np.sum(mt == -16) == mt.shape[0]:
        return True
    else:
        return False



#返回无加圈0元素[即-16]的行
def getNoMaskORow(mt):
    tickRow = []
    for i in range(mt.shape[0]):
        sumN = np.sum(mt[i,:]==-16)
        if sumN == 0:
            tickRow.append(i)
    return set(tickRow)

#对加勾的行做检查,对划去的零[-32]的列加勾
def getMarkXCol(mt,tickRow):
    tickCol = []
    for i in tickRow:
        ncol = np.where(mt[i,:]==-32)[1].tolist()
        tickCol += ncol
    return set(tickCol)

def getMarkORow(mt,tickCol):
    tickRow = []
    for i in tickCol:
        nrow = np.where(mt[:,i]==-16)[0].tolist()
        tickRow += nrow
    return set(tickRow)


def convert(mt):
    tickRow = getNoMaskORow(mt)
    tickCol = getMarkXCol(mt,tickRow)
    while(1):
        tickRowTemp = tickRow | getMarkORow(mt,tickCol)
        tickColTemp = tickCol | getMarkXCol(mt,tickRowTemp)
        if tickRowTemp == tickRow and tickColTemp == tickCol:
            break
        else:
            tickCol = tickColTemp
            tickRow = tickRowTemp
    allRow = set(range(0,mt.shape[0]))
    noTickRow = allRow - tickRow
    noTickRow = list(noTickRow)
    tickCol = list(tickCol)
    tickRow = list(tickRow)
    mtD = mt.copy()
    if len(noTickRow) + len(tickCol) == mt.shape[0]:
         raise Exception("l < n 分派错误,要重新回到第二步,但是好像这种情况很难搞所以先不搞")
    mtD = np.delete(mtD, noTickRow,0)
    mtD = np.delete(mtD, tickCol, 1)
    mt = delMark(mt)
    min = np.min(mtD)
    for i in tickRow:
        mt[i,:] -= min
    for j in tickCol:
        mt[:,j] += min
    return mt

def HM(mt):
    for i in range(mt.shape[0]):
        mt[i,:] = mt[i,:] - float(np.min(mt[i,:]))
    for i in range(mt.shape[1]):
        mt[:,i] = mt[:,i] - float(np.min(mt[:,i]))
    print(mt)
    markMt = mt.copy()
    while 1:
        markMt = setMark(markMt)
        print(markMt)
        if isOk(markMt):
            break
        else:
            markMt = convert(markMt)
            print(markMt)


if __name__ == '__main__':
    mt = np.mat([
                [37.7,32.9,33.8,37.0,35.4],
                [43.3,33.1,42.2,34.7,41.8],
                [33.3,28.5,38.9,30.4,33.6],
                [29.2,26.4,29.4,28.5,31.1],
                [   0,   0,   0,   0,   0]
                ])
    HM(mt)
