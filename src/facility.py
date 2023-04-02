"""
facility.py is the main module of the simulation. It contains an environment, Facilitiy and processes defined by generators.
Such processes are the two inspectors and three workstations. 

Running this module will begin the project's simulation.

Author: Diana Miraflor
Carleton University
"""

import simpy
import service_times
import measurements
import random
import text_file_fnc
from constants import SIMULATION_DURATION, C1W1, C1W2, C1W3, buffer_capacity, c1_initial, c2_initial, c3_initial, c1_max, c2_max, c3_max, it_dir, st_dir, comp_dir
from buffer import Buffer
from component import Component
from rng import rand_float_samples
from rvg import generate_random_vars
from stats import generate_stats


# Get all the service times of inspectors and workstations
st = service_times.ServiceTimes()
measurements = measurements.Measurements()


class Facility: 
    """
    A Facility class.
    Contains the 5 buffers shared between the inspectors and workstations, as well as containers for inspectors to fetch
    components from.
    """
    def __init__(self, env):

        # Instantiate the containers for loading the components for inspectors
        self.c1 = simpy.Container(env, capacity = c1_max, init = c1_initial)
        self.c2 = simpy.Container(env, capacity = c2_max, init = c2_initial)
        self.c3 = simpy.Container(env, capacity = c3_max, init = c3_initial)

        # Instantiate the containers (buffers) for each workstation
        self.c1w1 = simpy.Container(env, capacity = buffer_capacity)
        self.c1w2 = simpy.Container(env, capacity = buffer_capacity)
        self.c2w2 = simpy.Container(env, capacity = buffer_capacity)
        self.c1w3 = simpy.Container(env, capacity = buffer_capacity)
        self.c3w3 = simpy.Container(env, capacity = buffer_capacity)

def inspector_1(env, facility, buffer1, buffer2, buffer4):
    """
    Inspector 1 process.
    This process will loop for the entirety of the simulation duration.

    Inspector 1 will get components from container c1 and will perform inspection, 
    and once finished will then place it in one of the workstation's component 1's (c1w1, c1w2, c1w3) containers
    """
    while True:
        # Inspector is not idle at the start 
        idle = False
        idle_start = 0.0        # For block time
        idle_end = 0.0          # For block time

        ############### INSPECTING ###############
        service_time = st.get_random_i1_st() 
        c1 = Component(1)
        c1.set_start_time()
        print("Inspector 1 has started inspecting component 1")
        yield env.timeout(service_time)
        

        ################ PLACING COMPONENT IN BUFFER ################
        c1w1_level = facility.c1w1.level
        c1w2_level = facility.c1w2.level
        c1w3_level = facility.c1w3.level

        # Case 1: All buffers are at max capacity which will cause inspector 1 to block
        if c1w1_level == c1w2_level == c1w3_level == buffer_capacity:
            idle = True
            idle_start = env.now
            print("Inspector 1 has been blocked (all buffers are at max capacity) and is waiting for an available buffer")
            buffer, idle = get_chosen_buffer_at_capacity(facility)
            idle_end = env.now

        # Case 2: All buffers are not at max capacity -> there is always an available buffer to place component 1 in
        else: 
            print("Inspector 1 is currently choosing the shortest buffer (queue) to place a component in")
            buffer = get_chosen_buffer(c1w1_level, c1w2_level, c1w3_level)

        if not idle:
            if buffer == C1W1:
                yield facility.c1w1.put(1)
                buffer1.put(c1, env.now)
                print("Inspector 1 has finished inspecting component 1 and has placed it in C1W1") 
            if buffer == C1W2:
                yield facility.c1w2.put(1)
                buffer2.put(c1, env.now)
                print("Inspector 1 has finished inspecting component 1 and has placed it in C1W2") 
            if buffer == C1W3:
                yield facility.c1w3.put(1)
                buffer4.put(c1, env.now)
                print("Inspector 1 has finished inspecting component 1 and has placed it in C1W3") 

        measurements.add_comp_1_count() # STATS
        measurements.st_i1(service_time) # STATS
        measurements.it_i1(idle_end - idle_start)
        measurements.add_inspector1_component_times(1, env.now)



