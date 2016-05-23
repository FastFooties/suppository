import numpy as np
import os, sys
sys.path.insert(0, os.path.pardir)
import src.helpers as lib
from src.server import Server
from src.fcfs import FCFS
from src.rr import RR
from src.cgc import CGC

np.random.seed(3)       # Random number generator

"""Server departures the arrivals for the next server"""
Distribution = 'p'
Q = [[0] * 0, [0] * 0, [0] * 0]
N = 2
LD = [[0] * 10, [0] * 10, [0] * 10]
AI = [5, 5, 5]
I = 3
C = 25
S = 2

FFS = []
RRS = []
CGCS = []

for i in range(S):
	FFS .append(Server(C, I))
	RRS .append(Server(C, I))
	CGCS.append(Server(C, I))

FFS[0] .Q = list(Q)
RRS[0] .Q = list(Q)
CGCS[0].Q = list(Q)

for n in range(N):
	# Determine arrivals
	A = [0] * I
	if Distribution == 'p':
		for i in range(I):
			A[i] = np.random.poisson(AI[i])
	else:
		for i in range(I):
			A[i] = AI[i]

	Af = list(A)
	Ar = list(A)
	Ac = list(A)

	# Servers
	for s in range(S):
		FCFS(FFS[s], Af, n)
		print('FCFS','Period:', n, 'Server %s' % (s + 1), 'Last Departures:', FFS[s].LD, 'Arrivals:', Af)
		Af = FFS[s].LD

		RR(RRS[s], Ar, n)
		print('RR', 'Period:', n, 'Server %s' % (s + 1), 'Last Departures:', RRS[s].LD, 'Arrivals:', Ar)
		Ar = RRS[s].LD

		CGC(CGCS[s], Ac, n)
		print('CGC', 'Period:', n, 'Server %s' % (s + 1), 'Last Departures:', CGCS[s].LD, 'Arrivals:', Ac)
		Ac = CGCS[s].LD
