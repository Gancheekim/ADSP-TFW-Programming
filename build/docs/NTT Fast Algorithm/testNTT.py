import numpy as np
from tqdm import tqdm
import time
from argparse import ArgumentParser, Namespace
from NTT import *

parser = ArgumentParser()
parser.add_argument(
    "--round",
    type = int,
    help = "Number of rounds",
    default = 1000,
)
parser.add_argument(
    "--parameter_set",
    type = int,
    help = "Which parameter set to use (0, 1 or 2)",
    default = 0,
)
parser.add_argument(
    "--N",
    type = int,
    help = "Size of transform",
    default = None
)
parser.add_argument(
    "--M",
    type = int,
    help = "Modular number",
    default = None
)
parser.add_argument(
    "--alpha",
    type = int,
    help = "Primitive root to used",
    default = None
)
args = parser.parse_args()

# choose number of test rounds
Round = args.round
# choose which parameter set is used. Format: (N, M, alpha)
parameter_set = [(16, 17, 3), (16, 8380417, 2883726), (512, 8380417, 1753)]
parameter_used = args.parameter_set
if args.N != None and args.M != None:
	N, M, alpha = args.N, args.M, args.alpha
else:
	if args.N != None or args.M != None or args.alpha != None:
		print("[Warning] Not enough parameters are given, so a default parameter set is used")
	parameter = parameter_set[parameter_used]
	N, M, alpha = parameter

print(f"Testing NTT with size {N}, modular {M}  {Round} rounds")
print()

def matmul(A, x, M):
	Ax = np.zeros(A.shape[0])
	for i in range(A.shape[0]):
		for j in range(A.shape[1]):
			Ax[i] += modmult(A[i][j], x[j], M)
	return Ax

fNTT_t1 = time.time()

ntt = fNTT(N, M, alpha)

fNTT_t2 = time.time()

for i in tqdm(range(Round)):
	x = np.random.randint(0, M, size = (N))
	y = ntt.forward(x)
	xb = ntt.inverse(y)

fNTT_t3 = time.time()

print(f"It takes {fNTT_t2 - fNTT_t1} to initialize fNTT")
print(f"It takes {fNTT_t3 - fNTT_t2} to compute fNTT {Round} rounds")
print()

mNTT_t1 = time.time()

A, B = mNTT(N, M, alpha)

mNTT_t2 = time.time()

for i in tqdm(range(Round)):
	x = np.random.randint(0, M, size = (N))
	y = matmul(A, x, M)
	xb = matmul(B, y, M)

mNTT_t3 = time.time()

print(f"It takes {mNTT_t2 - mNTT_t1} to initialize mNTT")
print(f"It takes {mNTT_t3 - mNTT_t2} to compute mNTT {Round} rounds")