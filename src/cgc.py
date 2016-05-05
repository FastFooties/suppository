# Contested Garment Consistent
import src.helpers as lib

# Half the sum of the claims (determine y)
def halfTheSumOfTheClaims (I, Q):
    return lib.sumQ(I, Q) / 2

# Determine rule (determine x)
def exceedsServerCapacity (I, c, Q):
    return c > halfTheSumOfTheClaims(I, Q)

def CGC (s, A, n):
    s.LR = list(s.R)

    # Start with equal split
    c = s.c
    s.R = [c / s.I] * s.I
    x = 0.0

    # First rule
    if not exceedsServerCapacity(s.I, c, s.Q):
        rule = 1
        r = 0.0                        # Remainder
        for i in range(s.I):
            ri = r / (s.I - i)         # Queue remainder
            r -= ri                    # Use queue remainder

            lenQi = float(len(s.Q[i]))
            value = s.R[i] + ri
            limit = lenQi / 2          # Upper bound
            delta = value - limit

            if delta > 0:
                r += delta
                value = limit

            value, rest = lib.roundRest(value)
            x += rest
            s.R[i] = value

        x += r                         # Add remainder from last queue

    # Second rule
    else:
        rule = 2
        loss = (lib.sumQ(s.I, s.Q) - c) / s.I # Distributed loss
        r = 0.0                        # Remainder
        for i in range(s.I):
            ri = r / (s.I - i)         # Queue remainder
            r -= ri                    # Use queue remainder

            lenQi = float(len(s.Q[i]))
            value = loss + ri
            limit = lenQi / 2          # Lower bound
            delta = value - limit

            if delta > 0:
                r += delta
                value = limit
            else:
                value = lenQi - value

            value, rest = lib.roundRest(value)
            x += rest
            s.R[i] = value

        x -= r                         # Remove remainder from last queue

    lib.correctR(s, round(x))

    s.LD = lib.determineNumberOfJobsInQ(s)

    s.OR = s.R
    s.P.append(lib.sumQ(s.I, s.Q) + sum(A)) # Total length queue
    s.rule = rule

    lib.addArrivals(s, A)
    lib.increaseTIQ(s)
