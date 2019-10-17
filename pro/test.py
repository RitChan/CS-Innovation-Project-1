# encoding=utf-8
"""test module"""


from table import TableManager
from myio import IO
from dna_v3 import Decoder
from dna_v3 import Encoder
import checker
import os


class Tester:        
    def __init__(self):
        pass

    def test_check(self):
        i = 0b1010111100111001
        n = 16
        print(checker.check(i, n))

    def test_usability(self, io):
        io.print('Getting input......')
        n = io.get('n')
        b = io.read()
        io.print('Succefully got input')
        io.print('Getting table......')
        path = 'tables/table_manager{:d}.data'.format(n)
        if os.path.exists(path):
            tablem = io.load_table(n)
        else:
            io.print('table not found, start generating a new table')
            tablem = TableManager(n)
            tablem.generate_encode()
            tablem.generate_decode()
            io.store_table(tablem)
        io.print('Successfully got table')
        encoder = Encoder(b)
        io.print('Start encoding...')
        encoder.encode(tablem)
        io.print(encoder.result, v=1)
        io.print('Encoding successfully!')
        decoder = Decoder(encoder.seg_len, encoder.result)
        io.print('Start decoding...')
        decoder.decode(tablem)
        io.print('Decoding successfully!')
        io.print('Check decoding result')
        same = (encoder.inp == decoder.result)
        if same:
            io.print('Same!')
            io.print('origin', encoder.inp, v=1)
            io.print('decoded', decoder.result, v=1)
        elif encoder.inp == decoder.result[0:-1]:
            io.print('Same except last byte!')
            io.print('Input:          ', encoder.inp, v=1)
            io.print('Decoding result:', decoder.result, v=1)
        else:
            io.print('Failed!')
            io.print('Input ', encoder.inp, v=1)
            io.print('Result', decoder.result, v=1)
        io.print('Writing decoding result...')
        io.write(decoder.result)
        io.print('Done')

    def test_io_load(self):
        io = IO()
        io.load_table(8)
        io.load_table(8, 'tables/table_manager{:d}.data'.format(8))
        f = open('tables/table_manager{:d}.data'.format(8), 'rb')
        io.load_table(8, f=f)
        io.print('pass')

    def test_in_out(self):
        io = IO()
        b = io.read()
        io.print(b, v=1)
        io.write(b)

if __name__ == "__main__":
    tester = Tester()
    # tester.test_io_load()
    tester.test_usability(IO())
    # tester.test_in_out()