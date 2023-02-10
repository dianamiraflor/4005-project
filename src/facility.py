import simpy
import service_times
import random
from constants import C1W1, C1W2, C1W3, buffer_capacity, c1_initial, c2_initial, c3_initial, c1_max, c2_max, c3_max, SIMULATION_DURATION

# Get all the service times of inspectors and workstations
st = service_times.ServiceTimes()

class Facility: 
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

# TODO: Implement blocking
def inspector_1(env, facility):
    while True:
        yield facility.c1.get(1)
        print("Inspector 1 has started inspecting component 1")
        # Get the service time from the file
        service_time = st.get_random_i1_st()
        yield env.timeout(service_time)

        print("Inspector 1 service time: " + str(service_time) + " minutes")
        
        # TODO: 
        # Process will have to wait until there's an available slot in a buffer.
        c1w1_level = facility.c1w1.level
        c1w2_level = facility.c1w2.level
        c1w3_level = facility.c1w3.level

        # If they are all full 
        # Block 
        if c1w1_level == c1w2_level == c1w3_level == buffer_capacity:
            print("Inspector 1 has been blocked (all buffers are at max capacity) and is waiting for an available buffer")
            buffer = get_chosen_buffer_at_capacity(c1w1_level, c1w2_level, c1w3_level, facility)
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
        

# TODO: Implement blocking
def inspector_2(env, facility):
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
            print("Inspector 3 service time on C3: " + str(service_time) + " minutes")
            yield facility.c3w3.put(1) # Will be blocked until there's space in this buffer
            print("Inspector 2 has finished inspecting component 3 and has placed it in C3W3")

def workstation_1(env, facility):
    while True:
        print("Workstation 1 has begun assembling product 1")
        yield facility.c1w1.get(1)
        service_time = st.get_random_w1_st()
        yield env.timeout(service_time)
        print("Workstation 1 service time: " + str(service_time) + " minutes")
        print("Workstation 1 has finished assembling product 1")

def workstation_2(env, facility):
    while True:
        c1_req = facility.c1w1.get(1)
        c2_req = facility.c2w2.get(1)
        print("Workstation 2 is waiting for product 1 and 2...")
        yield c1_req & c2_req # Wait until c1 and c2 components are both available
        print("Workstation 2 has started assembling product 2")
        service_time = st.get_random_w2_st()
        yield env.timeout(service_time)
        print("Workstation 2 service time: " + str(service_time) + " minutes")
        print("Workstation 2 has finished assembling product 2")

def workstation_3(env, facility):
    while True:
        c1_req = facility.c1w3.get(1)
        c3_req = facility.c3w3.get(1)
        print("Workstation 2 is waiting for product 1 and 3...")
        yield c1_req & c3_req # Wait until c1 and c3 components are both available
        print("Workstation 3 has started assembling product 3")
        service_time = st.get_random_w3_st()
        yield env.timeout(service_time)
        print("Workstation 3 service time: " + str(service_time) + " minutes")
        print("Workstation 3 has finished assembling product 3")

def get_chosen_buffer_at_capacity(facility):
    # If they are all full 
    # Block 
    free_c1w1 = False
    free_c1w2 = False
    free_c1w3 = False
    chosen_buffer = C1W1
    while (not free_c1w1) & (not free_c1w2) & (not free_c1w3):
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

    return chosen_buffer

def get_chosen_buffer(c1w1, c1w2, c1w3):
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
    # SIMULATION_DURATION = int(input('Duration of simulation (ms): '))
    # NUN_COMPONENTS = int(input('Enter the number of components (default is 1000): ')) # This is related to the infinite amount of components

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