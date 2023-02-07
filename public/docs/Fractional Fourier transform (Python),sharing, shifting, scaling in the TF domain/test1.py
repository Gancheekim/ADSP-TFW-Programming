import numpy as np
import math
import scipy.signal
import matplotlib.pyplot as plt
import cmath
import random
from frac import myfrac_fourier


def mytest1():
	fig, ax = plt.subplots(2,3,figsize=(13,7))
	###########################
	np.random.seed(5)
	dt=0.0001
	t=np.arange(0.0,10.0,dt)
	r=0.3*np.random.random(size=len(t))
	sam=int(1.0/dt)
	###################################
	x1=[]
	x2=[]
	x3=[]
	########################################
	for tt in t:
		f1=2*math.cos(2*math.pi*1000*tt)
		f2=1.5*math.cos(2/3*math.pi*500*tt)
		x3.append(f1+f2)
	###################################
	trans=[0, 0.3, 1, 1.7, 2.3, 3.5]
	

	for i,tr in enumerate(trans):
		f=myfrac_fourier(x3,tr)
        
		if i< 3:
			ax[0][i].specgram(f+r,Fs=sam,cmap=plt.cm.Blues)
			ax[0][i].grid(False)
			ax[0][i].set_title(f"fraction={tr}",fontsize=14)
			ax[0][i].set_xlabel('time')
			ax[0][i].set_ylabel('Hz')
		else:
			ax[1][i-3].specgram(f+r,Fs=sam, cmap=plt.cm.Blues)
			ax[1][i-3].grid(False)
			ax[1][i-3].set_title(f"fraction={tr}", fontsize=14)
			ax[1][i-3].set_xlabel('time')
			ax[1][i-3].set_ylabel('Hz')

	############################################3
	fig.suptitle('Fractional Fourier Transform\n',fontsize=14,fontweight='bold')
	fig.tight_layout(pad=5)
	plt.show()


mytest1()