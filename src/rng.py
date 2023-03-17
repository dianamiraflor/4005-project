"""
LCG IMPLEMENTATION SOURCE: https://github.com/rossilor95/lcg-python/blob/main/lcg.py
PARAMETERS SOURCE: https://www.ams.org/journals/mcom/1999-68-225/S0025-5718-99-00996-5/S0025-5718-99-00996-5.pdf
"""

from typing import Iterator
from matplotlib import pyplot as plt
from datetime import datetime
import pandas as pd
import numpy as np
import scipy.stats as stats
import math


def linear_congruential_generator(m: int, a: int, c: int, seed: int) -> Iterator[int]:
    """
    This generator implements the Linear Congruential Generator algorithm
    :param m: the modulus, a positive integer constant
    :param a: the multiplier, a non-negative integer constant < m
    :param c: the increment, a non-negative integer constant < m
    :param seed: the starting state of the LCG. It is used to initialize the pseudo-random number sequence
    :return: a non-negative integer in [0, m-1] representing the i-th state of the generator
    """
    x = seed
    while True:
        yield x
        x = (a * x + c) % m # Real number X

def rand_float_samples(n_samples: int, seed: int = 114121598):
    """
    This function uses an LCG to output a sequence of pseudo-random floats from the uniform distribution on [0, 1)
    :param n_samples: the number of pseudo-random floats to generate
    :param seed: the starting state of the LCG. It is used to initialize the pseudo-random number sequence
    :return: a list of length n_samples containing the generated pseudo-random numbers
    """
    exp_31 = 2147483648
    exp_32 = 4294967296
    m: int = exp_32 # 2^32
    a: int = 741103597
    c: int = 0
    gen = linear_congruential_generator(m, a, c, seed)
    sequence = []

    for i in range(0, n_samples):
        rand: float = next(gen) / m # Random number R
        sequence.append(rand)

    return sequence

if __name__ == "__main__":
    n = 300
    rand_sequence = rand_float_samples(n)

    file = open('random_numbers.txt', 'w')
    for r_num in rand_sequence:
         file.write(str(r_num)+"\n")

    file.close()

    counts, bins, bars = plt.hist(rand_sequence, bins=17) # Bin Size = sqrt(sample_size)
