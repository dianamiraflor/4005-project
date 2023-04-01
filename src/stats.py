from measurements import Measurements
from buffer import Buffer
from text_file_fnc import list_to_text_file
import numpy as np

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

def facility_mean_num_components():
    """
    TODO: DO THIS. DUNNO HOW.

    Calculates the average number of components in the facility
    """
    return

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


def workstations_mean_number_comps(b):
    """
    Calculates mean number of components in buffer + workstation of workstations

    This is buffer + workstation
    """




def generate_stats(measurements: Measurements, sim_dur, buffers):
    """
    MAIN FUNCTION TO CALL TO GENERATE STATISTICS
    """

    facility_thru = facility_throughput(measurements.get_component_1_count(), measurements.get_component_2_count(), measurements.get_component_3_count(), sim_dur)
    mean_component_delays = facility_mean_delay_components(measurements.get_component_1_time(), measurements.get_component_2_time(), measurements.get_component_3_time())

    w1_thru, w2_thru, w3_thru = workstations_throughput(buffers, sim_dur)
    w1_st_qt, w2_st_qt, w3_st_qt = workstations_mean_service_queue_time(measurements.get_component_1_buf_work(), measurements.get_component_2_buf_work(), measurements.get_component_3_buf_work())
    

    lines = [
        'Here are the statistics for the simulation: ',
        'SIMULATION DURATION: {}'.format(sim_dur),
        '--------------------------------------------------------',
        'SYSTEM: Facility',
        'Facility throughput: {}' .format(facility_thru),
        'Mean delay of components: {}'.format(mean_component_delays),
        'Mean number of components in facility: ' + str(),
        '--------------------------------------------------------',
        'SYSTEM: Buffer + Workstation',
        'Workstation 1 throughput: {}'.format(w1_thru),
        'Workstation 1 QT + ST: {}'.format(w1_st_qt),
        'Workstation 1 Mean Number of Components in System: {}'.format(),
        '\n',
        'Workstation 2 throughput: {}'.format(w2_thru),
        'Workstation 2 QT + ST: {}'.format(w2_st_qt),
        'Workstation 2 Mean Number of Components in System: {}'.format(),
        '\n',
        'Workstation 3 throughput: {}'.format(w3_thru),
        'Workstation 3 QT + ST: {}'.format(w3_st_qt),
        'Workstation 3 Mean Number of Components in System: {}'.format(),
    ]

    list_to_text_file('./data/stats/', 'sim_' + str(sim_dur) + '_stats.txt', lines)