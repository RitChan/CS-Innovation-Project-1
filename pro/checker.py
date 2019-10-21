# encoding=utf-8
"""checker module"""


def check(i, n):
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

def is_legal_cat(i1, i2, n):
    """Return True if the last 6 bits of i1 can concatenate with the first 6 bits of i2 legally.

        n is the number of bits in i2.
    """        
    last6 = i1 % 64
    first6 =  i2 >> (n-6)
    new12 = (last6 << 6) + first6
    return check(new12, 12)[0]
    
def get_gc(i, n):
    """n is length of i in bits"""
    assert n % 2 == 0
    count = 0
    while n > 0:
        t = i % 4
        count += (t == 1 or t == 2)
    return count

def get_gc_from_bytes(data=b''):
    # count gc numbers in one bytes
    def count_in_one(b):
        if isinstance(b, bytes):
            b = b[0]
        c = 0
        for _ in range(4):
            nt = b % 4 
            if nt == 1 or nt == 2:
                c += 1
            b = b >> 2
        return c

    count = 0
    for b in data:
        count += count_in_one(b)

    return count