def inspector_2(env, facility, buffer3, buffer5):
    """
    Inspector 2 process.
    This process will loop for the entirety of the simulation duration.

    Inspector 2 will get components from container c2 and c3. However, it will randomly choose a random container to pick from.
    Once chosen, inspector 2 will perform inspection and place the component in its respective container (either c2w2 or c3w3).
    """
    while True:
        random_component = random.randint(2,3)

        if random_component == 2:
            idle_time = env.now

            c2 = Component(2)
            c2.set_start_time(env.now)

            yield facility.c2.get(1)
            print("Inspector 2 has started inspecting component 2")
            idle_time_done = env.now
            service_time = st.get_random_i2_2_st()
            yield env.timeout(service_time)
            print("Inspector 2 service time on C2: " + str(service_time) + " minutes")
            yield facility.c2w2.put(1) # Will be blocked until there's space in this buffer
            buffer3.put(c2, env.now)
            print("Inspector 2 has finished inspecting component 2 and has placed it in C2W2")

            # STATS
            measurements.add_comp_2_count()
            measurements.it_i2(idle_time_done - idle_time)
            measurements.st_i2_2(service_time)
            measurements.add_inspector22_component_times(1, env.now)
            
        else:
            idle_time = env.now

            c3 = Component(3)
            c3.set_start_time(env.now)

            yield facility.c3.get(1)
            print("Inspector 2 has started inspecting component 3")
            idle_time_done = env.now
            service_time = st.get_random_i2_3_st()
            yield env.timeout(service_time)
            print("Inspector 2 service time on C3: " + str(service_time) + " minutes")
            yield facility.c3w3.put(1) # Will be blocked until there's space in this buffer
            buffer5.put(c3, env.now)
            print("Inspector 2 has finished inspecting component 3 and has placed it in C3W3")

            # STATS
            measurements.add_comp_3_count()
            measurements.it_i2(idle_time_done - idle_time)
            measurements.st_i2_3(service_time)
            measurements.add_inspector23_component_times(1, env.now)

def workstation_1(env, facility, buffer1):
    """
    Workstation 1 process.
    This process will loop for the entirety of the simulation duration.

    Workstation 1 has only one container it fetches components from, c1w1. 
    Once component 1 is available in this container, it will then begin assembling product 1. 
    """
    while True:
        idle_time = env.now
        measurements.add_workstation1_length_times(0, idle_time)
        yield facility.c1w1.get(1)
        c1 = buffer1.get(env.now)
        if c1 is not None: # TODO: Might be a problem.
            
            measurements.add_workstation1_length_times(1, env.now)
            print("Workstation 1 has begun assembling product 1")
            idle_time_done = env.now
            service_time = st.get_random_w1_st()
            yield env.timeout(service_time)
            print("Workstation 1 service time: " + str(service_time) + " minutes")
            print("Workstation 1 has finished assembling product 1")
            
            c1.set_end_time(env.now)        # Ends component time
            c1.set_time_spent()             # Calculates time in the facility
            c1.buffer_workstation_time()    # Calculates time in buffer + workstation

            measurements.it_w1(idle_time_done - idle_time)
            measurements.st_w1(service_time)
            measurements.add_prod_1_count()
            measurements.add_comp_1_time(c1.get_time_spent())
            measurements.add_comp_1_time_buf_work(c1.get_buffer_workstation_time())

def workstation_2(env, facility, buffer2, buffer3):
    """
    Workstation 2 process.
    This process will loop for the entirety of the simulation duration.

    Workstation 2 has two containers: one for component 1 and one for component 2. 
    It will wait until both components are available in the containers. 
    Once available, it will begin assembling product 2.
    """
    while True:
        idle_time = env.now
        measurements.add_workstation2_length_times(0, idle_time)

        print("Workstation 2 is waiting for product 1 and 2...")

        yield facility.c1w2.get(1) or facility.c2w2.get(1) # Waits until one is available
        measurements.add_workstation2_length_times(1, env.now)

        yield facility.c1w2.get(1) and facility.c2w2.get(1) # Wait until c1 and c2 components are both available
        c1 = buffer2.get(env.now)
        c2 = buffer3.get(env.now)
        if c1 is not None and c2 is not None:
            measurements.add_workstation2_length_times(2, env.now)

            print("Workstation 2 has started assembling product 2")
            idle_time_done = env.now
            service_time = st.get_random_w2_st()
            yield env.timeout(service_time)
            print("Workstation 2 service time: " + str(service_time) + " minutes")
            print("Workstation 2 has finished assembling product 2")

            c1.set_end_time(env.now)        # Ends component time
            c1.set_time_spent()             # Calculates time in the facility
            c1.buffer_workstation_time()    # Calculates time in buffer + workstation

            c2.set_end_time(env.now)
            c2.set_time_spent()             # Calculates time in the facility
            c2.buffer_workstation_time()    # Calculates time in buffer + workstation
            
            measurements.it_w2(idle_time_done - idle_time)
            measurements.st_w2(service_time)

            measurements.add_prod_2_count()
            measurements.add_comp_1_time(c1.get_time_spent())
            measurements.add_comp_2_time(c2.get_time_spent())

            measurements.add_comp_1_time_buf_work(c1.get_buffer_workstation_time())
            measurements.add_comp_2_time_buf_work(c2.get_buffer_workstation_time())

