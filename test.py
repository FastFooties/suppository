import sys
sys.path.append('/usr/lib/python2.7/dist-packages')

import numpy as np
import math
import matplotlib.pylab as plt

np.random.seed(3)

I = 3
AI = [[8, 1], [10, 2], [50, 3]]
S = np.random.normal(50, 5, I)

Q = np.empty(I)
R = np.empty(I)
N = len(S)
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















"""


#N=5000

A=random.normal(8, 1)


print(A)






Q=










def computeQandD (n):
    for i in range(1, I):
        Q = np.empty(N)
    halfTheSumOfTheClaims(






def computeQandD(A, S):
    N = len(A)
    Q = np.empty(N)
    D = np.zeros_like(A)
    Q[0] = 0
    for n in range(1,N):
        Q[n] = max(Q[n-1]+ A[n] - S[n], 0)
        D[n] = min(Q[n-1] + A[n], S[n])
    return Q, D

def network():
    # station 1
    A1 = randint(0,201,N)
    S1 = randint(0,260,len(A1))
    Q1, D1 = computeQandD(A1, S1)

    # station 2
    A2 = randint(0,201,N)
    S2 = randint(0,260,len(A2))
    Q2, D2 = computeQandD(A2, S2)

    # station 3
    A3 = np.sum([D1,D2], axis =0) #join output of queue 1 and 2
    S3 = randint(0,540,len(A3))
    Q3, D3 = computeQandD(A3, S3)

    # station 4
    A4 = randint(0,201,N)
    S4 = randint(0,301,len(A4))
    Q4, D4 = computeQandD(A4, S4)

    # station 5
    A5 = np.sum([D3,D4], axis =0) #join output of queue 3 and 4
    S5 = randint(0,700,len(A5))
    Q5, D5 = computeQandD(A5, S5)

    # station 6
    A6 = D5/3    #fork 1/3 of station 5
    A6 = A6.astype(int)
    S6 = randint(0,300,len(A6))
    Q6, D6 = computeQandD(A6, S6)

    # station 7
    A7 = D5-A6    #fork the rest of station 5
    S7 = randint(100,400,len(A7))
    Q7, D7 = computeQandD(A7, S7)

    plt.plot(Q1, label="Q1")
    plt.plot(Q2, label="Q2")
    plt.plot(Q3, label="Q3")
    plt.plot(Q4, label="Q4")
    plt.plot(Q5, label="Q5")
    plt.plot(Q6, label="Q6")
    plt.plot(Q7, label="Q7")
    plt.legend()
    plt.show()

N = 5000

network()
"""
