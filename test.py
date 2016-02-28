import numpy as np
import math
import matplotlib.pylab as plt

np.random.seed(3)

# Configuration
I = 3
AI = [3, 8, 16]
N = 5000
C = np.empty(N)
C.fill(sum(AI))
#C = np.random.poisson(50, N)

# Other variables
Qf = [[] for q in range(0, I)]
Rf = np.empty(I)
Rf.fill(0)
Df = [[] for q in range(0, I)]
FF_WIP = 0.0
FF_TH = 0.0
Pf = []

Qr = [[] for q in range(0, I)]
Rr = np.empty(I)
Rr.fill(0)
Dr = [[] for q in range(0, I)]
RR_WIP = 0.0
RR_TH = 0.0
Pr = []

Qc = [[] for q in range(0, I)]
Rc = np.empty(I)
Rc.fill(0)
Dc = [[] for q in range(0, I)]
CGC_WIP = 0.0
CGC_TH = 0.0
Pc = []

# Increase time in queue per period
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

    return (Q, D)

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
def FCFS (Q, A, R, D, n):
    Q, D = determineNumberOfJobsInQ(Q, A, R, D)

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

    return (Q, R, D)

# > Round Robin
def RR (Q, A, R, D, n):
    Q, D = determineNumberOfJobsInQ(Q, A, R, D)

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

    return (Q, R, D)

# > Contested Garment Consistent

# Half the sum of the claims (determine y)
def halfTheSumOfTheClaims (Q):
    return sumQ(Q) / 2

# Determine rule (determine x)
def exceedsServerCapacity (Q, n):
    return C[n] > halfTheSumOfTheClaims(Q)

def CGC (Q, A, R, D, n):
    Q, D = determineNumberOfJobsInQ(Q, A, R, D)

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

    return (Q, R, D, rule)

# Test
total = 0.0
for n in range(0, N):
    # Determine arrivals
    A = np.empty(I)
    for i in range(0, I):
        A[i] = np.random.poisson(AI[i])

    total += sum(A)

    # FCFS
    Qf = increaseTIQ(Qf)
    Qf, Rf, Df = FCFS(Qf, A, Rf, Df, n)

    FF_WIP += sumQ(Qf)

    Pf.append(sumQ(Qf))

    # RR
    Qr = increaseTIQ(Qr)
    Qr, Rr, Dr = RR(Qr, A, Rr, Dr, n)

    RR_WIP += sumQ(Qr)

    Pr.append(sumQ(Qr))

    # CGC
    Qc = increaseTIQ(Qc)
    Qc, Rc, Dc, rule =  CGC(Qc, A, Rc, Dc, n)

    CGC_WIP += sumQ(Qc)

    Pc.append(sumQ(Qc))

    # Dump
    """
    print('Cn', C[n])
    print('A', A)
    print('Qf', Qf)
    #print('Df', Df)
    print('sum Df', countD(Df))
    print('Qr', Qr)
    #print('Dr', Dr)
    print('sum Dr', countD(Dr))
    print('Qc', Qc)
    #print('Dc', Dc)
    print('sum Dc', countD(Dc))
    print('Rule', rule)
    print('---')
    print('Rf', Rf)
    print('Rr', Rr)
    print('Rc', Rc)
    """

print(total)
print(countD(Df))
print(countD(Dr))
print(countD(Dc))
# Totals FCFS
FF_WIP = FF_WIP / N
FF_TH = countD(Df) / N
FF_CT = FF_WIP / FF_TH

print('FCFS ---')
print('WIP', FF_WIP)
print('TH', FF_TH)
print('CT', FF_CT)
#print('D', Df)
print('Davg', averageD(Df))
print('stdDev', stdDev(Df))
print('CV', CV(Df))

# Totals RR
RR_WIP = RR_WIP / N
RR_TH = countD(Dr) / N
RR_CT = RR_WIP / RR_TH

print('RR ---')
print('WIP', RR_WIP)
print('TH', RR_TH)
print('CT', RR_CT)
#print('D', Dr)
print('Davg', averageD(Dr))
print('stdDev', stdDev(Dr))
print('CV', CV(Dr))

# Totals CGC
CGC_WIP = CGC_WIP / N
CGC_TH = countD(Dc) / N
CGC_CT = CGC_WIP / CGC_TH

print('CGC ---')
print('WIP', CGC_WIP)
print('TH', CGC_TH)
print('CT', CGC_CT)
#print('D', Dc)
print('Davg', averageD(Dc))
print('stdDev', stdDev(Dc))
print('CV', CV(Dc))

plt.plot(Pf, label = "length queue FCFS")
plt.plot(Pr, label = "length queue RR")
plt.plot(Pc, label = "length queue CGC")
plt.legend()
plt.show()
