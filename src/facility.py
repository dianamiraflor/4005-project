import simpy
import service_times
import random

buffer_capacity = 2
c1_initial = 1000
c2_initial = 1000
c3_initial = 1000
c1_max = 500
c2_max = 500
c3_max = 500

# Get all the service times of inspectors and workstations
st = service_times.ServiceTimes()

class Facility: 
    def __init__(self, env):
        self.c1 = simpy.Container(env, capacity = c1_max, init = c1_initial)
        self.c2 = simpy.Container(env, capacity = c2_max, init = c2_initial)
        self.c3 = simpy.Container(env, capacity = c3_max, init = c3_initial)
        self.c1w1 = simpy.Container(env, capacity = buffer_capacity)
        self.c1w2 = simpy.Container(env, capacity = buffer_capacity)
        self.c2w2 = simpy.Container(env, capacity = buffer_capacity)
        self.c1w3 = simpy.Container(env, capacity = buffer_capacity)
        self.c3w3 = simpy.Container(env, capacity = buffer_capacity)


def inspector_1(env, facility):
    while True:
        yield facility.c1.get(1)
        # Get the service time from the file
        service_time = st.get_random_i1_st()
        yield env.timeout(service_time)

def inspector_2(env, facility):
    while True:
        random_component = random.randint(2,3)

        if random_component == 2:
            yield facility.c2.get(1)
            service_time = st.get_random_i2_2_st()
            yield env.timeout(service_time)
        else:
            yield facility.c3.get(1)
            service_time = st.get_random_i2_3_st()
            yield env.timeout(service_time)

def workstation_1(env, facility):
    while True:
        arrive_time = facility.env.now
        yield facility.c1w1.get(1)
        start_time = facility.env.now
        service_time = st.get_random_w1_st
        yield env.timeout(service_time)
        end_time = facility.env.now
        
def workstation_2(env, facility):
    while True:
        arrive_time = facility.env.now
        c1_req = facility.c1w1.get(1)
        c2_req = facility.c2w1.get(1)
        yield c1_req & c2_req # Wait until c1 and c2 components are both available
        start_time = facility.env.now
        service_time = st.get_random_w2_st
        yield env.timeout(service_time)
        end_time = facility.env.now

def workstation_3(env, facility):
    while True:
        arrive_time = facility.env.now
        c1_req = facility.c1w3.get(1)
        c3_req = facility.c3w3.get(1)
        yield c1_req & c3_req # Wait until c1 and c2 components are both available
        start_time = facility.env.now
        service_time = st.get_random_w3_st
        yield env.timeout(service_time)
        end_time = facility.env.now