def workstation_3(env, facility, buffer4, buffer5):
    """
    Workstation 3 process.
    This process will loop for the entirety of the simulation duration.

    Workstation 3 has two containers: one for component 1 and one for component 3. 
    It will wait until both components are available in the containers. 
    Once available, it will begin assembling product 3.
    """
    while True:
        idle_time = env.now
        measurements.add_workstation3_length_times(0, idle_time)

        print("Workstation 3 is waiting for product 1 and 3...")

        yield facility.c1w3.get(1) or facility.c3w3.get(1) # Waits until one is available
        measurements.add_workstation3_length_times(1, env.now)

        yield facility.c1w3.get(1) and facility.c3w3.get(1) # Wait until c1 and c3 components are both available
        c1 = buffer4.get(env.now)
        c3 = buffer5.get(env.now)
        if c1 is not None and c3 is not None:
            measurements.add_workstation3_length_times(2, env.now)
            
            print("Workstation 3 has started assembling product 3")
            idle_time_done = env.now
            service_time = st.get_random_w3_st()
            yield env.timeout(service_time)
            print("Workstation 3 service time: " + str(service_time) + " minutes")
            print("Workstation 3 has finished assembling product 3")
            
            c1.set_end_time(env.now)
            c3.set_end_time(env.now)
            
            measurements.it_w3(idle_time_done - idle_time)
            measurements.st_w3(service_time)

            measurements.add_prod_3_count()
            measurements.add_comp_1_time(c1.get_time_spent())
            measurements.add_comp_3_time(c3.get_time_spent())

            measurements.add_comp_1_time_buf_work(c1.get_buffer_workstation_time())
            measurements.add_comp_3_time_buf_work(c3.get_buffer_workstation_time())


def measure_num_components(env, facility):
    """
    This process monitors the number of components every clock tick 
    """

def get_chosen_buffer_at_capacity(facility, idle):
    """
    A method that will make inspector 1 block when all of its buffers for component 1 are at full capacity.
    Inspector 1 will then remain in a loop until a buffer has space.

    """
    # If they are all full 
    # Block 
    free_c1w1 = False
    free_c1w2 = False
    free_c1w3 = False
    chosen_buffer = C1W1

    if idle: 
        # TODO: Goes into an infinite loop
        while (not free_c1w1) and (not free_c1w2) and (not free_c1w3):
            current_c1w1_level = facility.c1w1.level
            current_c1w2_level = facility.c1w2.level
            current_c1w3_level = facility.c1w3.level
            # Wait until one is full
            if current_c1w1_level < buffer_capacity:
                free_c1w1 = True
            if current_c1w2_level < buffer_capacity:
                chosen_buffer = C1W2
                free_c1w2 = True
            if current_c1w3_level < buffer_capacity:
                chosen_buffer = C1W3
                free_c1w3 = True

        idle = False 

    return chosen_buffer, idle

def get_chosen_buffer(c1w1, c1w2, c1w3):
    """
    A method for inspector 1 to pick the buffer with the shortest queue. 
    """
    chosen_buffer = C1W1

    # Case 1: If all the same
    if c1w1 == c1w2 == c1w3:
        return chosen_buffer
    
    # Case 2: First buffer (W1) has the lowest amount
    if c1w1 <= c1w2 and c1w1 <= c1w3:
        return chosen_buffer

    # Case 3: Second buffer (W2) has the lowest
    if c1w2 <= c1w3 or c1w2 < c1w1:
        chosen_buffer = C1W2
        return chosen_buffer
    
    # Case 4: Third buffer (W3) has the lowest
    chosen_buffer = C1W3
    return chosen_buffer


