import numpy as np
import os, sys
sys.path.insert(0, os.path.pardir)
import src.helpers as lib
from src.server import Server
from src.fcfs import FCFS
from src.rr import RR
from src.cgc import CGC

"""Emptying the system"""
Distribution = 'p'
Q = [[0] * 10, [0] * 10, [0] * 10]
N = 7
A = [0, 0, 0]
I = 3
C = 5

fcfs = Server(C, I)
fcfs.Q = list(Q)
rr = Server(C, I)
rr.Q = list(Q)
cgc = Server(C, I)
cgc.Q = list(Q)

for n in range(N):
    FCFS(fcfs, A, n)
    print('FCFS', 'Period:', n, 'Capacity:', fcfs.c, 'Queue:', fcfs.Q, 'Arrivals:', A, 'Departures', fcfs.D)

    RR(rr, A, n)
    print('RR', 'Period:', n, 'Capacity:', rr.c, 'Queue:', rr.Q, 'Arrivals:', A, 'Departures', rr.D)

    CGC(cgc, A, n)
    print('CGC', 'Period:', n, 'Capacity:', cgc.c, 'Queue:', cgc.Q, 'Arrivals:', A, 'Departures', cgc.D)
