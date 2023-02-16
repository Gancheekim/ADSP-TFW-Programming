import numpy as np
from math import *
import matplotlib.pyplot as plt


# ---------"Implement WDF by Chirp-Z Transform"---------
def chirpZ_WDF(x,t,f,B):
    dt = t[1]-t[0]
    df = f[1]-f[0]
    
    Q = int(B/dt)
    N = int(np.round(1/(dt*df),2))

    T = len(t)
    F = len(f)
    
    n0 = int(t[0]/dt)
    m0 = int(f[0]/df)

    n = np.arange(n0,n0+T)
    m = np.arange(m0,m0+F)
    
    zero_time_index = np.where(n == 0)[0]
    zero_freq_index = np.where(m == 0)[0]


    for n in np.arange(n0,n0+T):
        
        p = np.arange(-Q,Q+1,1)
        
        # Step1: Multiplication
        x1 = x[(n+p)%T]*np.conj(x[(n-p)%T])*(e**(-2j*pi*dt*df*(p**2)))
        
        # Step2: Convolution
        m_col = m[:,np.newaxis]
        c = e**(2j*pi*((m_col-p)**2)*dt*df)
                
        X2_tmp = np.transpose(np.sum(x1*c,axis=1,keepdims=True)) 
   
        if n == n0:
            X2 = X2_tmp
        else:
            X2 = np.vstack((X2,X2_tmp))
        
    
    # Step3: Multiplication
    X_tmp = 2*dt*(e**(-2j*pi*(m**2)*dt*df))*X2
    X_tmp = np.transpose(X_tmp)
    
    
    # check whether the array is not empty(there is zero value in time)
    if zero_time_index.size != 0:
        # shift the col(time = t_begin~0~t_end)
        X = np.hstack((X_tmp[:,zero_time_index[0]:len(X_tmp[0])],X_tmp[:,0:zero_time_index[0]])) 

    return X