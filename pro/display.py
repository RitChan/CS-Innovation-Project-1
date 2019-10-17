# encoding=utf-8
"""display management module"""


class DisplayGenerator:
    def __init__(self, verbosity=1):
        self.verbosity = verbosity

    def get_acgt(self, inp: bytes):
        d = {0:'A', 1:'C', 2:'G', 3:'T'}
        s = ''
        for b in inp:
            t = ''
            for _ in range(4):
                t += d[b % 4]
                b = b >> 2
            s += t[::-1]
        return s