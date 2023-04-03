import random
from measurements import Measurements
from service_times import ServiceTimes
from component import Component
from constants import SIMULATION_DURATION, C1W1, C1W2, C1W3, buffer_capacity


class Inspector1(object):

    def __init__(self, env, buffer1, buffer2, buffer4, measurements : Measurements, st : ServiceTimes):
        self.env = env
        self.buffer1 = buffer1
        self.buffer2 = buffer2
        self.buffer4 = buffer4
        self.measurements = measurements
        self.st = st
        self.action = env.process(self.run())

    def run(self):
        print('Inspector 1 is starting...')

        while True:
            # Inspector is not idle at the start 
            idle = False
            idle_start = 0.0        # For block time
            idle_end = 0.0          # For block time

            ############### INSPECTING ###############
            service_time = self.st.get_random_i1_st() 
            c1 = Component(1)
            c1.set_start_time(self.env.now)
            print("Inspector 1 has started inspecting component 1")
            yield self.env.timeout(service_time)
            print("Inspector 1 service time on C1: " + str(service_time) + " minutes")
            

            ################ PLACING COMPONENT IN BUFFER ################
            buffer1_size = len(self.buffer1.items)
            buffer2_size = len(self.buffer2.items)
            buffer4_size = len(self.buffer4.items)

            # Case 1: All buffers are at max capacity which will cause inspector 1 to block
            if buffer1_size == buffer2_size == buffer4_size == buffer_capacity:
                idle = True
                idle_start = self.env.now
                print("Inspector 1 has been blocked (all buffers are at max capacity) and is waiting for an available buffer")
                
                # Try finding a free buffer
                # TODO: Might be broken
                self.find_free_buffer(idle)

                idle_end = self.env.now
                idle = False

            # Case 2: All buffers are not at max capacity -> there is always an available buffer to place component 1 in
            else: 
                print("Inspector 1 is currently choosing the shortest buffer (queue) to place a component in")
                buffer = self.get_chosen_buffer(buffer1_size, buffer2_size, buffer4_size)

            if not idle:
                if buffer == C1W1:
                    # yield facility.c1w1.put(1)
                    yield self.buffer1.put(c1)
                    c1.set_queue_start_time(self.env.now)
                    self.measurements.add_buffer1_comp_time(len(self.buffer1.items), self.env.now)           
                    self.measurements.avg_buff1_occ(len(self.buffer1.items))
                    print("Inspector 1 has finished inspecting component 1 and has placed it in C1W1") 
                    self.measurements.add_buffer1_total_count()
                if buffer == C1W2:
                    # yield facility.c1w2.put(1)  
                    yield self.buffer2.put(c1)
                    c1.set_queue_start_time(self.env.now)
                    self.measurements.add_buffer2_comp_time(len(self.buffer2.items), self.env.now)           
                    self.measurements.avg_buff2_occ(len(self.buffer2.items))
                    print("Inspector 1 has finished inspecting component 1 and has placed it in C1W2") 
                    self.measurements.add_buffer2_total_count()
                if buffer == C1W3:
                    # yield facility.c1w3.put(1)
                    yield self.buffer4.put(c1)
                    c1.set_queue_start_time(self.env.now)
                    self.measurements.add_buffer4_comp_time(len(self.buffer4.items), self.env.now)
                    self.measurements.avg_buff4_occ(len(self.buffer4.items))
                    print("Inspector 1 has finished inspecting component 1 and has placed it in C1W3") 
                    self.measurements.add_buffer4_total_count()

            self.measurements.add_comp_1_count() # STATS
            self.measurements.st_i1(service_time) # STATS
            self.measurements.it_i1(idle_end - idle_start)
            self.measurements.add_inspector1_component_times(1, self.env.now)

    def get_chosen_buffer(self, c1w1, c1w2, c1w3):
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
    
    def find_free_buffer(self, idle):
        """
        A method that will make inspector 1 block when all of its buffers for component 1 are at full capacity.
        Inspector 1 will then remain in a loop until a buffer has space.

        """
        # If they are all full 
        # Block 
        chosen_buffer = C1W1

        if idle: 
            # TODO: Goes into an infinite loop
            while True:
                if len(self.buffer1) < buffer_capacity:
                    idle = False
                    return chosen_buffer, False
                
                elif len(self.buffer2) < buffer_capacity:
                    chosen_buffer = C1W2
                    idle = False
                    return chosen_buffer, idle

                elif len(self.buffer4) < buffer_capacity:
                    chosen_buffer = C1W3
                    idle = False
                    return chosen_buffer, idle

                else:
                    yield self.env.timeout(0.1)

        return None


class Inspector2(object):

    def __init__(self, env, buffer3, buffer5, measurements : Measurements, st : ServiceTimes):
        self.env = env
        self.buffer3 = buffer3
        self.buffer5 = buffer5
        self.measurements = measurements
        self.st = st
        self.action = env.process(self.run())

    def run(self):
        while True:
            random_component = random.randint(2,3)

            if random_component == 2:

                c2 = Component(2)
                c2.set_start_time(self.env.now)

                print("Inspector 2 has started inspecting component 2")
                service_time = self.st.get_random_i2_2_st()
                yield self.env.timeout(service_time)
                print("Inspector 2 service time on C2: " + str(service_time) + " minutes")
                idle_time = self.env.now
                # yield facility.c2w2.put(1) # Will be blocked until there's space in this buffer
                yield self.buffer3.put(c2) # TODO: Will this block?
                c2.set_queue_start_time(self.env.now)
                self.measurements.add_buffer3_comp_time(len(self.buffer3.items), self.env.now)
                self.measurements.avg_buff3_occ(len(self.buffer3.items))
                print("Inspector 2 has finished inspecting component 2 and has placed it in C2W2")
                idle_time_done = self.env.now

                # STATS
                self.measurements.add_buffer3_total_count()
                self.measurements.add_comp_2_count()
                self.measurements.it_i2(idle_time_done - idle_time)
                self.measurements.st_i2_2(service_time)
                self.measurements.add_inspector22_component_times(1, self.env.now)
                
            else:

                c3 = Component(3)
                c3.set_start_time(self.env.now)

                print("Inspector 2 has started inspecting component 3")
                service_time = self.st.get_random_i2_3_st()
                yield self.env.timeout(service_time)
                print("Inspector 2 service time on C3: " + str(service_time) + " minutes")
                idle_time = self.env.now
                # yield facility.c3w3.put(1) # Will be blocked until there's space in this buffer
                yield self.buffer5.put(c3) # TODO: Will this block?
                c3.set_queue_start_time(self.env.now)
                self.measurements.add_buffer5_comp_time(len(self.buffer5.items), self.env.now)
                self.measurements.avg_buff5_occ(len(self.buffer5.items))
                idle_time_done = self.env.now
                print("Inspector 2 has finished inspecting component 3 and has placed it in C3W3")

                # STATS
                self.measurements.add_buffer5_total_count()
                self.measurements.add_comp_3_count()
                self.measurements.it_i2(idle_time_done - idle_time)
                self.measurements.st_i2_3(service_time)
                self.measurements.add_inspector23_component_times(1, self.env.now)