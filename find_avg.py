import csv
import os
import pandas as pd


master_workstation_df = pd.DataFrame()
master_inspector_df = pd.DataFrame()

# Get average service times for each workstation
for x in range(1,4): 
    workstation_service_time = pd.read_csv(os.getcwd() + '\\data\\ws' + str(1) + '.dat', header=None)
    workstation_service_time.columns = ['service_time']

    master_workstation_df['service_time_w' + str(x)] = workstation_service_time['service_time']

print(master_workstation_df.describe())

# Get average service times for each inspector
inspector_service_times = pd.read_csv(os.getcwd() + '\\data\\servinsp1.dat', header=None)
inspector_service_times.columns = ['service_time']

master_inspector_df['inspector1'] = inspector_service_times['service_time']

for x in range(2,4):
    inspector_service_times = pd.read_csv(os.getcwd() + '\\data\\servinsp2' + str(x) + '.dat', header=None)
    inspector_service_times.columns = ['service_time']

    master_inspector_df['inspector2' + str(x)] = inspector_service_times['service_time']

print(master_inspector_df.describe())