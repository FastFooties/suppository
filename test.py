import sys
sys.path.append('/usr/lib/python2.7/dist-packages')

import numpy as np
import numpy.random as random
import matplotlib.pylab as plt

np.random.seed(3)

Q = [100.0, 200.0, 300.0]
Qs = sum(Q)
I = len(Q)
S = [100.0, 150.0, 200.0, 300.0, 400.0, 500.0, 600.0]
N = len(S)
M = 1000000000

# Determine y
def halfTheSumOfTheClaims (Q):
    return Qs / 2

y = halfTheSumOfTheClaims(Q)

# Applicational rule
def exceedsServerCapacity (n):
    return S[n] > y

# First step
R = []

for n in range(0, N):
    Rn = []
    for i in range(0, I):
        Rn.append(S[n] / I)
    R.append(Rn)

print(R)

for n in range(0, N):
    # First rule
    if not exceedsServerCapacity(n):
        r = 0                          # Remainder
        for i in range(0, I):
            ri = r / (I - i)           # Queue remainder
            r -= ri                    # Use queue remainder

            value = R[n][i] + ri
            limit = Q[i] / 2           # Upper bound
            delta = value - limit

            if delta > 0:
                r += delta
                R[n][i] = limit
            else:
                R[n][i] = value

    # Second rule
    else:
        loss = (Qs - S[n]) / I         # Distributed loss
        r = 0                          # Remainder
        for i in range(0, I):
            ri = r / (I - i)           # Queue remainder
            r -= ri                    # Use queue remainder

            value = loss + ri
            limit = Q[i] / 2           # Lower bound
            delta = value - limit

            if delta > 0:
                r += delta
                R[n][i] = limit
            else:
                R[n][i] = Q[i] - value

print(R)
















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
