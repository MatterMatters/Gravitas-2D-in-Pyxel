import numpy as np
import vec

class Body: 

    def __init__(self, m, pos, r, v, a, col):
        self.m = m
        self.pos = pos
        self.r = r
        self.v = v
        self.a = a
        self.col = col