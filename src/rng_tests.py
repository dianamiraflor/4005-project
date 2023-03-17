"""
This module performs uniform and independence tests on the RNG that uses LCG (rng.py)
"""

from typing import Iterator
from matplotlib import pyplot as plt
from datetime import datetime
import pandas as pd
import numpy as np
import scipy.stats as stats
import math
from rng import rand_float_samples
from constants import num_samples, alpha, i, l, bin_size

def get_frequency_table(frequency, hist_bins, samples) -> pd.DataFrame :
    """
    Creates a frequency table to calculate the values of a chi-square test 
    
    param frequency: A list of frequencies of the intervals from the histogram
    param hist_bins: A list of values used as the intervals
    param samples: Number of samples

    return uniform_df: A dataframe that consists of the values of a chi-square test
    """
    uniform_df = pd.DataFrame(columns=["interval","frequency", "expected_freq", "variance", "chi"])

    list_of_intervals = []
    for i in range(len(hist_bins)):

        if i != len(hist_bins) - 1:
            list_of_intervals.append("(" + str(hist_bins[i]) + "," + str(hist_bins[i+1]) + "]")

    list_of_expected_freq = []
    for i in range (len(frequency)):
        list_of_expected_freq.append(samples / len(hist_bins))

    uniform_df["interval"] = list(list_of_intervals)
    uniform_df["frequency"] = frequency
    uniform_df["expected_freq"] = list(list_of_expected_freq)

    for index, row in uniform_df.iterrows():
        uniform_df.at[index,'variance'] = pow((row["frequency"] - row["expected_freq"]), 2)
    for index, row in uniform_df.iterrows():
        uniform_df.at[index,"chi"] = row["variance"] / row["expected_freq"]
    
    return uniform_df

def calculate_chi_square(chi_table) -> float:
    """
    Calculates the chi-square from the given frequency table

    param chi_table: A table that consists of values that help calculate the chi-square
    return chi_square: A float value that sums the 'chi' column of the table
    """
    chi_square = chi_table['chi'].sum()
    return chi_square

def test_for_uniformity_chi(chi_square, alpha, interval_count):
    """
    Uses a chi-square test to test for uniformity of a sequence of random numbers

    param chi_square: Calculated chi_square value
    param alpha: Signifance level of the chi-square test
    param interval_count: The number of bins
    
    """
    print("Uniformity Test")
    print("Null hypothesis: The nummbers are distributed uniformly on the interval [0,1]")
    
    critical_value = stats.chi2.ppf(1-alpha, interval_count-1)
    conclusion = "Failed to reject the null hypothesis."
    if chi_square > critical_value:
        conclusion = "Null Hypothesis is rejected."
        
    print("chisquare-score is:", chi_square, " and critical value is:", critical_value)
    print(conclusion)
 
def test_for_independence(rho, std_dev, alpha):
    """
    Test for indepence of a sequence of random numbers

    param rho: The mean
    param std_dev: The standard deviation
    param alpha: Signifance level of normal distribution
    """
    print("Autocorrelation Test")
    print("Null hypothesis: The numbers are independent of each other")

    z = -1 * (rho/std_dev) 

    print("Zo = " + str(z))

    z_value = stats.norm.ppf(alpha)

    conclusion = "Failed to reject the null hypothesis."
    if z > z_value:
        conclusion = "Null Hypothesis is rejected."

    print("z-score is:", z, " and z value is:", z_value)
    print(conclusion)

def calculate_rho_and_std_dev(random_nums, start, lag, N):
    """
    Calculates rho and dev to test for independence

    param random_nums: A sequence of random numbers
    param start: Starting position (i)
    param lag: Incremental value (l)
    param N: The number of samples (the length of random_nums)

    return rho: The mean
    return std_dev: The std. deviation
    """
    # M is the value such that i + (M + 1) * l <= N
    M = round(((N - start) / lag) - 1)
    
    #print(M)

    sum = 0
    for i in range(0, M+1):
        # print(random_nums[(start-1 + i*lag)])
        # print(str(random_nums[(start-1 + (i+1)*lag)-1]) + "\n")
        product = random_nums[((start-1) + i*lag)] * random_nums[((start-1) + (i+1)*lag)]
        sum = sum + product

    rho = (sum / M + 1) - 0.25

    std_dev = (math.sqrt(13*M + 7)) / (12 * (M+1))
    
    return rho, std_dev

if __name__ == "__main__":
    """
    Run this module to perform tests for RNG
    """
    rand_sequence = rand_float_samples(num_samples)

    file = open('random_numbers.txt', 'w')
    for r_num in rand_sequence:
         file.write(str(r_num)+"\n")

    file.close()

    counts, bins, bars = plt.hist(rand_sequence, bins=bin_size) # Bin Size = sqrt(sample_size)
    plt.show()
    freq_df = get_frequency_table(counts, bins, num_samples)
    print(freq_df)
    chi_square = calculate_chi_square(freq_df)
    test_for_uniformity_chi(chi_square, alpha, len(counts))

    rho, std_dev = calculate_rho_and_std_dev(rand_sequence, i, l, len(rand_sequence))
    test_for_independence(rho, std_dev, (alpha/2))