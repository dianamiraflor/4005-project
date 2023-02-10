from constants import data_directory

def inspector1_1_st():
    i1_st = []
    inspector1_data = data_directory + '\\servinsp1.dat'
    with open(inspector1_data, 'r') as f:
        for line in f.readlines():
            i1_st.append(float(line))

    return i1_st

def inspector2_2_st():
    i2_2_st = []
    inspector2_data = data_directory + '\\servinsp22.dat'
    with open(inspector2_data, 'r') as f:
        for line in f.readlines():
            i2_2_st.append(float(line))

    return i2_2_st

def inspector2_3_st():
    i2_3_st = []
    inspector2_data = data_directory + '\\servinsp23.dat'
    with open(inspector2_data, 'r') as f:
        for line in f.readlines():
            i2_3_st.append(float(line))
    return i2_3_st

def workstation1_st():
    w1_st = []
    ws_data = data_directory + '\\ws1.dat'
    with open(ws_data, 'r') as f:
        for line in f.readlines():
            w1_st.append(float(line))
    return w1_st

def workstation2_st():
    w2_st = []
    ws_data = data_directory + '\\ws2.dat'
    with open(ws_data, 'r') as f:
        for line in f.readlines():
            w2_st.append(float(line))
    return w2_st

def workstation3_st():
    w3_st = []
    ws_data = data_directory + '\\ws3.dat'
    with open(ws_data, 'r') as f:
        for line in f.readlines():
            w3_st.append(float(line))
    return w3_st