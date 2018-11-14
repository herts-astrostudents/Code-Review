import numpy as np
import pandas as pd


def overlap_python(primefile, happyfile):
    '''
    Return overlap between two lists using pure python.
    '''
    primenumbers = [int(line) for line in open(primefile).readlines()]
    happynumbers = [int(line) for line in open(happyfile).readlines()]

    intersection = []
    for prime in primenumbers:
        if prime in happynumbers:
            intersection.append(prime)

    return intersection


def overlap_numpy(primefile, happyfile):
    '''
    Return overlap between two lists using numpy.
    '''
    primenumbers = np.genfromtxt(primefile, dtype=int)
    happynumbers = np.genfromtxt(happyfile, dtype=int)

    return np.intersect1d(primenumbers, happynumbers, assume_unique=True)


def overlap_pandas(primefile, happyfile):
    '''
    Return overlap between two lists using pandas.
    '''
    primenumbers = pd.read_csv(primefile, header=None, names=['values'])
    happynumbers = pd.read_csv(happyfile, header=None, names=['values'])

    intersection = pd.merge(primenumbers, happynumbers, how='inner', on='values', \
        left_index=False, right_index=False, sort=True, suffixes=('_wtf', '_wtf'))

    return intersection
