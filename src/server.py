class Server:
    def __init__ (self, c, I):
        self.c = c
        self.I = I
        self.Q = [[] for q in range(I)]
        self.OR = None # Original R
        self.R = [0] * I
        self.D = [[] for q in range(I)]
        self.LR = None # Last R
        self.LD = None # Last departures
        self.P = []
        self.A = []
        self.rule = None
