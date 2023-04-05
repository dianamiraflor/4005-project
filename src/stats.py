from measurements import Measurements
from buffer import Buffer
from text_file_fnc import list_to_text_file
import numpy as np
import matplotlib.pyplot as plt
import statistics

######### FACILITY #########
#############################################################################################

def facility_input_rate(total_comp_count, sim_dur):
    """
    Calculates facility throughput ~ average input rate of the system
    """
    
    return total_comp_count / sim_dur

def facility_mean_delay_components(component_times):
    """
    Calculates mean delay of components in the facility
    """
    combined_delays = [item for sublist in component_times.values() for item in sublist]
    mean_delay = statistics.mean(combined_delays)
    
    return mean_delay

def facility_mean_num_components(aggreg_comp_facility):
    """
    Calculates the average number of components in the facility

    Each parameter is in the form of [length, time] -> Which keeps track of the duration of 
    how many components are in their respective system.

    EX: [2 components, 20.0] 2 components are in the buffer for 20 minutes.

    """
    
    facility_mean_comps = calculate_mean_system_components(aggreg_comp_facility)

    return facility_mean_comps
   

######### BUFFER + WORKSTATION #########
#############################################################################################

def workstations_input_rate(workstations, sim_dur):
    """
    Calculates input rate of buffer + workstations

    This is buffer + workstation
    """
    w1_thru = workstations['workstation1'] / sim_dur
    w2_thru = workstations['workstation2'] / sim_dur
    w3_thru = workstations['workstation3'] / sim_dur

    return w1_thru, w2_thru, w3_thru

def workstations_mean_service_queue_time(comp1_b_wt, comp2_b_wt, comp3_b_wt):
    """
    Calculates mean service times of workstations

    This is buffer + workstation
    """

    mean_w1 = np.mean(comp1_b_wt)
    mean_w2 = np.mean(comp2_b_wt)
    mean_w3 = np.mean(comp3_b_wt)

    return mean_w1, mean_w2, mean_w3


def workstations_mean_number_comps(aggreg_comp_buff_work):
    """
    Calculates mean number of components in buffer + workstation of workstations
    buffers : In the form of [length, time] -> Duration of the buffer length
    workstation_length_times : In the form of [length, time] -> Duration of how many components are in the workstation
    
    EX: [2 components, 20.0] 2 components are in the buffer for 20 minutes.

    This is only for buffer + workstation
    
    """
    w1_mean_comp = calculate_mean_system_components(aggreg_comp_buff_work['workstation1'])
    w2_mean_comp = calculate_mean_system_components(aggreg_comp_buff_work['workstation2'])
    w3_mean_comp = calculate_mean_system_components(aggreg_comp_buff_work['workstation3'])

    return w1_mean_comp, w2_mean_comp, w3_mean_comp
    
###################################################################################
########## END OF BUFFER + WORKSTATION ###########################################

def calculate_all_buffers_occupancy(buffers):
    b1 = calculate_buffer_occupancy(buffers['buffer1'])
    b2 = calculate_buffer_occupancy(buffers['buffer2'])
    b3 = calculate_buffer_occupancy(buffers['buffer3'])
    b4 = calculate_buffer_occupancy(buffers['buffer4'])
    b5 = calculate_buffer_occupancy(buffers['buffer5'])

    return b1, b2, b3, b4, b5

def calculate_buffer_occupancy(buffer):
    total_time = buffer[-1][0] - buffer[0][0]
    total_components = 0

    for i in range(len(buffer) - 1):
        current_time = buffer[i][0]
        next_time = buffer[i+1][0]
        current_components = buffer[i][1]
        next_components = buffer[i+1][1]
        
        time_diff = next_time - current_time
        avg_components = (current_components + next_components) / 2.0
        
        total_components += avg_components * time_diff

    average_occupancy = total_components / total_time

    return average_occupancy



def calculate_mean_system_components(system_list):
    """
    TODO: Work on this. To get the overall number of components in the system, 
    do we combine the step functions together? 

    Helper function to help calculate the mean number of components
    system_list : A list of queues and service centers in the 'system'

     the time average is simply a summation of all steps multiplied by 
     the duration of each step and then divided by the total time
    """
    total_time = system_list[-1][1] - system_list[0][1]
    total_steps = len(system_list)
    steps_sum = 0
    for i in range(total_steps):
        steps_sum += system_list[i][0] * (system_list[i][1] - (system_list[i-1][1] if i > 0 else 0))
    mean_components = steps_sum / total_time
    return mean_components



