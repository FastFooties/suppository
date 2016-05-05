# Round Robin
import src.helpers as lib

def RR (s, A, n):
    s.LR = list(s.R)

    # Start with equal split
    s.R = [s.c / s.I for r in s.R]

    # Divide overcapacity onto other queues
    r = 0.0
    for i in range(s.I):
        ri = r / (s.I - i)             # Queue remainder
        r -= ri                        # Use queue remainder

        lenQi = len(s.Q[i])
        value = s.R[i] + ri
        limit = lenQi                  # Upper bound
        delta = value - limit

        if delta > 0:
            r += delta
            value = limit

        value, rest = lib.roundRest(value)
        r += rest
        s.R[i] = value

    lib.correctR(s, round(r))

    s.LD = lib.determineNumberOfJobsInQ(s)

    s.OR = s.R
    s.P.append(lib.sumQ(s.I, s.Q) + sum(A)) # Total length queue

    lib.addArrivals(s, A)
    lib.increaseTIQ(s)
