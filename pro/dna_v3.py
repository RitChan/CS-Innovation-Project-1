# encoding=utf-8

from time import process_time
from random import randint
from myio import IO
import os
import argparse
import numpy as np
import heapq
import pickle


class Encoder:
    def __init__(self, inp):
        self.inp = inp
        self.result = bytes()
        self.seg_len = 0 # length of single segment to encode

    def encode(self, tablem):
        ary = self._encode_to_ary(tablem)
        self._encode_to_bytes(ary)

    def _encode_to_ary(self, tablem):
        seg_len = 2*tablem.n-1
        self.seg_len = seg_len
        rsl_len = (8*len(self.inp)+seg_len-1) // seg_len # ceiling
        ary = np.zeros(rsl_len, dtype=tablem.datatype)
        bp = 0 # bytes string pointer
        ncollected = 0 # number of bits collected
        j = 0
        last6 = 0
        for i in range(rsl_len):
            while ncollected < seg_len and bp < len(self.inp):
                # collect one byte at a time
                j = j << 8
                j += self.inp[bp]
                ncollected += 8
                bp += 1
            if ncollected >= seg_len:
                # encode $seg_len bits data at a time
                ary[i] = tablem.en[last6][j >> (ncollected-seg_len)]
                j %= 1 << (ncollected - seg_len)
                ncollected -= seg_len
            elif bp >= len(self.inp):
                j = j << (seg_len-ncollected)
                ary[i] = tablem.en[last6][j]
                break
            else:
                # no else
                pass
            last6 = ary[i] % 64
        return ary

    def _encode_to_bytes(self, ary):
        """further encode the ary to bytes"""
        target_len = self.seg_len+1
        nremained = 0
        k = 0
        for i in ary:
            k = k << target_len
            k += i
            nremained += target_len
            while nremained >= 8:
                self.result += bytes([k >> (nremained-8)])
                k %= 1 << (nremained-8)
                nremained -= 8
        else:
            if nremained > 0:
                k = k << (8 - nremained)
                self.result += bytes([k])

    def set_inp(self, inp):
        self.inp = inp


class Decoder:
    def __init__(self, seg_len=0, inp=None):
        self.seg_len = seg_len # to ensure using the right table
        self.inp = inp # bytes
        self.result = bytes()

    def decode(self, tablem):
        ary = self._decode_to_ary(tablem)
        self._decode_to_bytes(tablem, ary)

    def _decode_to_bytes(self, tablem, ary):
        assert self.seg_len == 2*tablem.n-1
        seg_len = self.seg_len
        seg = 0
        nremained = 0
        last6 = 0
        for i in ary:
            if i == 0:
                break
            seg = seg << seg_len
            seg += tablem.de[last6][i]
            nremained += seg_len
            while nremained >= 8:
                self.result += bytes([seg >> (nremained-8)])
                seg %= 1 << (nremained-8)
                nremained -= 8
            last6 = i % 64
        
    def _decode_to_ary(self, tablem):
        target_len = self.seg_len+1
        ary_size = (8*len(self.inp)+target_len-1) // target_len # ceiling
        ary = np.zeros(ary_size, tablem.datatype)
        ncollected = 0
        i = 0 # collected integer
        p = 0 # ary pointer
        for b in self.inp:
            i = i << 8
            i += b
            ncollected += 8
            while ncollected >= target_len and p < ary_size:
                ncollected -= target_len
                ary[p] = i >> ncollected
                i = i % (1 << ncollected)
                p += 1
        else:
            if ncollected > 0 and p < ary_size:
                i = i << (target_len-ncollected)
                ary[p] = i
        return ary

    def set_inp(self, inp, seg_len):
        self.inp = inp
        self.seg_len = seg_len
