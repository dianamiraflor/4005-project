import simpy
import text_file_fnc
from stats import generate_stats
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

    text_file_fnc.list_to_text_file('data/' + comp_dir, 'comp1_time_spent.txt', measurements.get_component_1_time())
    text_file_fnc.list_to_text_file('data/' + comp_dir, 'comp2_time_spent.txt', measurements.get_component_2_time())
    text_file_fnc.list_to_text_file('data/' + comp_dir, 'comp3_time_spent.txt', measurements.get_component_3_time())
    
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

def multiple_durations(env, replications, batches, batch_interval, measurements, employee_list):
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

def multiple_replications(env, replications, duration, measurements, employee_list):
    keys=['inspector1',	'inspector22','inspector23','workstation1','workstation2','workstation3']

    multi_run_avgs={
        'inspector1': [],
        'inspector22': [],
        'inspector23': [],
        'workstation1':[],
        'workstation2':[],
        'workstation3':[]
    }
    ensemble_avg={}
    sample_variance={}
    confidence_interval={}
    r_val={}


    for num in range(replications):
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

        print(*single_run_avgs.values(), sep="\t")

    for key in keys:
        ensemble_avg[key]=sum(multi_run_avgs[key])/len(multi_run_avgs[key])

        tmp_sum=0
        for yi in multi_run_avgs[key]:
            tmp_sum+=(yi-ensemble_avg[key])**2

        sample_variance[key]=1/(replications-1) * tmp_sum

        # Scores for 95% confidence
        t_score=t.ppf(0.975,df=replications-1)
        z_score=z.ppf(0.975)

        confidence_interval[key]=t_score*sqrt(sample_variance[key]/replications)

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
    gen_stats_input = input('Would you like to generate stats for Littles Law? (Y/N) ')

    if gen_stats_input == 'Y':
        gen_stats = True

    run_type = input('Which type of simulation run would you like to simulate? (NORMAL/DURATIONS/REPLICATIONS) ')

    if run_type == "NORMAL":
        normal_run = True
    
    if run_type == "DURATIONS":
        mult_durations = True
    
    if run_type == "REPLICATIONS":
        mult_replications = True
        
    # random_nums = rand_float_samples(300, seed = int(seed_input))
    # generate_random_vars(random_nums)
    
    print(f'STARTING MANUFACTURING FACILITY SIMULATION')
    print(f'----------------------------------')

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

    if normal_run:
        for process in process_list:
            env.process(process.run())

        env.run(until = SIMULATION_DURATION)
    
    if mult_durations:
        multiple_durations(env, 100, 50, 500, measurements, process_list)
    
    if mult_replications:
        multiple_replications(env, 100, 30000, measurements, process_list)

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

    # to_file(measurements)

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