"""
facility.py is the main module of the simulation. It contains an environment, Facilitiy and processes defined by generators.
Such processes are the two inspectors and three workstations. 

Running this module will begin the project's simulation.

Author: Diana Miraflor
Carleton University
"""

import simpy
import service_times
import random
from constants import SIMULATION_DURATION, C1W1, C1W2, C1W3, buffer_capacity, c1_initial, c2_initial, c3_initial, c1_max, c2_max, c3_max

# Get all the service times of inspectors and workstations
st = service_times.ServiceTimes()

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

def inspector_1(env, facility):
    """
    Inspector 1 process.
    This process will loop for the entirety of the simulation duration.

    Inspector 1 will get components from container c1 and will perform inspection, 
    and once finished will then place it in one of the workstation's component 1's (c1w1, c1w2, c1w3) containers
    """
    while True:
        yield facility.c1.get(1)
        print("Inspector 1 has started inspecting component 1")
        # Get the service time from the file
        service_time = st.get_random_i1_st()
        yield env.timeout(service_time) 

        print("Inspector 1 service time: " + str(service_time) + " minutes")
        
        # TODO: Simulation does not simulate blocking for inspector 1 
        c1w1_level = facility.c1w1.level
        c1w2_level = facility.c1w2.level
        c1w3_level = facility.c1w3.level

        # Case 1: All buffers are at max capacity which will cause inspector 1 to block
        if c1w1_level == c1w2_level == c1w3_level == buffer_capacity:
            print("Inspector 1 has been blocked (all buffers are at max capacity) and is waiting for an available buffer")
            buffer = get_chosen_buffer_at_capacity(c1w1_level, c1w2_level, c1w3_level, facility)

        # Case 2: All buffers are not at max capacity -> there is always an available buffer to place component 1 in
        else: 
            print("Inspector 1 is currently choosing the shortest buffer (queue) to place a component in")
            buffer = get_chosen_buffer(c1w1_level, c1w2_level, c1w3_level)

        if buffer == C1W1:
            yield facility.c1w1.put(1)
            print("Inspector 1 has finished inspecting component 1 and has placed it in C1W1") 
        if buffer == C1W2:
            yield facility.c1w2.put(1)
            print("Inspector 1 has finished inspecting component 1 and has placed it in C1W2") 
        if buffer == C1W3:
            yield facility.c1w3.put(1)
            print("Inspector 1 has finished inspecting component 1 and has placed it in C1W3") 
        
def inspector_2(env, facility):
    """
    Inspector 2 process.
    This process will loop for the entirety of the simulation duration.

    Inspector 2 will get components from container c2 and c3. However, it will randomly choose a random container to pick from.
    Once chosen, inspector 2 will perform inspection and place the component in its respective container (either c2w2 or c3w3).
    """
    while True:
        random_component = random.randint(2,3)

        if random_component == 2:
            print("Inspector 2 has started inspecting component 2")
            yield facility.c2.get(1)
            service_time = st.get_random_i2_2_st()
            yield env.timeout(service_time)
            print("Inspector 2 service time on C2: " + str(service_time) + " minutes")
            yield facility.c2w2.put(1) # Will be blocked until there's space in this buffer
            print("Inspector 2 has finished inspecting component 2 and has placed it in C2W2")
        else:
            print("Inspector 2 has started inspecting component 3")
            yield facility.c3.get(1)
            service_time = st.get_random_i2_3_st()
            yield env.timeout(service_time)
            print("Inspector 2 service time on C3: " + str(service_time) + " minutes")
            yield facility.c3w3.put(1) # Will be blocked until there's space in this buffer
            print("Inspector 2 has finished inspecting component 3 and has placed it in C3W3")

def workstation_1(env, facility):
    """
    Workstation 1 process.
    This process will loop for the entirety of the simulation duration.

    Workstation 1 has only one container it fetches components from, c1w1. 
    Once component 1 is available in this container, it will then begin assembling product 1. 
    """
    while True:
        yield facility.c1w1.get(1)
        print("Workstation 1 has begun assembling product 1")
        service_time = st.get_random_w1_st()
        yield env.timeout(service_time)
        print("Workstation 1 service time: " + str(service_time) + " minutes")
        print("Workstation 1 has finished assembling product 1")