# ---------------------------------------------------------------------------------------
if __name__ == '__main__':
    """
    THE MAIN METHOD.
    Run facility.py to start simulation.
    """

    seed_input = 114121598
    gen_stats = False

    # simulation_duration = input('Please enter a simulation duration: ')
    # seed_input = input('Please enter a seed: ')
    gen_stats = input('Would you like to generate stats for Littles Law? (Y/N)')
    
    if gen_stats == 'Y':
        gen_stats = True

    random_nums = rand_float_samples(300, seed = int(seed_input))
    generate_random_vars(random_nums)

    print(f'STARTING MANUFACTURING FACILITY SIMULATION')
    print(f'----------------------------------')

    env = simpy.Environment()
    facility = Facility(env)

    # -------- QUEUES / BUFFERS
    buffers = [Buffer(1), Buffer(2), Buffer(3), Buffer(4), Buffer(5)]
                # c1w1      c1w2        c2w2      c1w3       c3w3

    inspector_1_process = env.process(inspector_1(env, facility, buffers[0], buffers[1], buffers[3]))
    inspector_2_process = env.process(inspector_2(env, facility, buffers[2], buffers[4]))
    workstation_1_process = env.process(workstation_1(env, facility, buffers[0]))
    workstation_2_process = env.process(workstation_2(env, facility, buffers[1], buffers[2]))
    workstation_3_process = env.process(workstation_3(env, facility, buffers[3], buffers[4]))
    
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

    text_file_fnc.list_to_text_file('./data/' + st_dir, '/i1_service_times.txt', measurements.get_list_st_i1())
    text_file_fnc.list_to_text_file('./data/' + st_dir, '/i22_service_times.txt', measurements.get_list_st_i2_2())
    text_file_fnc.list_to_text_file('./data/' + st_dir, '/i23_service_times.txt', measurements.get_list_st_i2_3())
    text_file_fnc.list_to_text_file('./data/' + st_dir, '/w1_service_times.txt', measurements.get_list_st_w1())
    text_file_fnc.list_to_text_file('./data/' + st_dir, '/w2_service_times.txt', measurements.get_list_st_w2())
    text_file_fnc.list_to_text_file('./data/' + st_dir, '/w3_service_times.txt', measurements.get_list_st_w3())

    text_file_fnc.list_to_text_file('./data/' + it_dir, '/i1_idle_times.txt', measurements.get_list_it_i1())
    text_file_fnc.list_to_text_file('./data/' + it_dir, '/i2_idle_times.txt', measurements.get_list_it_i2())
    text_file_fnc.list_to_text_file('./data/' + it_dir, '/w1_idle_times.txt', measurements.get_list_it_w1())
    text_file_fnc.list_to_text_file('./data/' + it_dir, '/w2_idle_times.txt', measurements.get_list_it_w2())
    text_file_fnc.list_to_text_file('./data/' + it_dir, '/w3_idle_times.txt', measurements.get_list_it_w3())

    text_file_fnc.list_to_text_file('./data/' + comp_dir, '/comp1_time_spent.txt', measurements.get_component_1_time())
    text_file_fnc.list_to_text_file('./data/' + comp_dir, '/comp2_time_spent.txt', measurements.get_component_2_time())
    text_file_fnc.list_to_text_file('./data/' + comp_dir, '/comp3_time_spent.txt', measurements.get_component_3_time())
    
    # TODO: Collect buffer length time stats for LITTLE'S LAW
    buffer1_queue_length_time = buffers[0].get_queue_length_time()
    buffer2_queue_length_time = buffers[1].get_queue_length_time()
    buffer3_queue_length_time = buffers[2].get_queue_length_time()
    buffer4_queue_length_time = buffers[3].get_queue_length_time()
    buffer5_queue_length_time = buffers[4].get_queue_length_time()
    

    print(f'Other results are saved in the data directory.')

    if gen_stats:
        print(f'Generating stats for Little Law...')
        generate_stats(measurements, SIMULATION_DURATION, buffers)
        print(f'Stats have been generated and are in ./stats/')

