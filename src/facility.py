import simpy
import service_times
import random
from constants import C1W1, C1W2, C1W3

buffer_capacity = 2
c1_initial = 500
c2_initial = 500
c3_initial = 500
c1_max = 1000
c2_max = 1000
c3_max = 1000

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
        
        c1w1_level = facility.c1w1.level
        c1w2_level = facility.c1w2.level
        c1w3_level = facility.c1w2.level

        buffer = get_chosen_buffer(c1w1_level, c1w2_level, c1w3_level)

        # Processes will have to wait (blocked)
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
            yield facility.c2w2.put(1)
            print("Inspector 2 has finished inspecting component 2 and has placed it in C2W2")
        else:
            print("Inspector 2 has started inspecting component 3")
            yield facility.c3.get(1)
            service_time = st.get_random_i2_3_st()
            yield env.timeout(service_time)
            yield facility.c3w3.put(1)
            print("Inspector 2 has finished inspecting component 3 and has placed it in C3W3")

def workstation_1(env, facility):
    while True:
        print("Workstation 1 has begun assembling product 1")
        yield facility.c1w1.get(1)
        service_time = st.get_random_w1_st()
        yield env.timeout(service_time)
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
        print("Workstation 3 has finished assembling product 3")

# TODO: Implement chosen buffer for inspector 1
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
    NUM_COMPONENTS = 1000

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