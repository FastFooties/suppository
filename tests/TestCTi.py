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
Q = [[1] * 1, [1] * 3, [1] * 5]
Qo = [[1] * 8]
N = 7
A = [0, 0, 0]
I = 3
C = 6

first = Server(C, I)
first.Q = list(Q)
second = Server(C, I)
second.Q = list(Q)
third = Server(C, I)
third.Q = list(Q)
single = Server(C, 1)
single.Q = Qo

def run (s):
    s.LD = lib.determineNumberOfJobsInQ(s)
    s.OR = s.R
    #lib.addArrivals(s, A)
    s.P.append(lib.sumQ(s.I, s.Q)) # Total length queue
    lib.increaseTIQ(s)
    return list(s.Q)

def CTi (results):
    length = len(results[0])
    CT = [0.0] * length

    for i in range(length):
        total = 0
        for result in results:
            for val in result[i]:
                CT[i] += val
                total += 1

        CT[i] /= total

    return CT

def runWithR (s, R):
    results = []
    for i in range(len(R)):
        s.R = R[i]
        results.append(run(s))
    print(results)
    CT = CTi(results)
    print(CT)
    print(sum(CT) / len(CT))

runWithR(first, [
    [0, 0, 0],
    [1, 1, 4],
    [0, 2, 1]
])
runWithR(second, [
    [0, 0, 0],
    [0, 2, 4],
    [1, 1, 1]
])
runWithR(third, [
    [0, 0, 0],
    [0, 3, 3],
    [1, 0, 2]
])
runWithR(single, [
    [6],
    [3]
])
