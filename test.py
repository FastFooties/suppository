import numpy as np
import math
import matplotlib.pylab as plt

np.random.seed(3)

# Configuration
I = 3
AI = [[8, 1], [10, 2], [30, 3]]
N = 50
#S = np.random.normal(50, 5, N)
S = np.empty(N)
S.fill(29)

# Other variables
S = [math.trunc(s) for s in S]

Qr = np.empty(I)
Rr = np.empty(I)
RR_WIP = 0
RR_TH = 0

Qc = np.empty(I)
Rc = np.empty(I)
CGC_WIP = 0
CGC_TH = 0

# Half the sum of the claims (determine y)
def halfTheSumOfTheClaims (Q):
    return sum(Q) / 2

# Applicational rule (determine x)
def exceedsServerCapacity (Q, n):
    return S[n] > halfTheSumOfTheClaims(Q)

# Determine number of jobs in queue
def determineNumberOfJobsInQ (A, Q, R):
    for i in range(0, I):
        Q[i] = max(Q[i] + A[i] - R[i], 0)
    return Q

# Distribution algorithms
def RR (A, Q, R, n):
    Q = determineNumberOfJobsInQ(A, Q, R)

    # Start with equal split
    R = [S[n] / I for r in R]

    # Divide over capacity into other queues
    r = 0
    for i in range(0, I):
        ri = r / (I - i)               # Queue remainder
        r -= ri                        # Use queue remainder

        value = R[i] + ri
        limit = Q[i]                   # Upper bound
        delta = value - limit

        if delta > 0:
            r += delta
            value = limit

        R[i] = math.floor(value)

    return (Q, R, sum(R))

def CGC (A, Q, R, n):
    Q = determineNumberOfJobsInQ(A, Q, R)

    # Start with equal split
    R = [S[n] / I for r in R]

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

    return (Q, R, sum(R))

# Test
for n in range(0, N):
    # Determine arrivals
    A = np.empty(I)
    for i in range(0, I):
        A[i] = np.random.normal(AI[i][0], AI[i][1])
    A = [math.trunc(a) for a in A]

    # RR
    Qr, Rr, Dr = RR(A, Qr, Rr, n)

    RR_WIP += sum(Qr)
    RR_TH  += sum(Rr)

    # CGC
    Qc, Rc, Dc =  CGC(A, Qc, Rc, n)

    CGC_WIP += sum(Qc)
    CGC_TH  += sum(Rc)

    # Dump
    #"""
    print('Sn', S[n])
    print('A', A)
    print('Qr', Qr)
    print('Rr', Rr)
    print('Dr', Dr)
    print('Qc', Qc)
    print('Rc', Rc)
    print('Dc', Dc)
    print('Rule', 2 if exceedsServerCapacity(Qc, n) else 1)
    print('---')
    #"""

# Totals RR
RR_WIP = RR_WIP / N
RR_TH = RR_TH / N
RR_CT = RR_WIP / RR_TH

print('RR ---')
print('WIP', RR_WIP)
print('TH', RR_TH)
print('CT', RR_CT)
print('------')

# Totals RR
CGC_WIP = CGC_WIP / N
CGC_TH = CGC_TH / N
CGC_CT = CGC_WIP / CGC_TH

print('CGC ---')
print('WIP', CGC_WIP)
print('TH', CGC_TH)
print('CT', CGC_CT)
print('------')
