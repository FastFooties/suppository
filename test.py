import numpy as np
import matplotlib.pylab as plt
import src.helpers as lib
from src.server import Server
from src.fcfs import FCFS
from src.rr import RR
from src.cgc import CGC

configs = [
    [1],
    [3],
    [5],
    [7]
]

print('fai;queue;CTq_a;CTq_b;CTq_c;CV_a;CV_b;CB_c')

for config in configs:
    np.random.seed(3) # Random number generator

    # Configuration
    I = 3                   # Number of Queues
    AI = [config[0], 7, 16] # Average arrivals
    N = 5000                # Number of Periods
    S = 1                   # Number of servers
    plotServer = 1          # Which server plot

    # Servers
    N = N + 1
    plotServer = min(plotServer,S)
    ra = sum(AI)
    #print(ra)

    FFS = []
    RRS = []
    CGCS = []
    c = np.ceil(ra + 1)  # Determine capacity of servers

    #print('Capacity', c)
    #print('')

    te = 1 / c
    #print(te)

    for i in range(S):
        FFS .append(Server(c, I))
        RRS .append(Server(c, I))
        CGCS.append(Server(c, I))
        c -= 1                  # Determine capacity of subsequent servers

    # Test
    for n in range(N):
        #print('=== Period %d ===' % (n + 1))

        # Determine arrivals
        A = [0] * I
        for i in range(I):
            A[i] = np.random.poisson(AI[i])

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

    # Totals
    def printResults (label, s):
        global config
        WIP = float(sum(s.P)) / N
        output = '%d;%s;' % (config[0], label)
        output += ';'.join(map(str, lib.averageD(s)))
        output += ';'
        output += ';'.join(map(str, lib.CV(s)))
        print(output)

    # > Totals FCFS
    for i in range(S):
        s = FFS[i]
        printResults('FCFS s%s' % (i + 1), s)

    # > Totals RR
    for i in range(S):
        s = RRS[i]
        printResults('RR s%s' % (i + 1), s)

    # > Totals CGC
    for i in range(S):
        s = CGCS[i]
        printResults('CGC s%s' % (i + 1), s)
