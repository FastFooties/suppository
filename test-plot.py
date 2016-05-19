import numpy as np
import matplotlib.pylab as plt
import src.helpers as lib
from src.server import Server
from src.fcfs import FCFS
from src.rr import RR
from src.cgc import CGC

np.random.seed(3)       # Random number generator

# Configuration
I = 3                   # Number of Queues
AI = [1, 8, 16]         # Average arrivals
Distribution = "p"      # Poisson Distributed arrivals
c = np.ceil(sum(AI) + 1)# Determine capacity of servers
N = 5000                # Number of Periods
S = 1                   # Number of servers
plotServer = 1          # Which server plot

# Servers
N = N + 1
plotServer = min(plotServer,S)

AI.sort()   #Sort arrivals

FFS = []
RRS = []
CGCS = []

print('=== System Configuration ===')
print('Run Length:', N - 1)
print('Number of Queues:', I)
print('Capacity:', c)
print('Arrivals:', AI)


ra = sum(AI)            # Arrival rate
print('Arrival Rate:', ra)

if c == 0:
    print("")
else:
    te = 1 / c
    print("Effective Process Time:", te)

if ra == 0 or te == 0:
    u = 0
else:
    u = ra * te
print('Utilization: {0:.2%}'.format(u) )
print('')

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

# Totals
def printResults (label, s):
    print('Server %d' % (i + 1))
    WIP = float(sum(s.P)) / N
    TH = lib.countD(s) / N
    if TH == 0:
        CT = "No Value"
        TH = "No Value"
    else:
        CT = WIP / TH
    CTq = 0.5 * u/(1-u) * te
    if te <= 0 or ra <= 0:
        ""
    else:
        print('Upper Limit WIP:', (WIP/ra)/te)
    print('WIP:', WIP)
    if te <= 0 or ra <= 0:
        ""
    else:
        print('Lower Limit WIP:', ((WIP/ra)-1)/te)
    print('TH:', TH)
    print('CT:', CT)
    if ra <= 0:
        ""
    else:
        print('Upper Limit CTq:', (WIP/ra))
    print('CTq:', CTq)
    if ra <= 0:
        ""
    else:
        print('Lower Limit CTq:', (WIP/ra)-1)
    print('CT', CTq + te + 1)
    print('Davg:', lib.averageD(s))
    print('stdDev:', lib.stdDev(s))
    print('CV:', lib.CV(s))
    print('')

# > Totals FCFS
print('=== Totals FCFS ===')

for i in range(S):
    s = FFS[i]
    printResults('FCFS s%s' % (i + 1), s)
    if i + 1 == plotServer:
        plt.plot(s.P, label = 'length queue FCFS S%d' % (i + 1))

# > Totals RR
print('=== Totals RR ===')

for i in range(S):
    s = RRS[i]
    printResults('RR s%s' % (i + 1), s)
    if i + 1 == plotServer:
        plt.plot(s.P, label = 'length queue RR S%d' % (i + 1))

# >Totals CGC
print('=== Totals CGC ===')

for i in range(S):
    s = CGCS[i]
    printResults('CGC s%s' % (i + 1), s)
    if i + 1 == plotServer:
        plt.plot(s.P, label = 'length queue CGC S%d' % (i + 1))
        
"""Total queue length equal over all periods"""
diff = False

for n in range(N):
    for i in range(S):
        a = FFS[i].P[n]
        b = RRS[i].P[n]
        c = CGCS[i].P[n]
        if a != b or a != c:
            print('Difference in Total Queue Length', n, i, a, b, c)
            diff = True

if not diff:
    print('No differences in Total Queue Length')
    print('')

# Show plot
plt.legend()
plt.show()
