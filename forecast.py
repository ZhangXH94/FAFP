import numpy as np
import math
def cirSum(X):
    result = list()
    for i in range(0,len(X)):
        result.append(sum(X[0:i+1]))
    return result
def calConsDem(X):
    consdem = list()
    for i in range(2,len(X)+1):
        consdem.append(math.log(X[i-1]/X[i-2])/math.log(float(i-1)/float(i)))
    return consdem
DEM = 35
SEG = [20,40]
def calHurst(X):
    N = len(X)
    n = range(20,40)
    m = [int(N/i) for i in n]
    F = list()
    for i in range(20):
        Fsum = 0.0
        for j in range(m[i]):
            if (j+1)*n[i]>N:
                x = X[j*n[i]:]
                xl = N - j*n[i]
            else:
                x = X[j*n[i]:(j+1)*n[i]]
                xl = n[i]
            x_ave = sum(x)/xl
            std = 0.0
            for k in x:
                std = std+(k-x_ave)**2
            R = std-(x[0]-x_ave)**2
            std = math.sqrt(std/xl)
            Fsum = Fsum+R/std
        F.append(Fsum/m[i])
    return F
def cirMinus(S2R,S1R):
    temp = [0,0,0,0,0]
    temp[4]=S2R[4]-S2R[3]
    temp[3]=S2R[3]-S2R[2]
    temp[2]=S2R[2]-S2R[1]
    temp[1]=S2R[1]-S2R[0]
    temp[0]=S2R[0]-S1R
    return temp

def calConsDem(X):
    consdem = list()
    for i in range(2,len(X)+1):
        consdem.append(math.log(X[i-1]/X[i-2])/math.log(float(i-1)/float(i)))
    return consdem

def calConsC(X,D):
    C = list()
    for i in range(1,len(X)):
        C.append(X[i]*math.pow(i,D[i-1]))
    return C

def fR(R,D,C):
    results  = list()
    for i in R:
        results.append(C/math.pow(i,D))
    return results

def forecast(X):
    lenX = len(X)
    results = dict()
    
    S1 = cirSum(X)
    S2 = cirSum(S1)
    S3 = cirSum(S2)
    S4 = cirSum(S3)
    D0 = calConsDem(X)
    D1 = calConsDem(S1)
    D2 = calConsDem(S2)
    D3 = calConsDem(S3)
    C2 = calConsC(S2,D2)
    S2R = fR(range(lenX-5,lenX),D2[-1],C2[-1])
    S1R = cirMinus(S2R,S2[lenX-5])
    XR = cirMinus(S1R,S1[lenX-5])
    results['history']=X
    results['predict']=XR
    return results



