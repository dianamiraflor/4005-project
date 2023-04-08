import simpy
import text_file_fnc
from stats import generate_stats, calculate_block_time, calculate_buffer_occupancy, facility_input_rate
from measurements import Measurements
from service_times import ServiceTimes
from inspector import Inspector1, Inspector2
from workstation import Workstation1, Workstation2, Workstation3
from system import System
from constants import SIMULATION_DURATION, buffer_capacity, st_dir, it_dir, comp_dir
from math import sqrt
from scipy.stats import t, norm as z

def to_file(measurements):
    text_file_fnc.list_to_text_file('data/' + st_dir, 'i1_service_times.txt', measurements.get_list_st_i1())
    text_file_fnc.list_to_text_file('data/' + st_dir, 'i22_service_times.txt', measurements.get_list_st_i2_2())
    text_file_fnc.list_to_text_file('data/' + st_dir, 'i23_service_times.txt', measurements.get_list_st_i2_3())
    text_file_fnc.list_to_text_file('data/' + st_dir, 'w1_service_times.txt', measurements.get_list_st_w1())
    text_file_fnc.list_to_text_file('data/' + st_dir, 'w2_service_times.txt', measurements.get_list_st_w2())
    text_file_fnc.list_to_text_file('data/' + st_dir, 'w3_service_times.txt', measurements.get_list_st_w3())

    text_file_fnc.list_to_text_file('data/' + it_dir, 'i1_idle_times.txt', measurements.get_list_it_i1())
    text_file_fnc.list_to_text_file('data/' + it_dir, 'i2_idle_times.txt', measurements.get_list_it_i2())
    text_file_fnc.list_to_text_file('data/' + it_dir, 'w1_idle_times.txt', measurements.get_list_it_w1())
    text_file_fnc.list_to_text_file('data/' + it_dir, 'w2_idle_times.txt', measurements.get_list_it_w2())
    text_file_fnc.list_to_text_file('data/' + it_dir, 'w3_idle_times.txt', measurements.get_list_it_w3())

    text_file_fnc.list_to_text_file('data/' + comp_dir, 'comp1_time_spent.txt', measurements.get_component_times()['component1'])
    text_file_fnc.list_to_text_file('data/' + comp_dir, 'comp2_time_spent.txt', measurements.get_component_times()['component2'])
    text_file_fnc.list_to_text_file('data/' + comp_dir, 'comp3_time_spent.txt', measurements.get_component_times()['component3'])
    
    # TODO: Collect buffer length time stats for LITTLE'S LAW
    text_file_fnc.list_to_text_file('data/buffer_len_times/', 'buffer1.txt', measurements.get_buffer_comp_times()['buffer1'])
    text_file_fnc.list_to_text_file('data/buffer_len_times/', 'buffer2.txt', measurements.get_buffer_comp_times()['buffer2'])
    text_file_fnc.list_to_text_file('data/buffer_len_times/', 'buffer3.txt', measurements.get_buffer_comp_times()['buffer3'])
    text_file_fnc.list_to_text_file('data/buffer_len_times/', 'buffer4.txt', measurements.get_buffer_comp_times()['buffer4'])
    text_file_fnc.list_to_text_file('data/buffer_len_times/', 'buffer5.txt', measurements.get_buffer_comp_times()['buffer5'])

    text_file_fnc.list_to_text_file('data/comp_queue_times/', 'facility.txt', measurements.get_queue_times()['facility'])
    text_file_fnc.list_to_text_file('data/comp_queue_times/', 'workstation1.txt', measurements.get_queue_times()['workstation1'])
    text_file_fnc.list_to_text_file('data/comp_queue_times/', 'workstation2.txt', measurements.get_queue_times()['workstation2'])
    text_file_fnc.list_to_text_file('data/comp_queue_times/', 'workstation3.txt', measurements.get_queue_times()['workstation3'])

    text_file_fnc.list_to_text_file('data/system_comp_len_times/', 'facility.txt', measurements.get_aggreg_facility())
    text_file_fnc.list_to_text_file('data/system_comp_len_times/', 'buff_work1.txt', measurements.get_aggreg_buff_work()['workstation1'])
    text_file_fnc.list_to_text_file('data/system_comp_len_times/', 'buff_work2.txt', measurements.get_aggreg_buff_work()['workstation2'])
    text_file_fnc.list_to_text_file('data/system_comp_len_times/', 'buff_work3.txt', measurements.get_aggreg_buff_work()['workstation3'])

