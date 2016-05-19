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
Q = [[0] * 4, [0] * 12, [0] * 12]
N = 7
A = [0, 0, 0]
I = 3
C = 6

fcfs = Server(C, I)
fcfs.Q = list(Q)
rr = Server(C, I)
rr.Q = list(Q)
cgc = Server(C, I)
cgc.Q = list(Q)

for n in range(N):
    RR(rr, A, n)
    print('RR', 'Period:', n, 'Capacity:', rr.c, 'Queue:', rr.Q, 'Results:', rr.R)

