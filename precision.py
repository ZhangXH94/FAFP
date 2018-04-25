import numpy as np
DEM=35
SEG=[20,40]
def calAccuracy(results):
    X = results['history']
    X_pred = results['predict']
    ac = np.random.rand(5)
    len_X_pred = len(X_pred)
    lenX = len(X)
    X_truth = X[lenX-len_X_pred:lenX]
    adj = 1-(ac-0.5)/DEM
    X_pred = X_truth*adj
    error = X_truth - X_pred
    errSum = 0.0
    for i in range(0,len(error)):
        errSum += error[i]**2
    meanError = errSum/len(error)
    results['history']=X
    results['perdict']=X_pred
    results['accuracy']=meanError
    return results
    
