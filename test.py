import numpy as np
import math
import matplotlib.pylab as plt

configs = [
    [3, 1]
]
"""
    [3, 1],
    [5, 3],
    [7, 5],
    [9, 8]
"""

print('seed;fai;queue;avgD_a;avgD_b;avgD_c;CV_a;CV_b;CB_c')

for config in configs:
    np.random.seed(config[0])

    # Configuration
    I = 3
    AI = [config[1], 8, 16]
    N = 20
    S = 3 # Number of servers

    # Servers
    class Server:
        def __init__ (self, c):
            global I
            self.c = c
            self.Q = [[] for q in range(0, I)]
            self.R = np.empty(I)
            self.R.fill(0)
            self.D = [[] for q in range(0, I)]
            self.LD = None # Last departures
            self.P = []
            self.rule = None

    FFS = []
    RRS = []
    CGCS = []
    c = float(sum(AI))
    for i in range(0, S):
        FFS .append(Server(c))
        RRS .append(Server(c))
        CGCS.append(Server(c))
        c -= 1

    # Increase time in queue per period
    def increaseTIQ (Q):
        for i in range(0, I):
            for q in range(0, len(Q[i])):
                Q[i][q] += 1

    # Length of queues
    def lenQ (Q):
        totals = []
        for i in range(0, I):
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
        for i in range(0, I):
            count += len(D[i])
        return count

    # Correct R
    def correctR (s, A):
        # Properly assign remainder based on arrivals
        for i in range (0, I):
            delta = s.R[i] - (len(s.Q[i]) + A[i])

            if delta < 1:
                continue

            s.R[i] -= delta

            # Respread overcapacity
            j = 0
            while delta > 0:
                # Don't assign to own queue
                if i != j:
                    s.R[j] += 1
                    delta -= 1

                j = (j + 1) % I # Next queue

    # Determine number of jobs in queue
    def determineNumberOfJobsInQ (Q, A, R, D):
        counts = []

        for i in range(0, I):
            Qi = Q[i]

            # Add arrivals
            for j in range(0, int(A[i])):
                Qi.append(0)

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

    # Average departures
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
                total += (d - avg[i]) ** 2

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
        s.LD = determineNumberOfJobsInQ(Q, A, R, D)

        # Determine results
        R = [0.0 for r in R]
        c = s.c
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
                R[I - 1] += 1

            c -= 1
            offset += 1                    # RR

        s.Q = Q
        s.R = R
        s.D = D
        s.P.append(sumQ(Q))

    # > Round Robin
    def RR (s, A, n):
        correctR(s, A)

        Q = s.Q
        R = s.R
        D = s.D

        increaseTIQ(Q)
        s.LD = determineNumberOfJobsInQ(Q, A, R, D)

        # Start with equal split
        R = [s.c / I for r in R]

        # Divide overcapacity onto other queues
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

            value, rest = roundRest(value)
            r += rest
            R[i] = value

        R[I - 1] += int(r)

        s.Q = Q
        s.R = R
        s.D = D
        s.P.append(sumQ(Q))

    # > Contested Garment Consistent

    # Half the sum of the claims (determine y)
    def halfTheSumOfTheClaims (Q):
        return sumQ(Q) / 2

    # Determine rule (determine x)
    def exceedsServerCapacity (c, Q):
        return c > halfTheSumOfTheClaims(Q)

    def CGC (s, A, n):
        correctR(s, A)

        Q = s.Q
        R = s.R
        D = s.D

        increaseTIQ(Q)
        s.LD = determineNumberOfJobsInQ(Q, A, R, D)

        # Start with equal split
        c = s.c
        R = [c / I for r in R]
        x = 0.0

        # First rule
        if not exceedsServerCapacity(c, Q):
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
            loss = (sumQ(Q) - c) / I       # Distributed loss
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

        R[I - 1] += round(x)

        s.Q = Q
        s.R = R
        s.D = D
        s.P.append(sumQ(Q))
        s.rule = rule

    # Test
    def printServer (label, s, A):
        """
        print('Server %s' % label)
        print('A', A)
        print('Q', s.Q)
        print('D', s.D)
        print('P', s.P)
        print('R', s.R)
        print('')
        """
        print('%s A, R, LD, Q, length Q' % label, A, s.R, s.LD, lenQ(s.Q), s.P[-1])

    for n in range(0, N):
        print('=== Period %d ===' % (n + 1))

        # Determine arrivals
        A = np.empty(I)
        for i in range(0, I):
            A[i] = np.random.poisson(AI[i])

        Af = list(A)
        Ar = list(A)
        Ac = list(A)

        # Servers
        for s in range(0, S):
            FCFS(FFS[s], Af, n)
            printServer('FFS %d' % (s + 1), FFS[s], Af)
            Af = FFS[s].LD

            RR(RRS[s], Ar, n)
            printServer('RRS %d' % (s + 1), RRS[s], Ar)
            Ar = RRS[s].LD

            CGC(CGCS[s], Ac, n)
            printServer('CGCS %d' % (s + 1), CGCS[s], Ac)
            Ac = CGCS[s].LD

    # Totals
    def printResults (label, s):
        global config
        output = '%d;%d;%s;' % (config[0], config[1], label)
        output += ';'.join(map(str, averageD(s.D)))
        output += ';'.join(map(str, CV(s.D)))
        print(output)

    # > Totals FCFS
    for i in range(0, S):
        s = FFS[i]
        printResults('FCFS s%s' % (i + 1), s)

    # > Totals RR
    for i in range(0, S):
        s = RRS[i]
        printResults('RR s%s' % (i + 1), s)

    # > Totals CGC
    for i in range(0, S):
        s = CGCS[i]
        printResults('CGC s%s' % (i + 1), s)
