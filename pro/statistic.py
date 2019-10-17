# encoding=utf-8
"""statistic module"""

import checker
import numpy as np
import matplotlib.pyplot as plt
from table import TableManager
from math import ceil
from math import floor
from dnacode import get_table
from myio import IO


def main():
    pass


def table_gc_distribution(n, unit=0.1):
    """get the distribution of gc content in a table

    n: same as table.n\n
    unit: the length of a partition
    """
    # init
    partitions = np.zeros(floor(1/unit)+1, dtype=np.int32)
    io = IO()
    tablem = get_table(n, io=io)
    # start
    count = 0
    for func in tablem.en:
        if count % 16 < 15:
            print(count, end=' ', flush=True)
        else:
            print(count, flush=True)
        count += 1
        for seq in func:
            valid, gc = checker.check(seq, 2*n)
            partitions[floor(gc/unit)] += 1
    return partitions


def table_statistics():
    # init
    step = 0.1
    plt.figure()
    # plot
    for k in range(5, 9):
        print('getting distribution for n={:d}...'.format(k))
        y = table_gc_distribution(k)
        n = y.shape[0]
        x = np.array([i*step for i in range(n)])
        x = x + 0.5
        print(y)
        plt.plot(x, y, label='n={:d}'.format(k))
        plt.scatter(x, y, label='n={:d}'.format(k))
    # post-setting
    plt.xlabel('GC-Content')
    plt.xticks(x)
    plt.ylabel('number of segments')
    plt.legend(loc='upper right')
    # show
    plt.show()


def encoding_statistics():
    pass


if __name__ == "__main__":
    main()