from measurements import Measurements
from buffer import Buffer
from text_file_fnc import list_to_text_file
import numpy as np
import matplotlib.pyplot as plt

def facility_throughput(comp1_count, comp2_count, comp3_count, sim_dur):
    """
    Calculates facility throughput ~ average input rate of the system
    """
    return (comp1_count + comp2_count + comp3_count) / sim_dur

def facility_mean_delay_components(comp1_times, comp2_times, comp3_times):
    """
    Calculates mean delay of components in the facility
    """
    mean_comp1_delay = np.mean(comp1_times)
    mean_comp2_delay = np.mean(comp2_times)
    mean_comp3_delay = np.mean(comp3_times)



    return mean_comp1_delay + mean_comp2_delay + mean_comp3_delay

def facility_mean_num_components(buffers, inspector_component_times, workstation_length_times):
    """
    TODO: DO THIS. DUNNO HOW.

    Calculates the average number of components in the facility
    """
    list_of_sys = []
    overall_mean = 0
    total_time = 0

    for buf in buffers:
        list_of_sys.append(buf.get_queue_length_time())

    for key in inspector_component_times:
        list_of_sys.append(inspector_component_times[key])

    for key in workstation_length_times:
        list_of_sys.append(workstation_length_times[key])

    mean_component_facility = calculate_mean_components_system(list_of_sys, overall_mean, total_time)
    
    return mean_component_facility

def workstations_throughput(buffers, sim_dur):
    """
    Calculates throughput of workstations

    This is buffer + workstation
    """

    w1_thru = buffers[0].get_total_count() / sim_dur
    w2_thru = buffers[1].get_total_count() + buffers[2].get_total_count() / sim_dur
    w3_thru = buffers[3].get_total_count() + buffers[4].get_total_count() / sim_dur
    
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


def workstations_mean_number_comps(buffers, workstation_length_times):
    """
    Calculates mean number of components in buffer + workstation of workstations

    This is buffer + workstation
    """
    workstation1_sys = []
    workstation1_sys.append(buffers[0], workstation_length_times['workstation1'])

    workstation2_sys = []
    workstation2_sys.append(buffers[1], buffers[2], workstation_length_times['workstation2'])

    workstation3_sys = []
    workstation3_sys.append(buffers[3], buffers[4], workstation_length_times['workstation3'])

    overall_mean_w1 = 0
    total_time_w1 = 0

    overall_mean_w2 = 0
    total_time_w2 = 0

    overall_mean_w3 = 0
    total_time_w3 = 0

    mean_component_w1 = calculate_mean_components_system(workstation1_sys, overall_mean_w1, total_time_w1)
    mean_component_w2 = calculate_mean_components_system(workstation2_sys, overall_mean_w2, total_time_w2)
    mean_component_w3 = calculate_mean_components_system(workstation3_sys, overall_mean_w3, total_time_w3)

    return mean_component_w1, mean_component_w2, mean_component_w3


def calculate_mean_components_system(system_list, overall_mean, total_time):

    for sys in system_list:
        # Calculate the total time elapsed between the first and last recorded time
        time_elapsed = sys[-1][1] - sys[0][1]

        # Calculate the sum of (number of components * time) for each recorded time
        component_time_sum = 0
        for i in range(len(sys) - 1):
            num_components = sys[i][0]
            time_diff = sys[i+1][1] - sys[i][1]
            component_time_sum += num_components * time_diff

        # Calculate the mean number of components for this data structure
        mean_components = component_time_sum / time_elapsed

        # Update the overall mean and total time
        overall_mean += mean_components * time_elapsed
        total_time += time_elapsed

    overall_mean /= total_time
    return overall_mean


def generate_stats(measurements: Measurements, sim_dur, buffers):
    """
    MAIN FUNCTION TO CALL TO GENERATE STATISTICS
    """

    facility_thru = facility_throughput(measurements.get_component_1_count(), measurements.get_component_2_count(), measurements.get_component_3_count(), sim_dur)
    mean_component_delays = facility_mean_delay_components(measurements.get_component_1_time(), measurements.get_component_2_time(), measurements.get_component_3_time())
    facility_mean_components = facility_mean_num_components(buffers, measurements.get_inspector_comp_times(), measurements.get_workstation_length_times())

    w1_thru, w2_thru, w3_thru = workstations_throughput(buffers, sim_dur)
    w1_st_qt, w2_st_qt, w3_st_qt = workstations_mean_service_queue_time(measurements.get_component_1_buf_work(), measurements.get_component_2_buf_work(), measurements.get_component_3_buf_work())
    w1_mean_comp, w2_mean_comp, w3_mean_comp = workstations_mean_number_comps(buffers, measurements.get_workstation_length_times())

    lines = [
        'Here are the statistics for the simulation: ',
        'SIMULATION DURATION: {}'.format(sim_dur),
        '--------------------------------------------------------',
        'SYSTEM: Facility',
        'Facility throughput: {}' .format(facility_thru),
        'Mean delay of components: {}'.format(mean_component_delays),
        'Mean number of components in facility: {}'.format(facility_mean_components),
        '--------------------------------------------------------',
        'SYSTEM: Buffer + Workstation',
        'Workstation 1 throughput: {}'.format(w1_thru),
        'Workstation 1 QT + ST: {}'.format(w1_st_qt),
        'Workstation 1 Mean Number of Components in System: {}'.format(w1_mean_comp),
        '\n',
        'Workstation 2 throughput: {}'.format(w2_thru),
        'Workstation 2 QT + ST: {}'.format(w2_st_qt),
        'Workstation 2 Mean Number of Components in System: {}'.format(w2_mean_comp),
        '\n',
        'Workstation 3 throughput: {}'.format(w3_thru),
        'Workstation 3 QT + ST: {}'.format(w3_st_qt),
        'Workstation 3 Mean Number of Components in System: {}'.format(w3_mean_comp),
    ]

    list_to_text_file('./data/stats/', 'sim_' + str(sim_dur) + '_stats.txt', lines)