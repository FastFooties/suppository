import os, sys
sys.path.insert(0, os.path.pardir)
import src.helpers as lib
from src.server import Server
from src.rr import RR
from src.cgc import CGC

A = [1, 10, 13]
c = 26
I = 3

print('discipline, capacity, R, expected, valid, CGC rule')

Q = [[0] * 1, [0] * 10, [0] * 16]
e = [1, 10, 15]
s = Server(c, I)
s.Q = list(Q)
RR(s, A, 0)
print('RR', c, s.R, e, s.R == e, s.rule)

Q = [[0] * 2, [0] * 11, [0] * 14]
e = [2, 10, 14]
s = Server(c, I)
s.Q = list(Q)
CGC(s, A, 0)
print('CGC', c, s.R, e, s.R == e, s.rule)
