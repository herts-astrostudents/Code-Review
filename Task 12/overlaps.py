import numpy as np
import pandas as pd


def overlap_python(primefile, happyfile):
    '''
    Return overlap between two lists using pure python.
    '''
    with open(primefile, 'r') as f:
        primes = set(map(int, f.readlines()))
    with open(happyfile, 'r') as f:
        happys = set(map(int, f.readlines()))
    return primes & happys



def overlap_numpy(primefile, happyfile):
    '''
    Return overlap between two lists using numpy.
    '''
    primes = np.loadtxt(primefile, dtype=int)
    happys = np.loadtxt(happyfile, dtype=int)
    return np.intersect1d(primes, happys, assume_unique=True)


def overlap_pandas(primefile, happyfile):
    '''
    Return overlap between two lists using pandas.
    '''
    primes = pd.read_table(primefile, header=None)[0]
    happys = pd.read_table(happyfile, header=None)[0]
    return primes[primes.isin(happys)]