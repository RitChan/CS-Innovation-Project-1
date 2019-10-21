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
    table_statistics_hist(8, norm=True)


def table_gc_distribution(n, unit):
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
        # print
        if count % 16 < 15:
            print(count, end=' ', flush=True)
        else:
            print(count, flush=True)
        count += 1

        # 
        for seq in func:
            valid, gc = checker.check(seq, 2*n)
            partitions[floor(gc/unit)] += 1

    return partitions


def raw_gc(n):
    # init
    gcs = np.zeros(64*(1<<(2*n-1)), dtype=np.float)
    io = IO()
    tablem = get_table(n, io=io)

    # start
    p = 0
    row = 0
    for func in tablem.en:
        print(row % 16, end=' ', flush=True)
        if row % 16 == 15:
            print()
        row += 1
        for i in func:
            valid, gc = checker.check(i, 2*n)
            gcs[p] = gc
            p += 1
    
    # end
    return gcs


def table_statistics_hist(n, norm=False):
    # get data
    gcs = raw_gc(n)
    print(gcs)

    # draw
    plt.figure(1)
    plt.subplot(1, 1, 1)
    plt.hist(
        gcs, bins=10, range=(0, 1), density=norm, 
        facecolor='#ffcccc', edgecolor='black'
    )

    # set text
    plt.xlabel('gc-content')
    if not norm:
        plt.ylabel('counts')
    else:
        plt.ylabel('density')
    plt.title(f'Histogram of gc-content for n={n}')

    # show
    plt.show()


def table_statistics_plot():
    # init
    step = 0.05
    plt.figure()
    # plot
    for k in range(7, 8):
        print('getting distribution for n={:d}...'.format(k))
        y = table_gc_distribution(k, step)
        n = y.shape[0]
        x = np.array([i*step for i in range(n)])
        x = x + step/2
        print(y)
        plt.plot(x, y, label='n={:d}'.format(k))
        plt.scatter(x, y)
    # post-setting
    plt.xlabel('GC-Content')
    x = [0.1*i for i in range(11)]
    plt.xticks(x)
    plt.ylabel('number of segments')
    plt.legend(loc='upper right')
    # show
    plt.show()


def encoding_statistics():
    pass


if __name__ == "__main__":
    main()