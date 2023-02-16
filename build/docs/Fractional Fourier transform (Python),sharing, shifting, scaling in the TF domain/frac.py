import numpy as np
import math
import scipy.signal
import matplotlib.pyplot as plt
import cmath
import random

#rotation
def myfrac_fourier(signal,n_f):
	n_f=n_f%4 #n_f is the fraction of 1 fourier transform #1=pi/2
	#################################
	N=len(signal)
	sq=math.sqrt(N)
	signal=np.array(signal)
	after=np.zeros(signal.shape,dtype=np.complex)
	signal=signal.astype(np.complex)
	###################################################
	shift=[]
	for i in range(N):
		b=(i+N/2)%N
		shift.append(int(b))
	###########################################
	if n_f==0.0:
		return signal
	if n_f==1.0:
		after[shift]=np.fft.fft(signal[shift])/sq
		
		return after
	if n_f==2.0:
		return np.flipud(signal)
	if n_f==3.0:
		after[shift]=np.fft.ifft(signal[shift])*sq
		return after
	################################################
	if n_f > 2.0:
		n_f = n_f - 2.0
		signal = np.flipud(signal)
	elif n_f > 1.5:
		n_f = n_f - 1
	elif n_f < 0.5:
		n_f = n_f + 1
		signal[shift] = np.fft.ifft(signal[shift])*sq
	###########################################################
	alpha =n_f* math.pi/2
	sina = math.sin(alpha)
	tana2 = math.tan(alpha/2)
	####################################
	m=np.zeros(2*N-1,dtype=signal.dtype)
	m[:2*N:2]=signal

	s0=[]
	for n in range(-2*N+3,2*N-2):
		s0.append(np.sinc(n/2))

	ww=scipy.signal.fftconvolve(m[:2*N],np.array(s0))
	#########################################
	signal= np.hstack((np.zeros(N-1),ww[2*N-3:-2*N+3], np.zeros(N-1))).T
	chirp=[]
	for n in range(-2*N+2,2*N-1):
		p=-1j*(math.pi*tana2*pow(n,2))*(1/(4*N))
		m=cmath.exp(p)
		chirp.append(m)
	chirp=np.array(chirp)
	signal=chirp*signal
	##############################
	g=math.pi/(N*sina*4)
    
	s1=[]
	for k in range(-4*N+4,4*N-3):
		con=1j*g*pow(k,2)
		p=cmath.exp(con)
		s1.append(p)

	after=scipy.signal.fftconvolve(np.array(s1),signal)
	after=after[4*N-4:8*N-7]*math.sqrt(g/math.pi)
	after=after*chirp

	h=cmath.exp(-1j*(1-n_f)*math.pi/4)
	return after[N-1:-N+1:2]*h


#######################################################