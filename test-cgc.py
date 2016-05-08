import os, sys
sys.path.insert(0, os.path.pardir)
import src.helpers as lib
from src.server import Server
from src.cgc import CGC

A = [0, 0, 0]
Q = [[0] * 100, [0] * 200, [0] * 300]
C = range(0, 600 + 1, 50) # inclusive
I = 3
E = [
    [0, 0, 0],
    [16, 16, 18],
    [33, 33, 34],
    [50, 50, 50],
    [50, 75, 75],
    [50, 100, 100],
    [50, 100, 150],
    [50, 100, 200],
    [50, 125, 225],
    [50, 150, 250],
    [66, 166, 268],
    [83, 183, 284],
    [100, 200, 300]
]

print('Q=', lib.lenQ(I, Q))
print('C=', C)
print('I=', I)
print('capacity, R, expected, valid, CGC rule')

for i in range(len(C)):
    c = C[i]
    e = E[i]
    s = Server(c, I)
    s.Q = list(Q)
    CGC(s, A, i)
    print(c, s.R, e, s.R == e, s.rule)
