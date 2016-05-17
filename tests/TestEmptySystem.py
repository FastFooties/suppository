import numpy as np
import os, sys
sys.path.insert(0, os.path.pardir)
import src.helpers as lib
from src.server import Server
from src.fcfs import FCFS
from src.rr import RR
from src.cgc import CGC


"""Emptying the system"""
Distribution = "d"
Q = [[0] * 10, [0] * 10, [0] * 10]
N=7
for n in range(N):
    A = [0, 0, 0]
    c = 5
    I = 3
    s = Server(c,I)
    s.Q = list(Q)
    CGC(s, A, 0)
    print('CGC', 'Period:', n, 'Capacity:', c, 'Queue:', Q, 'Arrivals:', A, 'Departures', s.D)

    A = [0, 0, 0]
    Q = [[0] * 10, [0] * 10, [0] * 10]
    c = 5
    I = 3
    s = Server(c,I)
    s.Q = list(Q)
    RR(s, A, 0)
    print('RR', 'Period:', n, 'Capacity:', c, 'Queue:', Q, 'Arrivals:', A, 'Departures', s.D)

    A = [0, 0, 0]
    Q = [[0] * 10, [0] * 10, [0] * 10]
    c = 5
    I = 3
    s = Server(c,I)
    s.Q = list(Q)
    FCFS(s, A, 0)
    print('FCFS', 'Period:', n, 'Capacity:', c, 'Queue:', Q, 'Arrivals:', A, 'Departures', s.D)

