"""
constants.py is a configurable file that allows you to change the simulation duration, 
as well as the initial amount of components at the start of the simulation

Author: Diana Miraflor
Carleton University
"""

from pathlib import Path

data_directory = Path("data/rv/")
buffer_capacity = 2
C1W1 = 'C1W1'
C1W2 = 'C1W2'
C1W3 = 'C1W3'

# ------------ Configurable
SIMULATION_DURATION = 30000
# NOTE: To imitate infinite number of components - set to a high (very high) number.
# NOTE: Make initial numbers higher than simulation
# NOTE: c1 initial > c2 & c3
c1_initial = 1000000000
c2_initial = 1000000
c3_initial = 1000000
c1_max = 100000000000000
c2_max = 100000000000000
c3_max = 100000000000000

# ------------ Output directories for a simulation
st_dir = 'st_sim_dur_' + str(SIMULATION_DURATION)
it_dir = 'it_sim_dur_' + str(SIMULATION_DURATION)
comp_dir = 'comp_time_sim_dur_' + str(SIMULATION_DURATION)


#------------- RNG & RVG TEST Config
num_samples = 300
alpha = 0.05

i = 5
l = 5
bin_size = 20
# -------------
