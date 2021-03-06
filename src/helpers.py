import math
import operator

# Increase time in queue per period
def increaseTIQ (s):
    for i in range(s.I):
        for q in range(len(s.Q[i])):
            s.Q[i][q] += 1

# Length of queues
def lenQ (I, Q):
    totals = []
    for i in range(I):
        totals.append(len(Q[i]))
    return totals

# Sum of queue
def sumQ (I, Q):
    return sum(lenQ(I, Q))

# Round with rest
def roundRest (value):
    rounded = math.floor(value)
    return rounded, value - rounded

# Count departures
def countD (s):
    count = 0.0
    for i in range(s.I):
        count += len(s.D[i])
    return count

# Correct R
def correctR (s, r):
    # Spread remainder over queues with biggest difference to R value
    while r > 0:
        diff = [i - j for i, j in zip(lenQ(s.I, s.Q), s.R)]
        i, _ = max(enumerate(diff), key=operator.itemgetter(1))
        s.R[i] += 1
        r -= 1

# Determine number of jobs in queue
def determineNumberOfJobsInQ (s):
    counts = []

    for i in range(s.I):
        Qi = s.Q[i]

        # No departures
        if s.R[i] == 0.0:
            counts.append(0)
            continue

        # Pick R[i] amount of jobs from beginning of queue
        if len(Qi) > s.R[i]:
            r = int(s.R[i])
            d = Qi[:r]
            s.Q[i] = Qi[r:]

        # Depart all
        else:
            d = Qi[:]
            s.Q[i] = []

        s.D[i] += d
        counts.append(len(d))

    return counts

# Add arrivals
def addArrivals (s, A):
    s.A.append(sum(A))
    for i in range (s.I):
        s.Q[i] += [0] * int(A[i])

# Average CT of jobs
def averageD (s):
    avg = [0] * s.I

    for i in range(s.I):
        if len(s.D[i]) == 0:
            avg[i] = 0
        else:
            avg[i] = float(sum(s.D[i])) / (len(s.D[i]))

    return avg


# Total CT per queueing discipline
def CTQD (s):
    total = 0
    count = 0
    for d in s.D:
        total += sum(d)
        count += len(d)
    return total / count


def stdDev (s):
    avg = averageD(s)
    V = []

    for i in range(s.I):
        total = 0

        for d in s.D[i]:
            total += (d - avg[i]) ** 2
        if len(s.D[i]) == 0:
            V.append(0)
        else:
            V.append((total / len(s.D[i])) ** (0.5))

    return V

def CV (s):
    cv = []
    std = stdDev(s)
    avg = averageD(s)

    for i in range(s.I):
        cv.append(std[i] / avg[i] if avg[i] > 0 else 0.0)

    return cv


# Print server info
def printServer (label, n, s, A):
    #print('Period', n)
    #print('Server %s' % label)
    #print('A', A)
    #print('Sum Arrivals', sum(A))
    #print('new Q', lenQ(s.I, s.Q))
    #print('sum new Q', sum(lenQ(s.I, s.Q)))
    #print('Q', s.Q)
    #print('D', s.D)
    #print('sum D', countD(s))
    #print('P', s.P)
    #print('R', s.R)
    #print('')
