import numpy as np
import math
import matplotlib.pylab as plt

np.random.seed(3)       # Random number generator

# Configuration
I = 3                   # Number of Queues
AI = [1, 8, 16]         # Average arrivals
N = 20                  # Number of Periods
S = 1                   # Number of servers
plotServer = 2          # Which server plot

# Servers
N = N + 1
plotServer = min(plotServer,S)
ra = sum(AI)
print(ra)


class Server:
    def __init__ (self, c):
        global I
        self.c = c
        self.Q = [[] for q in range(I)]
        self.OR = None # Original R
        self.R = [0] * I
        self.D = [[] for q in range(I)]
        self.LR = None # Last R
        self.LD = None # Last departures
        self.P = []
        self.rule = None

FFS = []
RRS = []
CGCS = []
c = np.ceil(ra * 1.01)  # Determine capacity of servers

print('Capacity', c)
print('')

te = 1 / c
print(te)

for i in range(S):
    FFS .append(Server(c))
    RRS .append(Server(c))
    CGCS.append(Server(c))
    c -= 1                  # Determine capacity of subsequent servers

# Increase time in queue per period
def increaseTIQ (Q):
    for i in range(I):
        for q in range(len(Q[i])):
            Q[i][q] += 1

# Length of queues
def lenQ (Q):
    totals = []
    for i in range(I):
        totals.append(len(Q[i]))
    return totals

# Sum of queue
def sumQ (Q):
    return sum(lenQ(Q))

# Round with rest
def roundRest (value):
    rounded = math.floor(value)
    return rounded, value - rounded

# Count departures
def countD (D):
    count = 0.0
    for i in range(I):
        count += len(D[i])
    return count

# Determine number of jobs in queue
def determineNumberOfJobsInQ (Q, R, D):
    counts = []

    for i in range(I):
        Qi = Q[i]

        # No departures
        if R[i] == 0.0:
            counts.append(0)
            continue

        # Pick R[i] amount of jobs from beginning of queue
        if len(Qi) > R[i]:
            r = int(R[i])
            d = Qi[:r]
            Q[i] = Qi[r:]

        # Depart all
        else:
            d = Qi[:]
            Q[i] = []

        D[i] += d
        counts.append(len(d))

    return counts

# Add arrivals
def addArrivals (s, A):
    for i in range (I):
        s.Q[i] += [0] * int(A[i])

# Average departures
def averageD (D):
    avg = [0] * I

    for i in range(I):
        avg[i] = float(sum(D[i])) / len(D[i])

    return avg

def stdDev (D):
    avg = averageD(D)
    V = []

    for i in range(I):
        total = 0

        for d in D[i]:
            total += (d - avg[i]) ** 2

        V.append((total / len(D[i])) ** (0.5))

    return V

def CV (D):
    cv = []
    std = stdDev(D)
    avg = averageD(D)

    for i in range(I):
        cv.append(std[i] / avg[i] if avg[i] > 0 else 0.0)

    return cv

# Queueing Disciplines
# > First Come, First Served
def FCFS (s, A, n):
    s.LR = list(s.R)

    # Determine results
    s.R = [0.0 for r in s.R]
    c = s.c
    offset = 0
    indexes = [0 for r in s.R]

    while c > 0:
        # First rule: handle longest waiting job
        high = 0
        queues = []
        for i in range(I):
            i = (i + offset) % I       # Round-Robin cycle
            index = indexes[i]

            # Queue is fully handled
            if index >= len(s.Q[i]):
                continue

            # Multiple longest waiting jobs
            if s.Q[i][index] == high:
                queues.append(i)
                indexes[i] += 1

            # New longest waiting job
            elif s.Q[i][index] > high:
                # Other job found, reset indexes
                for _, j in enumerate(queues):
                    indexes[j] -= 1

                high = s.Q[i][index]
                queues = [i]
                indexes[i] += 1

        # Second rule: handle one of longest waiting jobs using RR
        if len(queues) > 1:
            q = queues[offset % len(queues)]

            # Reset other indexes
            for _, j in enumerate(queues):
                if j != q:
                    indexes[j] -= 1

            s.R[q] += 1

        # Handle longest waiting job only
        elif len(queues) == 1:
            s.R[queues[0]] += 1

        # No more jobs
        else:
            #R[0] += 1
            #R[int(c % I)] += 1
            s.R[I - 1] += 1

        c -= 1
        offset += 1                    # RR

    increaseTIQ(s.Q)
    s.LD = determineNumberOfJobsInQ(s.Q, s.R, s.D)

    #s.Q = Q
    s.OR = s.R
    #s.R = R
    #s.D = D
    s.P.append(sumQ(s.Q))                # Total length queue

    addArrivals(s, A)