def multiple_durations(replications, batches, batch_interval, measurements):
    keys=['inspector1',	'inspector22','inspector23','workstation1','workstation2','workstation3']

    ensemble_avg={}

    for duration in range (batch_interval,batches*batch_interval+1,batch_interval):
        multi_run_avgs={
            'inspector1': [],
            'inspector22': [],
            'inspector23': [],
            'workstation1':[],
            'workstation2':[],
            'workstation3':[]
        }
        for num in range(replications):

            env, employee_list, facility = init_simulation()

            for process in employee_list:
                env.process(process.run())

            env.run(until=duration)

            single_run_avgs={}
            for key in keys:
                if len(measurements.service_times[key])==0:
                    single_run_avgs[key]=0
                else:
                    single_run_avgs[key]=sum(measurements.service_times[key])/len(measurements.service_times[key])

                multi_run_avgs[key].append(single_run_avgs[key])

            # print(*single_run_avgs.values(), sep="\t")

        for key in keys:
            ensemble_avg[key]=sum(multi_run_avgs[key])/len(multi_run_avgs[key])
        ensemble_avg["time"]=duration
        print(*ensemble_avg.values(), sep="\t")

def multiple_replications(replications, duration, measurements):
    keys=['inspector1',	'inspector22','inspector23','workstation1','workstation2','workstation3']
    server_keys=['inspector1','inspector2','workstation1','workstation2','workstation3']
    buffer_keys=['buffer1','buffer2','buffer3','buffer4','buffer5']

    multi_run_avgs={
        # This is for service times
        'inspector1': [],
        'inspector22': [],
        'inspector23': [],
        'workstation1':[],
        'workstation2':[],
        'workstation3':[]
    }

    multi_run_throughput = []

    multi_run_blocked_probability = {
        'inspector1': [],
        'inspector2': [],
        'workstation1':[],
        'workstation2':[],
        'workstation3':[]
    }

    multi_run_avg_buff_occupancy = {
        'buffer1': [],
        'buffer2': [],
        'buffer3': [],
        'buffer4': [],
        'buffer5': []
    }


    for num in range(replications):
        env, employee_list, facility = init_simulation()

        for process in employee_list:
            env.process(process.run())

        env.run(until=duration)

        total = facility.get_total_component_num()
        measurements.set_total_comp_facility(total)

        single_run_avgs={}
        
        for key in keys:
            if len(measurements.service_times[key])==0:
                single_run_avgs[key]=0
            else:
                single_run_avgs[key]=sum(measurements.service_times[key])/len(measurements.service_times[key])
                
            multi_run_avgs[key].append(single_run_avgs[key])
            measurements.service_times[key] = [] # Resest for next replication


        for s_key in server_keys:
            # Calculate the probability a service center is blocked in one replication
            multi_run_blocked_probability[s_key].append(calculate_block_time(measurements.idle_times[s_key], duration))
            measurements.idle_times[s_key] = [] # Resest for next replication

        for b_key in buffer_keys:
            multi_run_avg_buff_occupancy[b_key].append(calculate_buffer_occupancy(measurements.buffer_component_times[b_key]))
            measurements.buffer_component_times[b_key] = [] # Resest for next replication

        measurements
        multi_run_throughput.append(facility_input_rate(measurements.get_total_facility_count(), duration))   



    text_file_fnc.list_to_text_file('data/replications/', 'i1_block_times.txt', multi_run_blocked_probability['inspector1'])
    text_file_fnc.list_to_text_file('data/replications/', 'i2_block_times.txt', multi_run_blocked_probability['inspector2'])
    text_file_fnc.list_to_text_file('data/replications/', 'w1_block_times.txt', multi_run_blocked_probability['workstation1'])
    text_file_fnc.list_to_text_file('data/replications/', 'w2_block_times.txt', multi_run_blocked_probability['workstation2'])
    text_file_fnc.list_to_text_file('data/replications/', 'w3_block_times.txt', multi_run_blocked_probability['workstation3'])

    text_file_fnc.list_to_text_file('data/replications/', 'buffer1_occ.txt', multi_run_avg_buff_occupancy['buffer1'])
    text_file_fnc.list_to_text_file('data/replications/', 'buffer2_occ.txt', multi_run_avg_buff_occupancy['buffer2'])
    text_file_fnc.list_to_text_file('data/replications/', 'buffer3_occ.txt', multi_run_avg_buff_occupancy['buffer3'])
    text_file_fnc.list_to_text_file('data/replications/', 'buffer4_occ.txt', multi_run_avg_buff_occupancy['buffer4'])
    text_file_fnc.list_to_text_file('data/replications/', 'buffer5_occ.txt', multi_run_avg_buff_occupancy['buffer5'])

    text_file_fnc.list_to_text_file('data/replications/', 'throughput.txt', multi_run_throughput)


    print('\n SERVICE TIMES CONFIDENCE INTERVAL')
    calculate_confidence_interval(multi_run_avgs, replications)

    print('\n PROBABILITY OF SERVER BLOCKED CONFIDENCE INTERVAL')
    calculate_confidence_interval(multi_run_blocked_probability, replications)

    print('\n AVERAGE BUFFER OCCUPANCY CONFIDENCE INTERVAL')
    calculate_confidence_interval(multi_run_avg_buff_occupancy, replications)

    print('\n THROUGHPUT CONFIDENCE INTERVAL')
    calculate_confidence_interval_thru(multi_run_throughput, replications)


