# encoding=utf-8
"""statistic module"""

import checker
import numpy as np
import matplotlib.pyplot as plt
import dnacode
import os
import pickle
from table import TableManager
from math import ceil
from math import floor
from myio import IO
from time import process_time

XA = 0.2
COLOR = '#009999'


def main():
    nlist = [5, 6, 7, 8]
    rtype = ['gc', 'time']
    encoding_statistics(5, 'speed')
    

# table statistic
def table_gc_distribution(n, unit):
    """get the distribution of gc content in a table

    n: same as table.n\n
    unit: the length of a partition
    """
    # init
    partitions = np.zeros(floor(1/unit)+1, dtype=np.int32)
    io = IO()
    tablem = dnacode.get_table(n, io=io)
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
    tablem = dnacode.get_table(n, io=io)

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


# encoding statistic
def encoding_statistics(n, rtype):
    # init
    try:
        f = open(f'test_output/result{n}.data', 'rb')
        results = pickle.load(f)
        f.close()
        dir_list = []    
    except FileNotFoundError:
        dir_list = ['test_dataset/single', 'test_dataset/sustech_files']
        results = []
        tm = dnacode.get_table(n)

    # start
    for directory in dir_list:
        a, b = test_one_dir(directory, n, tm=tm)
        print(a)
        results.extend(b)
    
    # extract data
    xlabel = ''
    ylabel = 'count'
    title = f'Statistics for Encoding {len(results)} Files with n={n}'
    data = np.zeros(len(results), dtype=np.float)
    avg = 0
    maximum = float('-inf')
    minimum = float('inf')
    if rtype == 'time':
        for i in range(len(results)):
            data[i] = results[i].time
            avg += data[i]
            maximum = max(maximum, data[i])
            minimum = min(minimum, data[i])
        label = 'Time(s)'
    elif rtype == 'gc':
        gcs = 0
        size = 0
        for i in range(len(results)):
            data[i] = results[i].gc / (4*results[i].size)
            gcs += results[i].gc
            size += 4 * results[i].size
            maximum = max(maximum, data[i])
            minimum = min(minimum, data[i])
        avg = gcs / size
        xlabel = 'GC-Content'
    elif rtype == 'speed':
        for i in range(len(results)):
            data[i] = results[i].speed
            avg += data[i]
            maximum = max(maximum, data[i])
            minimum = min(minimum, data[i])
        xlabel = 'Speed(bytes/sec)'
        avg /= len(results)
    else:
        for rsl in results:
            print(rsl)
            print()
    # draw
    plt.figure(1)
    plt.subplot(1, 1, 1)
    plt.hist(
        data, 
        bins=20, 
        facecolor=COLOR, 
        edgecolor='black'
    )
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    xannotate = XA
    plt.annotate(f'avg={avg}', xy=(xannotate, 0.9), xycoords='axes fraction')
    plt.annotate(f'max={maximum}', xy=(xannotate, 0.85), xycoords='axes fraction')
    plt.annotate(f'min={minimum}', xy=(xannotate, 0.8), xycoords='axes fraction')
    plt.savefig(f'../pic/{rtype}{n}.png', format='png', dpi=300)
    plt.show()

    # store result
    with open(f'test_output/result{n}.data', 'wb') as f:
        pickle.dump(results, f)

    return results
    

def test_one_file(path, n, info='', tm=None):
    """test one file"""
    # init
    if tm is None:
        tm = dnacode.get_table(n)

    # start
    test_rsl = TestResult()
    test_rsl.name = path.split(sep='/')[-1]
    test_rsl.info = info
    start = process_time()
    with open(path, 'rb') as f:
        file = f.read()
        result = dnacode.encode(n, file)
        test_rsl.time = process_time() - start
        test_rsl.size = len(result)
        test_rsl.speed = test_rsl.size /test_rsl.time
        test_rsl.gc = checker.get_gc_from_bytes(result)

    return test_rsl


def test_one_dir(path, n, info='', tm=None):
    """test one directory, path should not end with / """
    # init
    file_list = os.listdir(path)
    file_num = len(file_list)
    dir_rsl = TestResult()
    dir_rsl.name = path
    results = []
    if tm is None:
        tm = dnacode.get_table(n)
    start = process_time()

    # start
    print('working directory:', path)
    for file in file_list:
        test_rsl = test_one_file(path + '/' + file, n, tm=tm)
        dir_rsl.gc += test_rsl.gc
        dir_rsl.size += test_rsl.size
        results.append(test_rsl)
        print(f'one finished...({file})')
    dir_rsl.time = process_time() - start
    dir_rsl.speed = dir_rsl.size / dir_rsl.time

    return dir_rsl, results


class TestResult:
    def __init__(self):
        self.name = ''
        self.time = 0
        self.gc = 0
        self.info = ''
        self.size = 0 # in bytes
        self.speed = 0
    
    def __str__(self):
        s = '\n'
        s += 'TestResult:\n'
        s += f'name: {self.name}\n'
        s += f'gc_content = {self.gc/(self.size*4)}\n'
        s += f'speed = {self.speed} bytes/sec\n'
        if self.info:
            s += f'Additional info: {self.info}'
        return s


if __name__ == "__main__":
    main()