# encoding=utf-8
"""io module"""


import argparse
import pickle


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
            i = bytes()
            with open(self.get('input'), 'rb') as f:
                i = f.read()
            return i
        else:
            s = ''
            try:
                while True:
                    s += input('input >') + '\n'
            except EOFError:
                pass
            return s.encode()

    def write(self, b: bytes):
        """if output path is given, then write to the given path. Otherwise write to standard ouptut
        
            argument should be a bytes string
        """
        try:
            b = b.decode()
            file_type = 'w'
            encoding = 'utf-8'
        except Exception:
            file_type = 'wb'
            encoding = None
        if self.get('output'):
            # print('------>', file_type)
            f = open(self.get('output'), file_type, encoding=encoding)
            f.write(b)
            f.close()
        else:
            self.print(b)

    def print(self, *s, v=0, **kwargs):
        if self.get('verbosity') >= v:
            print(*s, **kwargs)

    def store_table(self, tablem, path=None):
        if path is None:
            path='tables/table_manager{:d}.data'
            f = open(path.format(tablem.n), 'wb')
        else:
            f = open(path, 'wb')
        pickle.dump(tablem, f)
        f.close()
    
    def load_table(self, n, path=None, f=None):
        if path is None and f is None:
            path = 'tables/table_manager{:d}.data'.format(n)
            with open(path, 'rb') as f:
                tablem = pickle.load(f)
        elif (path is None) and not (f is None):
            tablem = pickle.load(f)
        else:
            with open(path, 'rb') as f:
                tablem = pickle.load(f)       
        return tablem
