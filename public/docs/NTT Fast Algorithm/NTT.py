import numpy as np

def modmult(a, b, M):
	return (a * b) % M

def modpow(alpha, n, M):
	if n == 0:
		return 1
	p = 1
	bn = bin(n)
	for b in bn[2:]:
		p = modmult(p, p, M)
		if b == '1':
			p = modmult(p, alpha, M)
	return p

def is_primitive(alpha, N, M):
	for i in range(1, N):
		if modpow(alpha, i, M) == 1:
			return False
	if modpow(alpha, N, M) == 1:
		return True
	else:
		return False

def find_primitive(N, M):
	for alpha in range(2, M):
		if is_primitive(alpha, N, M):
			return alpha
	return 0

def findinv(alpha, M):
	for i in range(M):
		if modmult(alpha, i, M) == 1:
			return i

def bit_reverse(x, n):
	if type(x) == int:
		bx = bin(x)[2:]
		r = 0
		for i in range(n-1, -1, -1):
			if i < len(bx) and int(bx[len(bx) - i - 1]) == 1:
				r += (2 ** (n - i - 1))
		return r
	else:
		x_out = np.zeros(len(x), dtype = int)
		for i in range(len(x)):
			x_out[i] = x[bit_reverse(i, n)]
		return x_out

def mNTT(N, M, alpha = None):
	if alpha != None:
		if not is_primitive(alpha, N, M):
			print('given alpha is not primitive')
			return
	alpha = find_primitive(N, M)
	if alpha == 0:
		print('no primitive root exist')
		return

	modpow_table = np.zeros(N, dtype=np.int64)

	A = np.zeros((N, N), dtype=np.int64)
	for i in range(N):
		for j in range(N):
			power = (i*j) % N
			if modpow_table[power] != 0:
				A[i][j] = modpow_table[power]
			else:
				A[i][j] = modpow(alpha, power, M)
				modpow_table[power] = A[i][j]

	B = np.zeros((N, N), dtype=np.int64)
	for i in range(N):
		for j in range(N):
			power = (-i*j) % N
			if modpow_table[power] != 0:
				B[i][j] = modpow_table[power]
			else:
				B[i][j] = modpow(alpha, power, M)
				modpow_table[power] = B[i][j]

	Ninv = findinv(N, M)
	for i in range(N):
		for j in range(N):
			B[i][j] = modmult(B[i][j], Ninv, M)

	return A, B

def CT_Butterfly(x_out, x_in, twiddle_factor, M, length):
	if length <= 1:
		x_out[0] = x_in[0]
		return x_out
	halflen = length >> 1
	for i in range(halflen):
		a = x_in[i]
		bc = modmult(x_in[i+halflen], twiddle_factor, M)
		x_out[i] = a + bc
		x_out[i + halflen] = a - bc
	return x_out

class fNTT:
	def __init__(self, N, M, alpha = None):
		self.N = N
		self.M = M
		self.Nlen = int(np.log2(N))
		self.Ninv = findinv(self.N, self.M)
		if alpha != None:
			if not is_primitive(alpha, N, M):
				print('given alpha is not primitive')
				raise ValueError
		else:
			alpha = find_primitive(N, M)
			if alpha == 0:
				print('no primitive root exist')
				raise ValueError
		self.alpha = alpha
		self.alpha_modpow_table = np.zeros(N+1, dtype = int)
		for i in range(N+1):
			self.alpha_modpow_table[i] = modpow(alpha, i, M)

		self.bit_reverse_table = np.zeros(N // 2, dtype = int)
		for i in range(N // 2):
			self.bit_reverse_table[i] = bit_reverse(i, self.Nlen - 1)

	def forward(self, x_in):
		if len(x_in) != self.N:
			print(f'input should be sized {self.N}')
			return
		x = np.copy(x_in)
		for i in range(self.Nlen):
			n = 1 << i
			seqlen = self.N // n
			for j in range(n):
				twiddle_factor = self.alpha_modpow_table[self.bit_reverse_table[j]]
				CT_Butterfly(x[seqlen*j: seqlen*(j+1)], x[seqlen*j: seqlen*(j+1)], twiddle_factor, self.M, seqlen)		
		x = [i % self.M for i in x]
		return bit_reverse(x, self.Nlen)

	def inverse(self, x_in):
		if len(x_in) != self.N:
			print(f'input should be sized {self.N}')
			return
		x = np.copy(x_in)
		for i in range(self.Nlen):
			n = 1 << i
			seqlen = self.N // n
			for j in range(n):
				twiddle_factor = self.alpha_modpow_table[self.N - self.bit_reverse_table[j]]
				CT_Butterfly(x[seqlen*j: seqlen*(j+1)], x[seqlen*j: seqlen*(j+1)], twiddle_factor, self.M, seqlen)		
		
		x = [modmult(i, self.Ninv, self.M) for i in x]
		return bit_reverse(x, self.Nlen)


if __name__ == '__main__':
	ntt = fNTT(16, 17)
	# test input
	x = np.array([-1, -6, -2, 5, -7, 8, -5, 8, 0, 0, 0, 0, 0, 0, 0, 0])

	# output, should be [0, 9, 10, 11, 9, 6, 2, 7, 4, 12, 12, 2, 6, 13, 0, 0]
	y = ntt.forward(x)
	print(y)

	# inverse back, should be the same as test input
	xb = ntt.inverse(y)
	print(xb)
