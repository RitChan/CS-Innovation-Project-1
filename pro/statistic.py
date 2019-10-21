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
    n = 8
    # table_statistics_hist(n, norm=False)


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
    plt.xticks([0.1*i for i in range(11)])

    # set text
    plt.xlabel('gc-content')
    if not norm:
        plt.ylabel('counts')
    else:
        plt.ylabel('density')
    plt.title(f'Histogram of gc-content in a table with n={n}')

    # set annotation
    if n == 5:
        # (0.4, 5), (0.6, 5), (0.2, 0)
        plt.annotate(r'$gc = 0.2$', (0.15, 1000))
        plt.annotate(r'$gc = 0.4$', (0.30, 16500))
        plt.annotate(r'$gc = 0.6$', (0.61, 16000))
    elif n == 6:
        # 0.333, 0.5, 0.667
        plt.annotate(r'$gc \approx 0.333$', (0.3, 3000))
        plt.annotate(r'$gc = 0.5$', (0.5, 81000))
        plt.annotate(r'$gc \approx 0.667$', (0.62, 51000))
    elif n == 7:
        # 0.2, 0.4, 0.6
        plt.annotate(r'$\frac{2}{7} \approx 0.2857$', (0.2, 20000))
        plt.annotate(r'$\frac{3}{7} \approx 0.4285$', (0.36, 250000))
        plt.annotate(r'$\frac{4}{7} \approx 0.5714$', (0.62, 270000))
        plt.annotate(r'$\frac{5}{7} \approx 0.7142$', (0.7, 20000))
    elif n == 8:
        # 0.3, 0.4, 0.6
        plt.annotate(r'$gc = 0.375$', (0.3, 560000))
        plt.annotate(r'$gc = 0.5$', (0.35, 1000000))
        plt.annotate(r'$gc = 0.625$', (0.62, 560000))

    # save
    plt.savefig(f'../pic/gc_distri_hist{n}.png', format='png', dpi=300)

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