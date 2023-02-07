import numpy as np
from NTT import *

def pointwise_modmult(X, Y, M):
	N = len(X)
	Z = np.zeros(N, dtype = int)
	for i in range(N):
		Z[i] = modmult(X[i], Y[i], M)
	return Z
	
def convolve(x_in, y_in, ntt = None):
	if ntt != None:
		x = np.append(x_in, [0] * (ntt.N - len(x_in)))
		y = np.append(y_in, [0] * (ntt.N - len(y_in)))
		X = ntt.forward(x)
		Y = ntt.forward(y)
		Z = pointwise_modmult(X, Y, ntt.M)
		z = ntt.inverse(Z)
		return z[: len(x_in) + len(y_in) - 1]
	else:
		output_len = len(x_in) + len(y_in) - 1
		x = np.append(x_in, [0] * (output_len - len(x_in)))
		y = np.append(y_in, [0] * (output_len - len(y_in)))
		z = np.zeros(output_len, dtype = int)
		for i in range(output_len):
			for j in range(i+1):
				z[i] += x[j] * y[i - j]
		return z

if __name__ == '__main__':
	N = 16
	M = 8380417
	alpha = 2883726
	ntt = fNTT(N, M, alpha)
	x = np.random.randint(0, 724, size = (N // 2))
	y = np.random.randint(0, 724, size = (N // 2))
	print("Input sequence:", x, y, sep = '\n')
	z_ntt = convolve(x, y, ntt)
	z_direct = convolve(x, y)

	print()
	print("Convolution with NTT:", z_ntt, sep = '\n')
	print()
	print("Convolution directly:", z_direct, sep = '\n')