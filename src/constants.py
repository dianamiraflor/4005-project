"""
constants.py is a configurable file that allows you to change the simulation duration, 
as well as the initial amount of components at the start of the simulation

Author: Diana Miraflor
Carleton University
"""

from pathlib import Path

data_directory = Path("data/")
buffer_capacity = 2
C1W1 = 'C1W1'
C1W2 = 'C1W2'
C1W3 = 'C1W3'

# ------------ Configurable
SIMULATION_DURATION = 100000 
# NOTE: To imitate infinite number of components - set to a high (very high) number.
c1_initial = 500
c2_initial = 500
c3_initial = 500
c1_max = 1000
c2_max = 1000
c3_max = 1000


#------------- RNG & RVG TEST Config
num_samples = 300
alpha = 0.05

i = 5
l = 5
bin_size = 20
# -------------
