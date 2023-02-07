import time
import numpy as np
import math
import cmath
import cv2
from frac import myfrac_fourier
import scipy.signal
import sys, os, argparse
import msvcrt
###############################################
#fshearc=2#[0,0,2]
#tshearc=2#1/2#[0,0,1/2]
#fraction=2/3
#t0=2
#f0=1
#scalec=2
#mag=100
#####################################################
dt=0.05
df=0.05
B=0.5
#######################################################
def myRange(start,end,step):
    i = start
    while i < end:
        yield i
        i += step
    yield end

##############################################################
def function1(tt):
	return math.cos(2*math.pi*tt)

def function2(tt):
	return math.cos(6*math.pi*tt)

def function3(tt):
	return math.cos(4*math.pi*tt)
#####################################################
def hshifting(t0,tt):
	faket=[]
	for i in range(len(tt)):
		faket.append(tt[i]-t0)

	return faket

def dilation(scalec,tt,Cs):
	faket=[]
	fakec=[]
	for i in range(len(tt)):
		faket.append(tt[i]/scalec)
		fakec.append(Cs[i]/math.sqrt(abs(scalec)))

	return faket,fakec
##############################################
def fshearing(fshearc,tt,Cs):
	#global fshearc
	fakec=[]

	for i in range(len(tt)):

		#ff=0
		#for k in range(len(fshearc)):
		#	ff+=fshearc[k]*pow(tt[i],k)
		ff=fshearc*pow(tt[i],2)

		com=1j*math.pi*ff
		fin=Cs[i]*cmath.exp(com)
		fakec.append(fin)
	
	return fakec

def vshifting(f0,tt,Cs):
	fakec=[]

	for i in range(len(tt)):
		fin=Cs[i]*cmath.exp(1j*2*math.pi*f0*tt[i])
		fakec.append(fin)

	return fakec

##################################################################
def tshearfunc(tshearc,tou):
	#global tshearc
	#tem=0
	#for k in range(len(tshearc)):
	#	tem+=tshearc[k]*pow(tou,k)
	tem=pow(tou,2)/tshearc
	tem=tem*1j*math.pi
	
	return cmath.exp(tem)

#############################################################
def recSTFT(x,t,f,B,mag):
	global dt,df
	
	nn=len(t)
	mm=len(f)

	Q=int(B/dt)
	N=int(1/(dt*df))

	immm=np.zeros((nn,mm), dtype=np.uint8)

	
	#####################################################

	for p in range(nn):
		
		n=int(t[p]/dt)
		for d in range(mm):
			
			#?
			m=int((f[d]/df))

			ss=dt*cmath.exp(1j*2*math.pi*(Q-n)*m/N)
			
			m=int((f[d]/df)%N)
			######################################3
			summ=0
			#############################################
			for q in range((2*Q+1)):

				
				##########################
				
				if abs((Q-q)*dt)<B:
				######################
					k=n-Q+q
					#?
					if (k>-1) and (k<nn):
						xq=x[k]
						summ+=xq*cmath.exp(-1j*2*math.pi*q*m/N)

			#############################################################
			#?
			immm[p,d]=abs(ss*summ)*mag

			###############################################

	return immm.transpose()


def show(see):
	cv2.imshow('result', see)
	cv2.waitKey(0) 
	cv2.destroyAllWindows() 
#############################################
class myProject:
	def __init__(self):
		
		##############################
		global dt,df,B#t0,f0,scalec,fraction
		#self.t0=t0
		#self.f0=f0
		#self.scalec=scalec
		#self.fraction=fraction
		#########################################
		self.dt=dt
		self.df=df
		self.B=B
		#################################
		self.t=[]
		self.c=[]
		####################
		self.f=[]
		self.x=[]

		for i in myRange(0,30,(dt)):
			self.t.append(round(i, 2))
	
		for i in myRange(-5,4.9999,(df)):
			self.f.append(round(i, 2))

		for i in range(len(self.t)):
			self.c.append(1)
    	#############################

	def recalx(self):

		self.x=[]
		inter=int(len(self.t)/3)
		for i in range(len(self.t)):
			if (i<inter*1):
				xx=function1(self.t[i])*self.c[i]
			elif (inter*1<=i) and (i<inter*2):
				xx=function2(self.t[i])*self.c[i]
			else:
				xx=function3(self.t[i])*self.c[i]

			self.x.append(xx)

	def main(self,arg):
		dic=vars(arg)
		mag=100
		ini=True

		for k in dic:
			v=dic[k]	
			
			if v!=None:
				ini=False
				if k=='hshift':
					t0=float(v[0])
					self.t=hshifting(t0,self.t)
					self.recalx()
				if k=='vshift':
					f0=float(v[0])
					self.c=vshifting(f0,self.t,self.c)
					self.recalx()
				if k=='dilate':
					scalec=float(v[0])
					self.t,self.c=dilation(scalec,self.t,self.c)
					self.recalx()
				if k=='fshear':
					fshearc=float(v[0])
					self.c=fshearing(fshearc,self.t,self.c)
					self.recalx()
				if k=='tshear':
					tshearc=float(v[0])
					h=[]
					for i in range(len(self.t)):
						h.append(tshearfunc(tshearc,self.t[i]))

					self.recalx()
					self.x=scipy.signal.fftconvolve(h,self.x)
					mag=5
				if k=='frac':
					frac=float(v[0])
					self.recalx()
					self.x=myfrac_fourier(self.x,frac)

		if ini:
			self.recalx()

		see=recSTFT(self.x,self.t,self.f,self.B,mag)
		show(see)
###############################################
parser = argparse.ArgumentParser()
parser.add_argument('--hshift', nargs=1,required=False)
parser.add_argument('--vshift', nargs=1,required=False)
parser.add_argument('--dilate', nargs=1,required=False)
parser.add_argument('--fshear', nargs=1,required=False)
parser.add_argument('--tshear', nargs=1,required=False)
parser.add_argument('--frac', nargs=1,required=False)
args = parser.parse_args()
##########################################3
pro=myProject()
pro.main(args)
