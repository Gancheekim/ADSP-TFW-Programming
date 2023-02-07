import numpy as np
from tqdm import tqdm
import time
from argparse import ArgumentParser, Namespace
# from NTT import *
from convolve import *

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
parameter_set = [(16, 17, 3, 1), (16, 8380417, 2883726, 723), (512, 8380417, 1753, 127)]
parameter_used = args.parameter_set
if args.N != None and args.M != None:
	N, M, alpha = args.N, args.M, args.alpha
	s = int((q // N) ** 0.5)
else:
	if args.N != None or args.M != None or args.alpha != None:
		print("[Warning] Not enough parameters are given, so a default parameter set is used")
	parameter = parameter_set[parameter_used]
	N, M, alpha, s = parameter

print(f"Testing convolution with sequence length {N // 2} {Round} rounds")
print()

ntt = fNTT(N, M, alpha)

fNTT_convolve_t1 = time.time()

for i in tqdm(range(Round)):
	x = np.random.randint(0, s+1, size = (N // 2))
	y = np.random.randint(0, s+1, size = (N // 2))
	z_ntt = convolve(x, y, ntt)

fNTT_convolve_t2 = time.time()

print(f"It takes {fNTT_convolve_t2 - fNTT_convolve_t1} to do convolution via NTT {Round} rounds")
print()

direct_convolve_t1 = time.time()

for i in tqdm(range(Round)):
	x = np.random.randint(0, s+1, size = (N // 2))
	y = np.random.randint(0, s+1, size = (N // 2))
	z_direct = convolve(x, y)

direct_convolve_t2 = time.time()

print(f"It takes {direct_convolve_t2 - direct_convolve_t1} to do convolution directly {Round} rounds")
print()

