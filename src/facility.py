import simpy
import text_file_fnc
from stats import generate_stats
from measurements import Measurements
from service_times import ServiceTimes
from inspector import Inspector1, Inspector2
from workstation import Workstation1, Workstation2, Workstation3
from constants import SIMULATION_DURATION, buffer_capacity, st_dir, it_dir, comp_dir

if __name__ == '__main__':
    """
    THE MAIN METHOD.
    Run facility.py to start simulation.
    """
    measurements = Measurements()
    st = ServiceTimes()

    # seed_input = 114121598
    gen_stats = False

    # simulation_duration = input('Please enter a simulation duration: ')
    # seed_input = input('Please enter a seed: ')
    gen_stats_input = input('Would you like to generate stats for Littles Law? (Y/N)')
    
    if gen_stats_input == 'Y':
        gen_stats = True

    # random_nums = rand_float_samples(300, seed = int(seed_input))
    # generate_random_vars(random_nums)

    print(f'STARTING MANUFACTURING FACILITY SIMULATION')
    print(f'----------------------------------')

    env = simpy.Environment()

    # -------- QUEUES / BUFFERS
    # buffers = [Buffer(1), Buffer(2), Buffer(3), Buffer(4), Buffer(5)]
                # c1w1      c1w2        c2w2      c1w3       c3w3
    buffer1 = simpy.Store(env, capacity = buffer_capacity)
    buffer2 = simpy.Store(env, capacity = buffer_capacity)
    buffer3 = simpy.Store(env, capacity = buffer_capacity)
    buffer4 = simpy.Store(env, capacity = buffer_capacity)
    buffer5 = simpy.Store(env, capacity = buffer_capacity)

    inspector_1_process = Inspector1(env, buffer1, buffer2, buffer4, measurements, st)
    inspector_2_process = Inspector2(env, buffer3, buffer5, measurements, st)
    workstation_1_process = Workstation1(env, buffer1, measurements, st)
    workstation_2_process = Workstation2(env, buffer2, buffer3, measurements, st)
    workstation_3_process = Workstation3(env, buffer4, buffer5, measurements, st)
    
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
    text_file_fnc.list_to_text_file('data/buffer_len_times/', 'buffer1.txt', measurements.get_buffer1_comp_time())
    text_file_fnc.list_to_text_file('data/buffer_len_times/', 'buffer2.txt', measurements.get_buffer2_comp_time())
    text_file_fnc.list_to_text_file('data/buffer_len_times/', 'buffer3.txt', measurements.get_buffer3_comp_time())
    text_file_fnc.list_to_text_file('data/buffer_len_times/', 'buffer4.txt', measurements.get_buffer4_comp_time())
    text_file_fnc.list_to_text_file('data/buffer_len_times/', 'buffer5.txt', measurements.get_buffer5_comp_time())



    print(f'Other results are saved in the data directory.')
    if gen_stats:
        print(f'Generating stats for Little Law...')
        generate_stats(measurements, SIMULATION_DURATION)
        print(f'Stats have been generated and are in ./stats/')