import numpy as np
import matplotlib.pylab as plt

np.random.seed(3)

# Configuration
I = 3
AI = [[8, 1], [10, 2], [30, 3]]
N = 50
S = np.empty(N)
S.fill(48)
#S = np.random.normal(50, 5, N)

# Other variables
Qf = [[] for q in range(0, I)]
Rf = np.empty(I)
Rf.fill(0)
Df = [[] for q in range(0, I)]
FF_WIP = 0.0
FF_TH = 0.0

Qr = [[] for q in range(0, I)]
Rr = np.empty(I)
Rr.fill(0)
Dr = [[] for q in range(0, I)]
RR_WIP = 0.0
RR_TH = 0.0

Qc = [[] for q in range(0, I)]
Rc = np.empty(I)
Rc.fill(0)
Dc = [[] for q in range(0, I)]
CGC_WIP = 0.0
CGC_TH = 0.0

# Increase time in queue
def increaseTIQ (Q):
    for i in range(0, I):
        for q in range(0, len(Q[i])):
            Q[i][q] += 1

    return Q

# Sum of queue
def sumQ (Q):
    total = 0

    for i in range(0, I):
        total += len(Q[i])

    return total

# Half the sum of the claims (determine y)
def halfTheSumOfTheClaims (Q):
    return sumQ(Q) / 2

# Applicational rule (determine x)
def exceedsServerCapacity (Q, n):
    return S[n] > halfTheSumOfTheClaims(Q)

# Determine number of jobs in queue
def determineNumberOfJobsInQ (Q, A, R, D):
    for i in range(0, I):
        Qi = Q[i]

        # Add arrivals
        for j in range(0, int(round(A[i]))):
            Qi.append(0)

        # No departures
        if R[i] == 0.0:
            continue

        # Depart R[i] amount of jobs from beginning of queue
        if len(Qi) > R[i]:
            r = int(round(R[i]))
            d = Qi[:r]
            Q[i] = Qi[r:]

        # Depart all
        else:
            d = Qi[:]
            Q[i] = []

        D[i] += d

    return (Q, D)

# Avarage departures
def averageD (D):
    avg = np.empty(I)

    for i in range(0, I):
        avg[i] = float(sum(D[i])) / len(D[i])

    return avg

def varianceD (D):
    avg = averageD(D)
    V = []

    for i in range(0, I):
        total = 0

        for d in D[i]:
            total += (D[i][d] - avg[i]) ** 2

        V.append(total / len(D[i]))

    return V

# Distribution algorithms
# > First Come, First Served
def FCFS (Q, A, R, D, n):
    Q, D = determineNumberOfJobsInQ(Q, A, R, D)

    # Determine results
    R = [0 for r in R]
    s = S[n]
    offset = 0
    indexes = [0 for r in R]

    while s > 0:
        # First rule: handle longest waiting job
        high = 0
        queues = []
        for i in range(0, I):
            i = (i + offset) % I       # RR
            Qi = Q[i]
            index = indexes[i]

            # Queue fully handled
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

        # Second rule: handle one of longest waiting jobs with RR
        if len(queues) > 1:
            q = queues[offset % len(queues)]

            # Reset other indexes
            for _, j in enumerate(queues):
                if j != q:
                    indexes[j] -= 1

            R[q] += 1
            s -= 1

        # Only one longest waiting job
        elif len(queues) == 1:
            R[queues[0]] += 1
            s -= 1
        else:
            break                      # No more jobs

        offset += 1                    # RR

    return (Q, R, D)

# > Round Robin
def RR (Q, A, R, D, n):
    Q, D = determineNumberOfJobsInQ(Q, A, R, D)

    # Start with equal split
    R = [S[n] / I for r in R]

    # Divide over capacity into other queues
    r = 0
    for i in range(0, I):
        ri = r / (I - i)               # Queue remainder
        r -= ri                        # Use queue remainder

        value = R[i] + ri
        limit = len(Q[i])              # Upper bound
        delta = value - limit

        if delta > 0:
            r += delta
            value = limit

        R[i] = value

    return (Q, R, D)

# > Contested Garment Consistent
def CGC (Q, A, R, D, n):
    Q, D = determineNumberOfJobsInQ(Q, A, R, D)

    # Start with equal split
    R = [S[n] / I for r in R]

    # First rule
    if not exceedsServerCapacity(Q, n):
        r = 0                          # Remainder
        for i in range(0, I):
            ri = r / (I - i)           # Queue remainder
            r -= ri                    # Use queue remainder

            value = R[i] + ri
            limit = len(Q[i]) / 2      # Upper bound
            delta = value - limit

            if delta > 0:
                r += delta
                value = limit

            R[i] = value

    # Second rule
    else:
        loss = (sumQ(Q) - S[n]) / I    # Distributed loss
        r = 0                          # Remainder
        for i in range(0, I):
            ri = r / (I - i)           # Queue remainder
            r -= ri                    # Use queue remainder

            value = loss + ri
            limit = len(Q[i]) / 2      # Lower bound
            delta = value - limit

            if delta > 0:
                r += delta
                value = limit
            else:
                value = len(Q[i]) - value

            R[i] = value

    return (Q, R, D)

# Test
for n in range(0, N):
    # Determine arrivals
    A = np.empty(I)
    for i in range(0, I):
        A[i] = np.random.normal(AI[i][0], AI[i][1])

    # FCFS
    Qf = increaseTIQ(Qf)
    Qf, Rf, Df = FCFS(Qf, A, Rf, Df, n)

    FF_WIP += sumQ(Qf)
    FF_TH  += sum(Rf)

    # RR
    Qr = increaseTIQ(Qr)
    Qr, Rr, Dr = RR(Qr, A, Rr, Dr, n)

    RR_WIP += sumQ(Qr)
    RR_TH  += sum(Rr)

    # CGC
    Qc = increaseTIQ(Qc)
    Qc, Rc, Dc =  CGC(Qc, A, Rc, Dc, n)

    CGC_WIP += sumQ(Qc)
    CGC_TH  += sum(Rc)

    # Dump
    """
    print('Sn', S[n])
    print('A', A)
    print('Qf', Qf)
    print('Rf', Rf)
    print('Df', Df)
    print('Qr', Qr)
    print('Rr', Rr)
    print('Dr', Dr)
    print('Qc', Qc)
    print('Rc', Rc)
    print('Dc', Dc)
    print('Rule', 2 if exceedsServerCapacity(Qc, n) else 1)
    print('---')
    """

# Totals FCFS
FF_WIP = FF_WIP / N
FF_TH = FF_TH / N
FF_CT = FF_WIP / FF_TH

print('FCFS ---')
print('WIP', FF_WIP)
print('TH', FF_TH)
print('CT', FF_CT)
#print('D', Df)
print('Davg', averageD(Df))
print('V', varianceD(Df))

# Totals RR
RR_WIP = RR_WIP / N
RR_TH = RR_TH / N
RR_CT = RR_WIP / RR_TH

print('RR ---')
print('WIP', RR_WIP)
print('TH', RR_TH)
print('CT', RR_CT)
#print('D', Dr)
print('Davg', averageD(Dr))
print('V', varianceD(Dr))

# Totals CGC
CGC_WIP = CGC_WIP / N
CGC_TH = CGC_TH / N
CGC_CT = CGC_WIP / CGC_TH

print('CGC ---')
print('WIP', CGC_WIP)
print('TH', CGC_TH)
print('CT', CGC_CT)
#print('D', Dc)
print('Davg', averageD(Dc))
print('V', varianceD(Dc))