def workstation_2(env, facility):
    """
    Workstation 2 process.
    This process will loop for the entirety of the simulation duration.

    Workstation 2 has two containers: one for component 1 and one for component 2. 
    It will wait until both components are available in the containers. 
    Once available, it will begin assembling product 2.
    """
    while True:
        c1_req = facility.c1w2.get(1)
        c2_req = facility.c2w2.get(1)
        print("Workstation 2 is waiting for product 1 and 2...")
        yield c1_req & c2_req # Wait until c1 and c2 components are both available
        print("Workstation 2 has started assembling product 2")
        service_time = st.get_random_w2_st()
        yield env.timeout(service_time)
        print("Workstation 2 service time: " + str(service_time) + " minutes")
        print("Workstation 2 has finished assembling product 2")

def workstation_3(env, facility):
    """
    Workstation 3 process.
    This process will loop for the entirety of the simulation duration.

    Workstation 3 has two containers: one for component 1 and one for component 3. 
    It will wait until both components are available in the containers. 
    Once available, it will begin assembling product 3.
    """
    while True:
        c1_req = facility.c1w3.get(1)
        c3_req = facility.c3w3.get(1)
        print("Workstation 3 is waiting for product 1 and 3...")
        yield c1_req & c3_req # Wait until c1 and c3 components are both available
        print("Workstation 3 has started assembling product 3")
        service_time = st.get_random_w3_st()
        yield env.timeout(service_time)
        print("Workstation 3 service time: " + str(service_time) + " minutes")
        print("Workstation 3 has finished assembling product 3")

def get_chosen_buffer_at_capacity(facility):
    """
    A method that will make inspector 1 block when all of its buffers for component 1 are at full capacity.
    Inspector 1 will then remain in a loop until a buffer has space.

    """
    free_c1w1 = False
    free_c1w2 = False
    free_c1w3 = False
    chosen_buffer = C1W1

    # Loop until a flag is set to true
    while (not free_c1w1) & (not free_c1w2) & (not free_c1w3):
        current_c1w1_level = facility.c1w1.level
        current_c1w2_level = facility.c1w2.level
        current_c1w3_level = facility.c1w3.level
        
        if current_c1w1_level < buffer_capacity:
            free_c1w1 = True
        if current_c1w2_level < buffer_capacity:
            chosen_buffer = C1W2
            free_c1w2 = True
        if current_c1w3_level < buffer_capacity:
            chosen_buffer = C1W3
            free_c1w3 = True

    return chosen_buffer

def get_chosen_buffer(c1w1, c1w2, c1w3):
    """
    A method for inspector 1 to pick the buffer with the shortest queue. 
    """
    chosen_buffer = C1W1

    # Case 1: If all the same
    if c1w1 == c1w2 == c1w3:
        return chosen_buffer
    
    # Case 2: First buffer (W1) has the lowest amount
    if c1w1 <= c1w2 & c1w1 <= c1w3:
        return chosen_buffer

    # Case 3: Second buffer (W2) has the lowest
    if c1w2 <= c1w3 | c1w2 < c1w1:
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

    SIMULATION_DURATION = 20000

    print(f'STARTING MANUFACTURING FACILITY SIMULATION')
    print(f'----------------------------------')

    env = simpy.Environment()
    facility = Facility(env)

    inspector_1_process = env.process(inspector_1(env, facility))
    inspector_2_process = env.process(inspector_2(env, facility))
    workstation_1_process = env.process(workstation_1(env, facility))
    workstation_2_process = env.process(workstation_2(env, facility))
    workstation_3_process = env.process(workstation_3(env, facility))

    env.run(until = SIMULATION_DURATION)

    print(f'----------------------------------')
    print(f'SIMULATION COMPLETED')