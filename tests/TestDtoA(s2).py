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

    Af = list(A)
    Ar = list(A)
    Ac = list(A)

    # Servers
    for s in range(S):
        FCFS(FFS[s], Af, n)
        #lib.printServer('FCFS %d' % (s + 1), n, FFS[s], Af)
        Af = FFS[s].LD

        RR(RRS[s], Ar, n)
        #lib.printServer('RRS %d' % (s + 1), n, RRS[s], Ar)
        Ar = RRS[s].LD

        CGC(CGCS[s], Ac, n)
        #lib.printServer('CGCS %d' % (s + 1), n, CGCS[s], Ac)
        Ac = CGCS[s].LD

fcfs = Server(C, I)
fcfs.Q = list(Q)
rr = Server(C, I)
rr.Q = list(Q)
cgc = Server(C, I)
cgc.Q = list(Q)

for n in range(N):
    for s in range(S):
        FCFS(fcfs, A, n)
        print('FCFS','Period:', n, 'Server %s' % (s + 1) , 'Last Departures:', fcfs.LD)

        RR(rr, A, n)
        print('RR', 'Period:', n, 'Server %s' % (s + 1) , 'Last Departures:', rr.LD)

        CGC(cgc, A, n)
        print('CGC', 'Period:', n, 'Server %s' % (s + 1), 'Last Departures:', cgc.LD)

