"""release version"""

import os
from table import TableManager
from myio import IO
from dna_v3 import Encoder
from dna_v3 import Decoder

DEFAULT_PATH = 'tables/table_manager{:d}.data'


def encode(n, data=b'', tm=None):
    # init
    if tm is None:
        tm = get_table(n)
    encoder = Encoder(data)

    # start
    encoder.encode(tm)

    # return 
    return encoder.result


def get_table(n, io=None, path=None):
    global DEFAULT_PATH
    # init
    if io is None:
        io = IO()
    if path is None:
        path = DEFAULT_PATH.format(n)

    if os.path.exists(path):
        # try to load table from local file system        
        tablem = io.load_table(n)
    else:
        io.print('table not found, start generating a new table', v=1)
        io.print('this might take some time...', v=1)
        
        # start calculating encoding and decoding tables
        tablem = TableManager(n)
        tablem.generate_encode()
        tablem.generate_decode()
        io.store_table(tablem)

        io.print('got table and stored table for n={:d} successfully'.format(n), v=1)
    
    return tablem