"""
data_wrapper.py reads the service times data of the inspectors and workstations and adds them to an array.
This is useful for picking a random service time for an inspector/workstation.

Author: Diana Miraflor
Carleton University
"""

from constants import data_directory

def inspector1_1_st():
    i1_st = []
    inspector1_data = data_directory / 'random_variates_i1.txt' 
    with open(inspector1_data, 'r') as f:
        for line in f.readlines():
            i1_st.append(float(line))

    return i1_st

def inspector2_2_st():
    i2_2_st = []
    inspector2_data = data_directory / 'random_variates_i22.txt'
    with open(inspector2_data, 'r') as f:
        for line in f.readlines():
            i2_2_st.append(float(line))

    return i2_2_st

def inspector2_3_st():
    i2_3_st = []
    inspector2_data = data_directory / 'random_variates_i23.txt'
    with open(inspector2_data, 'r') as f:
        for line in f.readlines():
            i2_3_st.append(float(line))
    return i2_3_st

def workstation1_st():
    w1_st = []
    ws_data = data_directory / 'random_variates_w1.txt'
    with open(ws_data, 'r') as f:
        for line in f.readlines():
            w1_st.append(float(line))
    return w1_st

def workstation2_st():
    w2_st = []
    ws_data = data_directory / 'random_variates_w2.txt'
    with open(ws_data, 'r') as f:
        for line in f.readlines():
            w2_st.append(float(line))
    return w2_st

def workstation3_st():
    w3_st = []
    ws_data = data_directory / 'random_variates_w3.txt'
    with open(ws_data, 'r') as f:
        for line in f.readlines():
            w3_st.append(float(line))
    return w3_st