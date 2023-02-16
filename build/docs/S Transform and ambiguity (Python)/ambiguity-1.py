import numpy as np
import matplotlib.pyplot as plt
pi = np.pi

def Ambiguity(x, T, Tau, Eta):
	'''
	Ambiguity Function
		x: signal, in callable form
		T: time indices in list
		Tau: tau indices in list
		Eta: eta indices in list
	'''
	dt = T[1] - T[0]
	dtau = Tau[1] - Tau[0]
	deta = Eta[1] - Eta[0]
	N = int((1/dt) * (1/deta))
	eta_offset = int(Eta[0] // deta)
	A = np.zeros((len(Tau), len(Eta)), dtype = 'D')

	def xx(tidx, tauidx):
		t = T[tidx]
		tau = Tau[tauidx]
		x1 = x(t + tau / 2)
		x2 = np.conjugate(x(t - tau / 2))
		return x1 * x2

	for tauidx in range(len(Tau)):
		xxlist = np.array([xx(tidx, tauidx) for tidx in range(len(T))])
		xxlist = np.concatenate((xxlist, np.zeros(N - len(T))))
		c = np.fft.fft(xxlist)
		for etaidx in range(len(Eta)):
			A[tauidx, etaidx] = c[(etaidx + eta_offset) % N] * dt

	return A


def Ambiguity_test(alpha, t1, f1, t2, f2, Tau, Eta):
	tauindex = 0
	etaindex = 0
	alphafact1 = np.sqrt(1 / (2 * alpha))
	alphafact2 = np.sqrt(1 / (2 * alpha))
	tmu = (t1 + t2) / 2
	fmu = (f1 + f2) / 2
	alphamu = alpha
	td = t1 - t2
	fd = f1 - f2
	alphamufact = np.sqrt(1 / (2 * alphamu))
	B = np.zeros((len(Tau), len(Eta)), dtype = 'D')
	for tau in Tau:
		etaindex = 0
		for eta in Eta:
			B[tauindex, etaindex] = alphafact1 * np.exp(-pi * (alpha * tau**2 / 2 + eta**2 / (2*alpha))) * np.exp(2j * pi * (f1 * tau - t1 * eta))
			B[tauindex, etaindex] += alphafact2 * np.exp(-pi * (alpha * tau**2 / 2 + eta**2 / (2*alpha))) * np.exp(2j * pi * (f2 * tau - t2 * eta))
			Ax1x2 = alphamufact * np.exp(-pi * (alphamu*(tau-td)**2 / 2 + (eta-fd)**2 / (2 * alphamu))) * np.exp(2j * pi * (fmu*tau - tmu*eta + fmu*tmu))
			Ax2x1 = np.conjugate(alphamufact * np.exp(-pi * (alphamu*(-tau-td)**2 / 2 + (-eta-fd)**2 / (2 * alphamu))) * np.exp(2j * pi * (fmu*(-tau) - tmu*(-eta) + fmu*tmu)))
			B[tauindex, etaindex] += Ax1x2 + Ax2x1
			etaindex += 1
		tauindex += 1
	return B


def show_image(X, extent = None, C = 500):
	X = X.transpose()
	X = np.abs(X) / np.max(np.abs(X)) * C
	fig = plt.figure(constrained_layout = True)
	if extent:
		plt.imshow(X, cmap='gray', origin='lower', extent = extent)
	else:
		plt.imshow(X, cmap='gray', origin='lower')
	plt.xlabel('Tau')
	plt.ylabel('Eta')
	plt.show()


if __name__ == '__main__':
	# signal
	(t1, f1) = (1, 1)
	(t2, f2) = (-1, -1)
	alpha = 0.1
	def x(t):
		x1 = np.exp(2j * pi * f1 * t - alpha * pi * (t-t1)**2)
		x2 = np.exp(2j * pi * f2 * t - alpha * pi * (t-t2)**2)
		return x1 + x2

	dt = 0.05
	dtau = dt
	deta = dt
	T = np.arange(-5, 5, dt)
	Tau = np.arange(-5, 5, dtau)
	Eta = np.arange(-5, 5, deta)

	A = Ambiguity(x, T, Tau, Eta)

	# B = Ambiguity_test(alpha, t1, f1, t2, f2, Tau, Eta)

	show_image(A, extent = (Tau[0], Tau[-1], Eta[0], Eta[-1]))