def calculate_confidence_interval(multi_values, replications):
    ensemble_avg={}
    sample_variance={}
    confidence_interval={}
    r_val={}


    for key in multi_values.keys():
        ensemble_avg[key]=sum(multi_values[key])/len(multi_values[key])

        tmp_sum=0
        for yi in multi_values[key]:
            tmp_sum+=(yi-ensemble_avg[key])**2

        sample_variance[key]=1/(replications-1) * tmp_sum

        # Scores for 95% confidence
        t_score=t.ppf(0.975,df=replications-1)
        z_score=z.ppf(0.975)

        confidence_interval[key]=t_score*(sample_variance[key]/sqrt(replications))

        r_val[key]=((z_score**2)*sample_variance[key])/0.2

    print("\nT-score:")
    print(t_score)

    print("\nSample Variances:")
    print(*[format(value, ".2f") for value in sample_variance.values()], sep="\t")

    print("\nStandard Deviation:")
    print(*[format(sqrt(value), ".2f") for value in sample_variance.values()], sep="\t")

    print("\nMeans:")
    print(*[format(value, ".2f") for value in ensemble_avg.values()], sep="\t")

    print("\nCI (+/-):")
    print(*[format(value, ".2f") for value in confidence_interval.values()], sep="\t")

    print(f"\nR at {replications} replications:")
    print(*[format(value, ".2f") for value in r_val.values()], sep="\t")   



def calculate_confidence_interval_thru(multi_throughput, replications):
    ensemble_avg=sum(multi_throughput)/len(multi_throughput)

    tmp_sum=0
    for i in range(len(multi_throughput)):
        tmp_sum+=(multi_throughput[i]-ensemble_avg)**2

    sample_variance=1/(replications-1) * tmp_sum

    # Scores for 95% confidence
    t_score=t.ppf(0.975,df=replications-1)
    z_score=z.ppf(0.975)

    confidence_interval=t_score*(sample_variance/sqrt(replications))

    r_val=((z_score**2)*sample_variance)/0.2

    print("\nT-score:")
    print(t_score)

    print("\nSample Variances:")
    print(format(sample_variance, ".4f"), sep="\t")

    print("\nStandard Deviation:")
    print(format(sqrt(sample_variance), ".4f"), sep="\t")

    print("\nMeans:")
    print(format(ensemble_avg, ".4f"), sep="\t")

    print("\nCI (+/-):")
    print(format(confidence_interval, ".4f"), sep="\t")

    print(f"\nR at {replications} replications:")
    print(format(r_val, ".4f"), sep="\t")  


def init_simulation():
    env = simpy.Environment()
    facility = System()
    buff_work1 = System()
    buff_work2 = System()
    buff_work3 = System()

    # -------- QUEUES / BUFFERS
    # buffers = [Buffer(1), Buffer(2), Buffer(3), Buffer(4), Buffer(5)]
                # c1w1      c1w2        c2w2      c1w3       c3w3

    buffer1 = simpy.Store(env, capacity = buffer_capacity)
    buffer2 = simpy.Store(env, capacity = buffer_capacity)
    buffer3 = simpy.Store(env, capacity = buffer_capacity)
    buffer4 = simpy.Store(env, capacity = buffer_capacity)
    buffer5 = simpy.Store(env, capacity = buffer_capacity)

    process_list = []

    process_list.append(Inspector1(env, buffer1, buffer2, buffer4, measurements, st, facility, buff_work1, buff_work2, buff_work3))
    process_list.append(Inspector2(env, buffer3, buffer5, measurements, st, facility, buff_work2, buff_work3))
    process_list.append(Workstation1(env, buffer1, measurements, st, facility, buff_work1))
    process_list.append(Workstation2(env, buffer2, buffer3, measurements, st, facility, buff_work2))
    process_list.append(Workstation3(env, buffer4, buffer5, measurements, st, facility, buff_work3))
    
    return env, process_list, facility


