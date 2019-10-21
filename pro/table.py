# encoding=utf-8
"""table management module"""


import numpy as np 
import checker
from myio import IO
from random import shuffle


class TableManager:
    def __init__(self, n=8):
        assert 3 <= n and n <= 35
        self.n = n
        if 3 <= self.n and self.n <= 8:
            self.datatype = np.uint16
        elif 8 < self.n and self.n <= 16:
            self.datatype = np.uint32
        elif 16 < self.n and self.n <= 32:
            self.datatype = np.uint64
        else:
            self.datatype = int
        self.en = np.zeros((64, 1<<(2*self.n-1)), dtype=self.datatype)
        self.de = []
        
    def generate_encode(self):
        pq = []
        for i in range(64):
            for j in range(1<<(2*self.n)):
                rl, gc = checker.check(j, 2*self.n)  
                gc = abs(gc-0.5)
                if rl and checker.is_legal_cat(i, j, 2*self.n):
                    pq.append((gc, j))
            shuffle(pq)
            pq = sorted(pq, key=lambda x: x[0])
            for k in range(self.en.shape[1]):
                self.en[i, k] = pq[k][1]
            pq.clear()
    
    def generate_decode(self):
        # if self.en[0, 0] == 0:
        #     self.generate_encode()
        x, y = self.en.shape
        for i in range(x):
            self.de.append({})
            for j in range(y):
                self.de[i][self.en[i][j]] = j