def calculate_average_service_times(recorded_service_times):
    means = {}

    for key in recorded_service_times:
        mean_value = statistics.mean(recorded_service_times[key])
        means[key] = mean_value

    inspector1_mean = means['inspector1']
    inspector22_mean = means['inspector22']
    inspector23_mean = means['inspector23']
    workstation1_mean = means['workstation1']
    workstation2_mean = means['workstation2']
    workstation3_mean = means['workstation3']

    return inspector1_mean, inspector22_mean, inspector23_mean, workstation1_mean, workstation2_mean, workstation3_mean




def generate_stats(measurements: Measurements, sim_dur):
    """
    MAIN FUNCTION TO CALL TO GENERATE STATISTICS
    """

    facility_thru = facility_input_rate(measurements.get_total_facility_count(), sim_dur)
    mean_component_delays = facility_mean_delay_components(measurements.get_component_times())
    facility_mean_components = facility_mean_num_components(measurements.get_aggreg_facility())

    w1_thru, w2_thru, w3_thru = workstations_input_rate(measurements.get_total_buff_work_count(), sim_dur)
    w1_st_qt, w2_st_qt, w3_st_qt = workstations_mean_service_queue_time(measurements.get_component_1_buf_work(), measurements.get_component_2_buf_work(), measurements.get_component_3_buf_work())
    w1_mean_comp, w2_mean_comp, w3_mean_comp = workstations_mean_number_comps(measurements.get_aggreg_buff_work())


    buff1_occ, buff2_occ, buff3_occ, buff4_occ, buff5_occ = calculate_all_buffers_occupancy(measurements.get_buffer_comp_times())

    i1_st_mean, i22_st_mean, i23_st_mean, w1_mean, w2_mean, w3_mean = calculate_average_service_times(measurements.get_service_times())

    lines = [
        'Here are the statistics for the simulation: ',
        'SIMULATION DURATION: {}'.format(sim_dur),
        '--------------------------------------------------------',
        'SYSTEM: Facility',
        'Facility input rate: {0:.3f}' .format(facility_thru),
        'Mean delay of components: {0:.3f}'.format(mean_component_delays),
        'Mean number of components in facility: {0:.3f}'.format(facility_mean_components),
        '--------------------------------------------------------',
        'SYSTEM: Buffer + Workstation',
        'Workstation 1 input rate: {0:.3f}'.format(w1_thru),
        'Workstation 1 QT + ST: {0:.3f}'.format(w1_st_qt),
        'Workstation 1 Mean Number of Components in System: {0:.3f}'.format(w1_mean_comp),
        '\n',
        'Workstation 2 input rate: {0:.3f}'.format(w2_thru),
        'Workstation 2 QT + ST: {0:.3f}'.format(w2_st_qt),
        'Workstation 2 Mean Number of Components in System: {0:.3f}'.format(w2_mean_comp),
        '\n',
        'Workstation 3 input rate: {0:.3f}'.format(w3_thru),
        'Workstation 3 QT + ST: {0:.3f}'.format(w3_st_qt),
        'Workstation 3 Mean Number of Components in System: {0:.3f}'.format(w3_mean_comp),
        '--------------------------------------------------------',
        'AVERAGE BUFFER OCCUPANCIES',
        'Buffer 1: {0:.3f}'.format(buff1_occ),
        'Buffer 2: {0:.3f}'.format(buff2_occ),
        'Buffer 3: {0:.3f}'.format(buff3_occ),
        'Buffer 4: {0:.3f}'.format(buff4_occ),
        'Buffer 5: {0:.3f}'.format(buff5_occ),
        '--------------------------------------------------------',
        'AVERAGE SERVICE TIMES',
        'Inspector 1 : {0:.3f}'.format(i1_st_mean),
        'Inspector 2_2 : {0:.3f}'.format(i22_st_mean),
        'Inspector 2_3 : {0:.3f}'.format(i23_st_mean),
        'Workstation 1 : {0:.3f}'.format(w1_mean),
        'Workstation 2 : {0:.3f}'.format(w2_mean),
        'Workstation 3 : {0:.3f}'.format(w3_mean),
    ]

    list_to_text_file('stats/', 'sim_' + str(sim_dur) + '_stats.txt', lines)
