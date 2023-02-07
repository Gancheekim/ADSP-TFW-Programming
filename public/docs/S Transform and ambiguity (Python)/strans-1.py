import numpy as np
from numpy.fft import fft, ifft
import matplotlib.pyplot as plt
pi = np.pi

def expi(x):
	return np.exp(-2j * pi * x)

def w(t, sgm = 0.5):
	return np.exp(-sgm * pi * t**2)

def Gabor(x, T, F, sgm = 0.5):
	dt = T[1] - T[0]
	df = F[1] - F[0]
	N = int((1/dt) * (1/df))
	m_offset = int(F[0] / df)
	n_offset = int(T[0] / dt)
	X = np.zeros((len(T), len(F)), dtype = 'D')
	Q = int((1.9143 / (sgm**0.5)) / dt)

	def xt(tidx):
		if tidx < 0 or tidx > len(T) - 1:
			return 0
		return x(T[tidx])

	for n in range(len(T)):
		x1 = [w(k*dt, sgm) * xt(n+n_offset+k) for k in range(-Q, Q+1)]
		x1 = np.concatenate((x1, np.zeros(N - 2*Q - 1)))
		X1 = np.fft.fft(x1)
		for m in range(len(F)):
			X[n, m] = X1[(m+m_offset) % N] * expi( (Q-n-n_offset) * (m+m_offset) / N ) * dt

	return X


def convolve(a, b):
	lenN = len(a) + len(b) - 1
	a0 = np.concatenate((a, np.zeros(lenN - len(a))))
	b0 = np.concatenate((b, np.zeros(lenN - len(b))))
	return ifft(fft(a0) * fft(b0))


def ST(x, T, F, s = None):
	'''
	S Transform
		x: signal, in callable form
		T: time indices in list
		F: frequency indices in list
		s: general parameter function, in callable form
	'''
	dt = T[1] - T[0]
	X = np.zeros((len(T), len(F)), dtype = 'D')
	if s == None:
		def s(f):
			return (0.3*abs(f)**0.7) + 0.1

	for m in range(len(F)):
		sf = s(F[m])
		ndt = min(len(T), int((1.9 / sf) / dt) + 1)
		a = [x(T[i]) * expi(F[m]*T[i]) for i in range(len(T))]
		b = [np.exp(-pi * (T[i] * sf)**2) for i in range(ndt)]
		b = np.concatenate((b[ndt - 2:: -1], b))
		c = convolve(a, b)
		for n in range(len(T)):
			X[n, m] = c[n + ndt - 1] * sf

	return X

def show_image(X, extent = None, C = 500):
	X = X.transpose()
	X = np.abs(X) / np.max(np.abs(X)) * C
	fig = plt.figure(constrained_layout = True)
	if extent:
		plt.imshow(X, cmap='gray', origin='lower', extent = extent)
	else:
		plt.imshow(X, cmap='gray', origin='lower')
	plt.xlabel('Time (Sec)')
	plt.ylabel('Frequency (Hz)')
	plt.show()

if __name__ == '__main__':
	dt = 0.05
	df = 0.05
	T1 = np.arange(0, 10, dt)
	T2 = np.arange(10, 20, dt)
	T3 = np.arange(20, 30, dt)
	T = np.arange(0, 30, dt)
	F = np.arange(-5, 5, df)
	x1 = [np.cos(2*pi*tt) for tt in T1]
	x2 = [np.cos(6*pi*tt) for tt in T2]
	x3 = [np.cos(4*pi*tt) for tt in T3]
	# x = np.concatenate((x1, x2, x3))
	def x(t):
		if t < 10:
			return np.cos(2 * pi * t)
		elif t < 20:
			return np.cos(6 * pi * t)
		else:
			return np.cos(4 * pi * t)

	Xg = Gabor(x, T, F)
	Xs = ST(x, T, F)

	C = 400
	Xg = np.abs(Xg) / np.max(np.abs(Xg)) * C
	Xs = np.abs(Xs) / np.max(np.abs(Xs)) * C
	plt.figure(constrained_layout = True)
	plt.subplot(2,1,1)
	plt.imshow(Xg.transpose(), cmap='gray', origin='lower', extent=[0,30, -5,5])
	plt.xlabel('Time (Sec)')
	plt.ylabel('Frequency (Hz)')
	plt.title('Gabor Transform')
	plt.subplot(2,1,2)
	plt.imshow(Xs.transpose(), cmap='gray', origin='lower', extent=[0,30, -5,5])
	plt.xlabel('Time (Sec)')
	plt.ylabel('Frequency (Hz)')
	plt.title('S Transform')
	plt.show()
