from time import process_time
from random import randint
import os
import argparse
import numpy as np
import heapq
import pickle


def main():
    io = IO()
    tester = Tester()
    tester.test_usability(io)
    # tester.test_check()


class Encoder:
    def __init__(self, inp):
        self.inp = inp
        self.result = bytes()
        self.seg_len = 0 # length of single segment

    def encode(self, tablem):
        ary = self.encode_to_ary(tablem)
        self.encode_to_bytes(ary)

    def encode_to_ary(self, tablem):
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

    def encode_to_bytes(self, ary):
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

    def set_de_inp(self, inp, seg_len):
        self.inp = inp
        self.seg_len = seg_len


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
                rl, gc = Tester.check(j, 2*self.n)  
                if rl and Tester.is_legal_cat(i, j, 2*self.n):
                    heapq.heappush(pq, (gc, j))
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


class Tester:        
    def __init__(self):
        pass

    def test_check(self):
        i = 0b1010111100111001
        n = 16
        print(Tester.check(i, n))

    def test_usability(self, io):
        io.print('Getting input......')
        n = io.get('n')
        b = io.read()
        io.print('Succefully got input')
        io.print('Getting table......')
        path = 'table_manager{:d}.data'.format(n)
        if os.path.exists(path):
            tablem = io.load_table(n)
        else:
            tablem = TableManager(n)
            tablem.generate_encode()
            tablem.generate_decode()
            io.store_table(tablem)
        io.print('Successfully got table')
        encoder = Encoder(b)
        io.print('Start encoding...')
        encoder.encode(tablem)
        print(encoder.result)
        io.print('Encoding successfully!')
        decoder = Decoder(encoder.seg_len, encoder.result)
        io.print('Start decoding...')
        decoder.decode(tablem)
        io.print('Decoding successfully!')
        io.print('Check decoding result')
        same = encoder.inp == decoder.result
        if same:
            io.print('Same!')
        elif encoder.inp == decoder.result[0:-1]:
            io.print('Same exept last byte!')
            print('Input:          ', encoder.inp)
            print('Decoding result:', decoder.result)
        else:
            io.print('Failed!')
            print('Input ', encoder.inp)
            print('Result', decoder.result)
        io.print('Writing decoding result...')
        io.write(encoder.result, True)
        io.print('Done')

    @classmethod
    def check(cls, i, n):
        """Return (run-length-legal: bool, gc-content: float)
        
        i is the bits string to be tested, n is the number of bits to be checked.
        """
        assert n % 2 == 0
        gc = 0
        m = n
        repeat = 1
        previous = -1
        while n > 0:
            current = i % 4
            if current == previous:
                repeat += 1
            else:
                repeat = 1
            if repeat > 3:
                return False, 0
            if current == 1 or current == 2:
                gc += 1
            previous = current
            n = n - 2
            i = i >> 2
        return True, gc/(m>>1)

    @classmethod
    def is_legal_cat(cls, i1, i2, n):
        """Return True if the last 6 bits of i1 can concatenate with the first 6 bits of i2 legally.

            n is the number of bits in i2.
        """        
        last6 = i1 % 64
        first6 =  i2 >> (n-6)
        new12 = (last6 << 6) + first6
        return Tester.check(new12, 12)[0]
    
    @classmethod
    def get_gc(cls, i, n):
        # n is length of i in bits
        assert n % 2 == 0
        count = 0
        while n > 0:
            t = i % 4
            count += (t == 1 or t == 2)
        return count


class IO:
    """Singleton class, dealing with command line argumet and file i/o"""
    def __init__(self):
        self.args = argparse.ArgumentParser()
        self.set_default_args()
        self.nsp = None
        self.dict = {}

    def add_argument(self, *args, **kwargs):
        """add new command line option/argument"""
        self.args.add_argument(*args, **kwargs)

    def set_default_args(self):
        """set default command line options"""
        self.args.add_argument('-i', '--input', help='indicate input file path', dest='input', metavar='path')
        self.args.add_argument('-o', '--output', help='indicate output file path', dest='output', metavar='path')
        self.args.add_argument('-b', '--binary', action='store_true', dest='bin', default=False, 
                                help='flag indicates that input file is a binary file. e.g. image, audio, video etc.')
        self.args.add_argument('-v', '--verbose', action='count', default=0, dest='verbosity', help='show more info')
        self.args.add_argument('-n', default=8, dest='n', type=int, help='set n in the algorithm')

    def get(self, s: str):
        """get the value for given option"""
        if not self.nsp:
            self.nsp = self.args.parse_args()
            self.dict = vars(self.nsp)            
        elif not self.dict:
            self.dict = vars(self.nsp)
        return self.dict[s]

    def read(self):
        """If input path is given, then read from the given path. Otherwise read from standard input
        
            return a bytes string    
        """
        if self.get('input'):
            if not self.get('bin'):
                f = open(self.get('input'), 'r')
                i = f.read().encode()
            else:
                f = open(self.get('input'), 'rb')
                i = f.read()
            f.close()
            return i
        else:
            s = ''
            try:
                while True:
                    s += input('input >') + '\n'
            except EOFError:
                pass
            return s.encode()

    def write(self, b: bytes, binary: bool):
        """if output path is given, then write to the given path. Otherwise write to standard ouptut
        
            argument should be a bytes string
        """
        if self.get('output'):
            if not binary:
                f = open(self.get('output'), 'w')
                f.write(b.decode())
            else:
                f = open(self.get('output'), 'wb')
                f.write(b)
            f.close()
        else:
            if self.get('bin'):
                print(b)
            else:
                print(b.decode())

    def print(self, s, v=-1):
        if self.get('verbosity') > v:
            print(s)

    def store_table(self, tablem):
        f = open('table_manager{:d}.data'.format(tablem.n), 'wb')
        pickle.dump(tablem, f)
        f.close()
    
    def load_table(self, n):
        f = open('table_manager{:d}.data'.format(n), 'rb')
        tablem = pickle.load(f)       
        return tablem

    
if __name__ == '__main__':
    main()