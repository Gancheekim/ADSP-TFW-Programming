# ------------------------------------------------------------
# Prime Factor Algorithm for DFT
# ------------------------------------------------------------

import numpy as np
import math
import cmath
import time

def prime_factor_dft(x):
  N = x.size
  p = 0

  # find factor of N if any
  for n in range(2, int(math.sqrt(N))+1):
    if N % n == 0:
      p = n
      break

  # perform DFT if N is a prime
  if p == 0:
    m = np.arange(N)
    n = np.arange(N).reshape(N, 1)
    X_matrix = x.reshape(N, 1) * np.exp(complex(0,-1) * 2 * np.pi * m * n / N)
    X = np.sum(X_matrix, axis=0) # sum along n axis
    return X

  # N is not prime, N = p x q
  q = N // p

  # case 1: p is prime to q
  if q % p != 0:
    m = np.arange(p).reshape(p, 1)
    n = np.arange(q)
    G = x[(m*q + n*p) % N]
    G = G.astype('complex128') # convert data type
    for i in range(p):
      G[i,:] = prime_factor_dft(G[i,:])
    for j in range(q):
      G[:,j] = prime_factor_dft(G[:,j]).flatten()

    X = np.zeros(N, dtype='complex128')
    for i in range(p):
      for j in range(q):
        n = (i*q + j*p) % N
        X[n] = G[(i*q) % p, (j*p) % q]
    return X

  # case 2: p is not prime to q
  # require twiddle factor
  m = np.arange(p).reshape(p, 1)
  n = np.arange(q)
  G = x[(m + n*p) % N]
  G = G.astype('complex128') # convert data type
  twiddle = np.exp(complex(0, -1) * 2 * np.pi * m * n / N)
  for i in range(p):
    G[i,:] = prime_factor_dft(G[i,:])
  G *= twiddle
  for j in range(q):
    G[:,j] = prime_factor_dft(G[:,j]).flatten()

  X = np.zeros(N, dtype='complex128')
  for i in range(p):
    for j in range(q):
      n = (i*q + j) % N
      X[n] = G[i,j]
  return X

# test
if __name__ == '__main__':
  x = np.random.rand(3500) * 100
  N = x.size

  # perform DFT directly
  t1 = time.time()
  m = np.arange(N)
  n = np.arange(N).reshape(N, 1)
  X_matrix = x.reshape(N, 1) * np.exp(complex(0,-1) * 2 * np.pi * m * n / N)
  X_dir = np.sum(X_matrix, axis=0) # sum along n axis
  t2 = time.time()
  t_dir = t2 - t1
  print(f'time required for direct DFT: {t_dir} (s)')

  # use prime factor algorithm
  t3 = time.time()
  X_pr = prime_factor_dft(x)
  t4 = time.time()
  t_pr = t4 - t3
  print(f'time required for prime factor algorithm: {t_pr} (s)')
  error = np.abs(X_pr - X_dir)
  print(f'average error: {np.average(error)}')

# ------------------------------
# end
# ------------------------------
