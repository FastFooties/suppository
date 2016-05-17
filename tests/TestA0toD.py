import numpy as np
import os, sys
sys.path.insert(0, os.path.pardir)
import src.helpers as lib
from src.server import Server
from src.fcfs import FCFS
from src.rr import RR
from src.cgc import CGC

"""Number of departures with no arrivals"""
Distribution = "d" 
A = [0, 0, 0]
Q = [[0] * 0, [0] * 0, [0] * 0]
c = 15
I = 3
s = Server(c,I)
s.Q = list(Q)
CGC(s, A, 0)
print('CGC', 'Capacity:', c, 'Queue:', Q, 'Arrivals:', A, 'Departures', s.D)

A = [0, 0, 0]
Q = [[0] * 0, [0] * 0, [0] * 0]
c = 15
I = 3
s = Server(c,I)
s.Q = list(Q)
RR(s, A, 0)
print('RR', 'Capacity:', c, 'Queue:', Q, 'Arrivals:', A, 'Departures', s.D)

A = [0, 0, 0]
Q = [[0] * 0, [0] * 0, [0] * 0]
c = 15
I = 3
s = Server(c,I)
s.Q = list(Q)
FCFS(s, A, 0)
print('FCFS', 'Capacity:', c, 'Queue:', Q, 'Arrivals:', A, 'Departures', s.D)

