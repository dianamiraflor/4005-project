"""
Exponential Distribution from input modeling

Y=Finv(q) -> A function of q with a lambda value in the equation
also dependent on the dataset
"""
import math
import rng

def get_inverse_cdf_exp_val(lam, rand):
    return -1 * ((1/lam) * math.log(1-rand)) # math.log calculates ln 

def generate_random_variates(num_samples, lam):
    variant_sequence = []
    rand_sequence = rng.rand_float_samples(num_samples)

    for rn in rand_sequence:
        x = get_inverse_cdf_exp_val(lam, rn)
        variant_sequence.append(x)

    return variant_sequence

def read_input_model_data():
    return

if __name__ == "__main__":
    lam = 0 # Lambda for exp dist
    samples = 0

    generate_random_variates(samples, lam)


