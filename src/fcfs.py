# First Come, First Served
import src.helpers as lib

def FCFS (s, A, n):
    s.LR = list(s.R)

    # Determine results
    s.R = [0.0 for r in s.R]
    c = s.c
    offset = 0
    indexes = [0 for r in s.R]
    r = 0.0

    while c > 0:
        # First rule: handle longest waiting job
        high = 0
        queues = []
        for i in range(s.I):
            i = (i + offset) % s.I     # Round-Robin cycle
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
            r += 1

        c -= 1
        offset += 1                    # RR

    lib.correctR(s, r)

    s.LD = lib.determineNumberOfJobsInQ(s)

    s.OR = s.R
    s.P.append(lib.sumQ(s.I, s.Q) + sum(A)) # Total length queue

    lib.addArrivals(s, A)
    lib.increaseTIQ(s)