# > Round Robin
def RR (s, A, n):
    s.LR = list(s.R)

    # Start with equal split
    s.R = [s.c / I for r in s.R]

    # Divide overcapacity onto other queues
    r = 0.0
    for i in range(I):
        ri = r / (I - i)               # Queue remainder
        r -= ri                        # Use queue remainder

        lenQi = len(s.Q[i])
        value = s.R[i] + ri
        limit = lenQi                  # Upper bound
        delta = value - limit

        if delta > 0:
            r += delta
            value = limit

        value, rest = roundRest(value)
        r += rest
        s.R[i] = value

    #R[0] += int(r)
    #for j in range(int(r)):
    #    R[j % I] += 1
    #s.R[I - 1] += int(r)
    LQ = lenQ(s.Q)
    high = max(LQ)
    for i in range(I):
        if LQ[i] == high:
            s.R[i] += round(r)

    increaseTIQ(s.Q)
    s.LD = determineNumberOfJobsInQ(s.Q, s.R, s.D)

    #s.Q = Q
    s.OR = s.R
    #s.R = R
    #s.D = D
    s.P.append(sumQ(s.Q))                  # Total length queue

    addArrivals(s, A)

# > Contested Garment Consistent

# Half the sum of the claims (determine y)
def halfTheSumOfTheClaims (Q):
    return sumQ(Q) / 2

# Determine rule (determine x)
def exceedsServerCapacity (c, Q):
    return c > halfTheSumOfTheClaims(Q)

def CGC (s, A, n):
    s.LR = list(s.R)

    # Start with equal split
    c = s.c
    R = [c / I for r in s.R]
    x = 0.0

    # First rule
    if not exceedsServerCapacity(c, s.Q):
        rule = 1
        r = 0.0                        # Remainder
        for i in range(I):
            ri = r / (I - i)           # Queue remainder
            r -= ri                    # Use queue remainder

            lenQi = len(s.Q[i])
            value = s.R[i] + ri
            limit = lenQi / 2          # Upper bound
            delta = value - limit

            if delta > 0:
                r += delta
                value = limit

            value, rest = roundRest(value)
            x += rest
            s.R[i] = value

    # Second rule
    else:
        rule = 2
        loss = (sumQ(s.Q) - c) / I       # Distributed loss
        r = 0.0                        # Remainder
        for i in range(I):
            ri = r / (I - i)           # Queue remainder
            ri = r
            r -= ri                    # Use queue remainder

            lenQi = len(s.Q[i])
            value = loss + ri
            limit = lenQi / 2          # Lower bound
            delta = value - limit

            if delta > 0:
                r += delta
                value = limit
            else:
                value = lenQi - value

            value, rest = roundRest(value)
            x += rest
            s.R[i] = value

    #R[0] += round(x)
    #for j in range(int(round(x))):
    #    R[j % I] += 1
    s.R[I - 1] += round(x)

    increaseTIQ(s.Q)
    s.LD = determineNumberOfJobsInQ(s.Q, s.R, s.D)

    #s.Q = Q
    s.OR = s.R
    #s.R = R
    #s.D = D
    s.P.append(sumQ(s.Q))                 # Total length queue
    s.rule = rule

    addArrivals(s, A)

# Test
def printServer (label, s, A):
    OQ = []
    for i in range(I):
        OQ.append(len(s.Q[i]) - A[i])

    print('%s A, Q, R, Q + A, Rc, length Q, LD' % label, A, OQ, s.OR, lenQ(s.Q), s.R, sumQ(s.Q), s.LD)
"""
    print('Period', n)
    print('Server %s' % label)
    print('A', A)
    #print('Sum Arrivals', sum(A))
    print('Q', s.Q)
    print('D', s.D)
    print('P', s.P)
    print('R', s.R)
    print('')
"""


for n in range(N):
    print('=== Period %d ===' % (n + 1))

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
        printServer('FCFS %d' % (s + 1), FFS[s], Af)
        Af = FFS[s].LD

        RR(RRS[s], Ar, n)
        printServer('RRS %d' % (s + 1), RRS[s], Ar)
        Ar = RRS[s].LD

        CGC(CGCS[s], Ac, n)
        printServer('CGCS %d' % (s + 1), CGCS[s], Ac)
        Ac = CGCS[s].LD

# Totals
def printResults (label, s):
    print('Server %d' % (i + 1))
    WIP = float(sum(s.P)) / N
    TH = countD(s.D) / N
    CT = WIP / TH
    print('WIP', WIP)
    print('TH', TH)
    print('CT', CT)
    print('Davg', averageD(s.D))
    print('stdDev', stdDev(s.D))
    print('CV', CV(s.D))
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

# > Totals CGC
print('=== Totals CGC ===')

for i in range(S):
    s = CGCS[i]
    printResults('CGC s%s' % (i + 1), s)
    if i + 1 == plotServer:
        plt.plot(s.P, label = 'length queue CGC S%d' % (i + 1))

# Show plot
plt.legend()
plt.show()
