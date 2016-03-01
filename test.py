import numpy as np
import math
import matplotlib.pylab as plt

np.random.seed(3)

# Configuration
I = 3
AI = [3, 8, 16]
N = 50
C = np.empty(N)
C.fill(sum(AI))
#C = np.random.poisson(50, N)
S = 3 # Number of servers

# Servers
class Server:
    def __init__ (self):
        global I
        self.Q = [[] for q in range(0, I)]
        self.R = np.empty(I)
        self.R.fill(0)
        self.D = [[] for q in range(0, I)]
        self.P = []
        self.rule = None

FFS = []
RRS = []
CGCS = []
for i in range(0, S):
    FFS.append(Server())
    RRS.append(Server())
    CGCS.append(Server())

# Increase time in queue per period
def increaseTIQ (Q):
    for i in range(0, I):
        for q in range(0, len(Q[i])):
            Q[i][q] += 1

# Sum of queue
def sumQ (Q):
    total = 0
    for i in range(0, I):
        total += len(Q[i])
    return total

# Round with rest
def roundRest (value):
    rounded = math.floor(value)
    return rounded, value - rounded

# Count departures
def countD (D):
    count = 0.0
    for i in range(0, I):
        count += len(D[i])
    return count

# Determine number of jobs in queue
def determineNumberOfJobsInQ (Q, A, R, D):
    for i in range(0, I):
        Qi = Q[i]

        # Add arrivals
        for j in range(0, int(A[i])):
            Qi.append(0)

        # No departures
        if R[i] == 0.0:
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

# Avarage departures
def averageD (D):
    avg = np.empty(I)

    for i in range(0, I):
        avg[i] = float(sum(D[i])) / len(D[i])

    return avg

def stdDev (D):
    avg = averageD(D)
    V = []

    for i in range(0, I):
        total = 0

        for d in D[i]:
            total += (D[i][d] - avg[i]) ** 2

        V.append((total / len(D[i])) ** (0.5))

    return V

def CV (D):
    return stdDev(D) / averageD(D)


# Queueing Disciplines
# > First Come, First Served
def FCFS (s, A, n):
    Q = s.Q
    R = s.R
    D = s.D

    increaseTIQ(Q)
    determineNumberOfJobsInQ(Q, A, R, D)

    # Determine results
    R = [0.0 for r in R]
    c = C[n]
    offset = 0
    indexes = [0 for r in R]

    while c > 0:
        # First rule: handle longest waiting job
        high = 0
        queues = []
        for i in range(0, I):
            i = (i + offset) % I       # Round-Robin cycle
            Qi = Q[i]
            index = indexes[i]

            # Queue is fully handled
            if index >= len(Qi):
                continue

            # Multiple longest waiting jobs
            if Qi[index] == high:
                queues.append(i)
                indexes[i] += 1

            # New longest waiting job
            elif Qi[index] > high:
                # Other job found, reset indexes
                for _, j in enumerate(queues):
                    indexes[j] -= 1

                high = Qi[index]
                queues = [i]
                indexes[i] += 1

        # Second rule: handle one of longest waiting jobs using RR
        if len(queues) > 1:
            q = queues[offset % len(queues)]

            # Reset other indexes
            for _, j in enumerate(queues):
                if j != q:
                    indexes[j] -= 1

            R[q] += 1

        # Handle longest waiting job only
        elif len(queues) == 1:
            R[queues[0]] += 1

        # No more jobs
        else:
            R[offset % I] += 1

        c -= 1
        offset += 1                    # RR

    s.Q = Q
    s.R = R
    s.D = D
    s.P.append(sumQ(Q))

# > Round Robin
def RR (s, A, n):
    Q = s.Q
    R = s.R
    D = s.D

    increaseTIQ(Q)
    determineNumberOfJobsInQ(Q, A, R, D)

    # Start with equal split
    R = [C[n] / I for r in R]

    # Divide overcapacity on to other queues
    r = 0.0
    for i in range(0, I):
        ri = r / (I - i)               # Queue remainder
        r -= ri                        # Use queue remainder

        lenQi = len(Q[i])
        value = R[i] + ri
        limit = lenQi                  # Upper bound
        delta = value - limit

        if delta > 0:
            r += delta
            value = limit

        R[i] = value

    for i in range(0, int(r)):
        R[i % I] += 1

    s.Q = Q
    s.R = R
    s.D = D
    s.P.append(sumQ(Q))

# > Contested Garment Consistent

# Half the sum of the claims (determine y)
def halfTheSumOfTheClaims (Q):
    return sumQ(Q) / 2

# Determine rule (determine x)
def exceedsServerCapacity (Q, n):
    return C[n] > halfTheSumOfTheClaims(Q)

def CGC (s, A, n):
    Q = s.Q
    R = s.R
    D = s.D

    increaseTIQ(Q)
    determineNumberOfJobsInQ(Q, A, R, D)

    # Start with equal split
    R = [C[n] / I for r in R]

    x = 0.0

    # First rule
    if not exceedsServerCapacity(Q, n):
        rule = 1
        r = 0.0                        # Remainder
        for i in range(0, I):
            ri = r / (I - i)           # Queue remainder
            r -= ri                    # Use queue remainder

            lenQi = len(Q[i])
            value = R[i] + ri
            limit = lenQi / 2          # Upper bound
            delta = value - limit

            if delta > 0:
                r += delta
                value = limit

            value, rest = roundRest(value)
            x += rest
            R[i] = value

    # Second rule
    else:
        rule = 2
        loss = (sumQ(Q) - C[n]) / I    # Distributed loss
        r = 0.0                        # Remainder
        for i in range(0, I):
            ri = r / (I - i)           # Queue remainder
            ri = r
            r -= ri                    # Use queue remainder

            lenQi = len(Q[i])
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
            R[i] = value

    for i in range(0, int(round(x))):
        R[i % I] += 1

    s.Q = Q
    s.R = R
    s.D = D
    s.P.append(sumQ(Q))
    s.rule = rule

# Test
total = 0.0
for n in range(0, N):
    # Determine arrivals
    A = np.empty(I)
    for i in range(0, I):
        A[i] = np.random.poisson(AI[i])
    total += sum(A)

    Af = list(A)
    Ar = list(A)
    Ac = list(A)

    # Servers
    for s in range(0, S):
        FCFS(FFS[s], Af, n)
        Af = [sum(d) for d in FFS[s].D]

        RR(RRS[s], Ar, n)
        Ar = [sum(d) for d in RRS[s].D]

        CGC(CGCS[s], Ac, n)
        Ac = [sum(d) for d in CGCS[s].D]

# Totals
def printResults (i, s):
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

for i in range(0, S):
    printResults(i, FFS[i])

# > Totals RR
print('=== Totals RR ===')

for i in range(0, S):
    printResults(i, RRS[i])

# > Totals CGC
print('=== Totals CGC ===')

for i in range(0, S):
    printResults(i, CGCS[i])

# Plotting
#plt.plot(Pf, label = "length queue FCFS")
#plt.plot(Pr, label = "length queue RR")
#plt.plot(Pc, label = "length queue CGC")
#plt.legend()
#plt.show()
