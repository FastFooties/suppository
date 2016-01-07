import sys
sys.path.append('/usr/lib/python2.7/dist-packages')

import numpy as np
import math
import matplotlib.pylab as plt

np.random.seed(3)

# Configuration
I = 3
AI = [[8, 1], [10, 2], [50, 3]]
N = 3
S = np.random.normal(50, 5, N)

# Other variables
Q = np.empty(I)
R = np.empty(I)
S = [math.trunc(s) for s in S]
WIP = 0
TH = 0
CT = 0

# Half the sum of the claims (determine y)
def halfTheSumOfTheClaims (Q):
    return sum(Q) / 2

# Applicational rule (determine x)
def exceedsServerCapacity (Q, n):
    return S[n] > halfTheSumOfTheClaims(Q)

for n in range(0, N):
    # Determine arrivals
    A = np.empty(I)
    for i in range(0, I):
        A[i] = np.random.normal(AI[i][0], AI[i][1])
    A = [math.trunc(a) for a in A]

    # Determine claims
    for i in range(0, I):
        Q[i] = max(Q[i] + A[i] - R[i], 0)

    # Equal split
    for i in range(0, I):
        R[i] = S[n] / I

    # First rule
    if not exceedsServerCapacity(Q, n):
        r = 0                          # Remainder
        for i in range(0, I):
            ri = r / (I - i)           # Queue remainder
            r -= ri                    # Use queue remainder

            value = R[i] + ri
            limit = Q[i] / 2           # Upper bound
            delta = value - limit

            if delta > 0:
                r += delta
                value = limit

            R[i] = math.floor(value)

    # Second rule
    else:
        loss = (sum(Q) - S[n]) / I     # Distributed loss
        r = 0                          # Remainder
        for i in range(0, I):
            ri = r / (I - i)           # Queue remainder
            r -= ri                    # Use queue remainder

            value = loss + ri
            limit = Q[i] / 2           # Lower bound
            delta = value - limit

            if delta > 0:
                r += delta
                value = limit
            else:
                value = Q[i] - value

            R[i] = math.floor(value)

    # Calculate departures
    D = sum(R)

    # Determine total jobs in queue
    WIP += sum(Q)

    # Determine throughput
    TH += D

    # Dump
    print('Sn', S[n])
    print('A', A)
    print('Q', Q)
    print('Rule', 2 if exceedsServerCapacity(Q, n) else 1)
    print('R', R)
    print('D', D)
    print('---')

# Totals
WIP = WIP / N
TH = TH / N
CT = WIP / TH

print('WIP', WIP)
print('TH', TH)
print('CT', CT)