if __name__ == '__main__':
    """
    THE MAIN METHOD.
    Run facility.py to start simulation.
    """
    start_time = 5000

    measurements = Measurements()
    st = ServiceTimes()

    # seed_input = 114121598
    gen_stats = False
    normal_run = False
    mult_durations = False
    mult_replications = False

    # simulation_duration = input('Please enter a simulation duration: ')
    # seed_input = input('Please enter a seed: ')

    run_type = input('Which type of simulation run would you like to simulate? (NORMAL/DURATIONS/REPLICATIONS) ')

    if run_type == "NORMAL":
        normal_run = True
        gen_stats_input = input('Would you like to generate stats for Littles Law? (Y/N) ')

        if gen_stats_input == 'Y':
            gen_stats = True
    
    if run_type == "DURATIONS":
        mult_durations = True
    
    if run_type == "REPLICATIONS":
        mult_replications = True
        
    # random_nums = rand_float_samples(300, seed = int(seed_input))
    # generate_random_vars(random_nums)
    
    print(f'STARTING MANUFACTURING FACILITY SIMULATION')
    print(f'----------------------------------')

    if normal_run:
        """
        USED FOR VERIFICATION
        """
        env = simpy.Environment()
        facility = System()
        buff_work1 = System()
        buff_work2 = System()
        buff_work3 = System()

        # -------- QUEUES / BUFFERS
        # buffers = [Buffer(1), Buffer(2), Buffer(3), Buffer(4), Buffer(5)]
                    # c1w1      c1w2        c2w2      c1w3       c3w3

        buffer1 = simpy.Store(env, capacity = buffer_capacity)
        buffer2 = simpy.Store(env, capacity = buffer_capacity)
        buffer3 = simpy.Store(env, capacity = buffer_capacity)
        buffer4 = simpy.Store(env, capacity = buffer_capacity)
        buffer5 = simpy.Store(env, capacity = buffer_capacity)

        process_list = []

        process_list.append(Inspector1(env, buffer1, buffer2, buffer4, measurements, st, facility, buff_work1, buff_work2, buff_work3))
        process_list.append(Inspector2(env, buffer3, buffer5, measurements, st, facility, buff_work2, buff_work3))
        process_list.append(Workstation1(env, buffer1, measurements, st, facility, buff_work1))
        process_list.append(Workstation2(env, buffer2, buffer3, measurements, st, facility, buff_work2))
        process_list.append(Workstation3(env, buffer4, buffer5, measurements, st, facility, buff_work3))
        
        for process in process_list:
            env.process(process.run())

        env.run(until = SIMULATION_DURATION)

        print(f'----------------------------------')
        print(f'SIMULATION COMPLETED')

        print(f'################################################################')
        print(f'SIMULATION DURATION: {SIMULATION_DURATION}')
        print(f'Here are the simulation results: ')

        print(f'Product 1 Count: {measurements.get_product_1_count()}')
        print(f'Product 2 Count: {measurements.get_product_2_count()}')
        print(f'Product 3 Count: {measurements.get_product_3_count()}')

        print(f'Component 1 Count: {measurements.get_component_1_count()}')
        print(f'Component 2 Count: {measurements.get_component_2_count()}')
        print(f'Component 3 Count: {measurements.get_component_3_count()}')

        total = facility.get_total_component_num()
        measurements.set_total_comp_facility(total)

        measurements.set_total_comp_buff_work('workstation1', buff_work1.get_total_component_num())
        measurements.set_total_comp_buff_work('workstation2', buff_work2.get_total_component_num())
        measurements.set_total_comp_buff_work('workstation3', buff_work3.get_total_component_num())

        measurements.set_components_departed(facility.get_total_components_departed())
        measurements.set_components_departed_buff_work('workstation1', buff_work1.get_total_components_departed())
        measurements.set_components_departed_buff_work('workstation2', buff_work2.get_total_components_departed())
        measurements.set_components_departed_buff_work('workstation3', buff_work3.get_total_components_departed())

        print(f'Other results are saved in the data directory.')
        if gen_stats:
            print(f'Generating stats for Little Law...')
            generate_stats(measurements, SIMULATION_DURATION)
            print(f'Stats have been generated and are in ./stats/')

        # to_file(measurements)
        
    if mult_durations:
        multiple_durations(100, 50, 500, measurements)
    
    if mult_replications:
        multiple_replications(100, 30000, measurements)

