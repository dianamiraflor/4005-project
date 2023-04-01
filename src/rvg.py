"""
Exponential Distribution from input modeling

Y=Finv(q) -> A function of q with a lambda value in the equation
also dependent on the dataset
"""
import math
import rng
import text_file_fnc
from constants import num_samples

def get_inverse_cdf_exp_val(lamd, rand):
    return -1 * ((1/lamd) * math.log(1-rand)) # math.log calculates ln 

def generate_random_variate_list(rand_sequence, lamd):
    variant_sequence = []

    for rn in rand_sequence:
        x = get_inverse_cdf_exp_val(lamd, rn)
        variant_sequence.append(x)

    return variant_sequence

def generate_random_vars(random_numbers):
    workstation1_lam = 1 / 4.604417
    workstation2_lam = 1 / 4.604417
    workstation3_lam = 1 / 4.604417
    inspector1_lam = 1 / 10.357910
    inspector22_lam = 1 / 15.536903
    inspector23_lam = 1 / 20.632757 

    workstation1_var_seq = generate_random_variate_list(random_numbers, workstation1_lam)
    workstation2_var_seq = generate_random_variate_list(random_numbers, workstation2_lam)
    workstation3_var_seq = generate_random_variate_list(random_numbers, workstation3_lam)
    inspector1_var_seq = generate_random_variate_list(random_numbers, inspector1_lam)
    inspector22_var_seq = generate_random_variate_list(random_numbers, inspector22_lam)
    inspector23_var_seq = generate_random_variate_list(random_numbers, inspector23_lam)

    text_file_fnc.list_to_text_file('./data/rv/', 'random_variates_w1.txt', workstation1_var_seq)
    text_file_fnc.list_to_text_file('./data/rv/', 'random_variates_w2.txt', workstation2_var_seq)
    text_file_fnc.list_to_text_file('./data/rv/', 'random_variates_w3.txt', workstation3_var_seq)
    text_file_fnc.list_to_text_file('./data/rv/', 'random_variates_i1.txt', inspector1_var_seq)
    text_file_fnc.list_to_text_file('./data/rv/', 'random_variates_i22.txt', inspector22_var_seq)
    text_file_fnc.list_to_text_file('./data/rv/', 'random_variates_i23.txt', inspector23_var_seq)

