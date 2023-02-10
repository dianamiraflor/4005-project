import os
from pathlib import Path

data_directory = Path("data/")
buffer_capacity = 2
C1W1 = 'C1W1'
C1W2 = 'C1W2'
C1W3 = 'C1W3'

# ------------ Configurable
SIMULATION_DURATION = 20000
# NOTE: These need to change because there the products will need more component 1s
c1_initial = 500
c2_initial = 500
c3_initial = 500
c1_max = 1000
c2_max = 1000
c3_max = 1000
# -------------
