import numpy as np
import os, sys
sys.path.insert(0, os.path.pardir)
import src.helpers as lib
from src.server import Server
from src.fcfs import FCFS
from src.rr import RR
from src.cgc import CGC

"""Server departures the arrivals for the next server"""
Distribution = 'p'
Q = [[0] * 0, [0] * 0, [0] * 0]
N = 2
LD = [[0] * 10, [0] * 10, [0] * 10]
AI =[5,5,5]
I = 3
C = 25
S = 2

# Determine arrivals
A = [0] * I
if Distribution == 'p':
    for i in range(I):
        A[i] = np.random.poisson(AI[i])
else:
    for i in range(I):
        A[i] = AI[i]

FCFS = []
RRS = []
CGCS = []

for i in range(S):
    FCFS.append(Server(C, i))
    RRS .append(Server(C, i))
    CGCS.append(Server(C, i))

for n in range(N):
    Af = list(A)
    Ar = list(A)
    Ac = list(A)

    # Servers
    for s in range(S):
        FCFS(FFS[s], Af, n)
        print('FCFS','Period:', n, 'Server %s' % (s + 1) , 'Last Departures:', FCFS[s].LD)
        Af = FFS[s].LD

        RR(RRS[s], Ar, n)
        print('RR', 'Period:', n, 'Server %s' % (s + 1) , 'Last Departures:', RRS[s].LD)
        Ar = RRS[s].LD

        CGC(CGCS[s], Ac, n)
        print('CGC', 'Period:', n, 'Server %s' % (s + 1), 'Last Departures:', CGCS[s].LD)
        Ac = CGCS[s].LD
