from typing import Iterator
from matplotlib import pyplot as plt
from datetime import datetime
import pandas as pd
import numpy as np
import scipy.stats as stats
import math
from rng import rand_float_samples

def get_frequency_table(frequency, hist_bins, samples) -> pd.DataFrame :
    """
    The distribution should be uniform 
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
    chi_square = chi_table['chi'].sum()
    return chi_square

def test_for_uniformity_chi(chi_square, alpha, interval_count):
    print("Uniformity Test")
    print("Null hypothesis: The nummbers are distributed uniformly on the interval [0,1]")
    
    print("Approach: The p-value approach to hypothesis testing in the decision rule")
    p_value = 1 - stats.chi2.cdf(chi_square, interval_count - 1)
    conclusion = "Failed to reject the null hypothesis."
    if p_value <= alpha:
        conclusion = "Null Hypothesis is rejected."
        
    print("chisquare-score is:", chi_square, " and p value is:", p_value)
    print(conclusion)
 
def test_for_independence(rho, std_dev, alpha):
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


    return

def calculate_rho_and_std_dev(random_nums, start, lag, N):
    # M is the value such that i + (M + 1) * l <= N
    M = round(((N - start) / lag) - 1)
    print(M)

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
    n = 300
    rand_sequence = rand_float_samples(n)

    file = open('random_numbers.txt', 'w')
    for r_num in rand_sequence:
         file.write(str(r_num)+"\n")

    file.close()

    counts, bins, bars = plt.hist(rand_sequence, bins=17) # Bin Size = sqrt(sample_size)

    freq_df = get_frequency_table(counts, bins, 300)
    chi_square = calculate_chi_square(freq_df)
    test_for_uniformity_chi(chi_square, 0.05, len(counts))

    rho, std_dev = calculate_rho_and_std_dev(rand_sequence, 5, 5, len(rand_sequence))
    test_for_independence(rho, std_dev, 0.025)