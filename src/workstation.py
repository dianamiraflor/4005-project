from measurements import Measurements
from service_times import ServiceTimes
from system import System
from constants import SIMULATION_DURATION

class Workstation1(object):

    def __init__(self, env, buffer1, measurements : Measurements, st : ServiceTimes, 
                 facility : System, buff_work : System):
        self.env = env
        self.buffer1 = buffer1
        self.measurements = measurements
        self.st = st
        self.facility = facility
        self.buff_work = buff_work

    def run(self):
        while True:
            self.measurements.add_buffer1_comp_time(len(self.buffer1.items), self.env.now)
            print("Workstation 1 is waiting for component 1...")
            idle_time = self.env.now
            self.measurements.add_blocked_time_start('workstation1', idle_time)
            self.measurements.add_workstation1_length_times(0, idle_time)
            # yield facility.c1w1.get(1)
            c1 = yield self.buffer1.get()
            self.measurements.add_buffer1_comp_time(len(self.buffer1.items), self.env.now)
            idle_time_done = self.env.now
            self.measurements.add_blocked_time_end('workstation1', idle_time_done)
            

            c1.set_assembly_time(self.env.now)
            c1.set_queue_time()
                
            self.measurements.add_workstation1_length_times(1, self.env.now)
            print("Workstation 1 has begun assembling product 1")
            service_time = self.st.get_random_w1_st()
            yield self.env.timeout(service_time)
            print("Workstation 1 service time: " + str(service_time) + " minutes")
            print("Workstation 1 has finished assembling product 1")
            self.facility.dec_current_comp(1)
            self.facility.add_total_components_departed(1)
            self.buff_work.dec_current_comp(1)
            self.buff_work.add_total_components_departed(1)
            self.measurements.update_comp_aggregate_facility(self.env.now, self.facility.get_current_comp())
            self.measurements.update_comp_aggregate_buff_work('workstation1', self.env.now, self.buff_work.get_current_comp())


            c1.set_end_time(self.env.now)        # Ends component time
            c1.set_time_spent()             # Calculates time in the facility
            c1.buffer_workstation_time()    # Calculates time in buffer + workstation

            self.measurements.it_w1(idle_time_done - idle_time)
            self.measurements.st_w1(service_time)
            self.measurements.add_prod_1_count()
            self.measurements.add_comp_1_time(c1.get_time_spent())
            self.measurements.add_queue_time('facility', c1.get_queue_time())
            self.measurements.add_queue_time('workstation1', c1.get_queue_time())
            self.measurements.add_w1_time_buff_work(c1.get_buffer_workstation_time())

class Workstation2(object):

    def __init__(self, env, buffer2, buffer3, measurements : Measurements, st : ServiceTimes,
                 facility : System, buff_work : System):
        self.env = env
        self.buffer2 = buffer2
        self.buffer3 = buffer3
        self.measurements = measurements
        self.st = st
        self.facility = facility
        self.buff_work = buff_work
      
    def run(self):
        while True:
            self.measurements.add_buffer2_comp_time(len(self.buffer2.items), self.env.now)
            self.measurements.add_buffer3_comp_time(len(self.buffer3.items), self.env.now)
            idle_time = self.env.now
            self.measurements.add_blocked_time_start('workstation2', idle_time)
            self.measurements.add_workstation2_length_times(0, idle_time)

            print("Workstation 2 is waiting for product 1 and 2...")

            #while True:
            #    if facility.c1w2.level > 0:
            #        measurements.add_workstation2_length_times(1, self.env.now)
            #        break
            #    elif facility.c2w2.level > 0:
            #        measurements.add_workstation2_length_times(1, self.env.now)
            #        break
            #    else:
            #        yield env.timeout(0.1)

            # yield facility.c1w2.get(1) and facility.c2w2.get(1) # Wait until c1 and c2 components are both available
            c1 = yield self.buffer2.get()
            c2 = yield self.buffer3.get()

            idle_time_done = self.env.now
            self.measurements.add_blocked_time_end('workstation2', idle_time_done)

            c1.set_assembly_time(self.env.now)
            c2.set_assembly_time(self.env.now)

            c1.set_queue_time()
            c2.set_queue_time()

            self.measurements.add_buffer2_comp_time(len(self.buffer2.items), self.env.now)
            self.measurements.add_buffer3_comp_time(len(self.buffer3.items), self.env.now)
                
            
            self.measurements.add_workstation2_length_times(2, self.env.now)

            print("Workstation 2 has started assembling product 2")
            service_time = self.st.get_random_w2_st()
            yield self.env.timeout(service_time)
            print("Workstation 2 service time: " + str(service_time) + " minutes")
            print("Workstation 2 has finished assembling product 2")
            self.facility.dec_current_comp(2)
            self.facility.add_total_components_departed(2)
            self.buff_work.dec_current_comp(2)
            self.buff_work.add_total_components_departed(2)
            self.measurements.update_comp_aggregate_facility(self.env.now, self.facility.get_current_comp())
            self.measurements.update_comp_aggregate_buff_work('workstation2', self.env.now, self.buff_work.get_current_comp())

            c1.set_end_time(self.env.now)        # Ends component time
            c1.set_time_spent()             # Calculates time in the facility
            c1.buffer_workstation_time()    # Calculates time in buffer + workstation

            c2.set_end_time(self.env.now)
            c2.set_time_spent()             # Calculates time in the facility
            c2.buffer_workstation_time()    # Calculates time in buffer + workstation
                    
            self.measurements.it_w2(idle_time_done - idle_time)
            self.measurements.st_w2(service_time)


            self.measurements.add_prod_2_count()
            self.measurements.add_comp_1_time(c1.get_time_spent())
            self.measurements.add_comp_2_time(c2.get_time_spent())

            self.measurements.add_queue_time('facility', c1.get_queue_time())
            self.measurements.add_queue_time('facility', c2.get_queue_time())
            self.measurements.add_queue_time('workstation2', c1.get_queue_time())
            self.measurements.add_queue_time('workstation2', c2.get_queue_time())

            self.measurements.add_w2_time_buff_work(c1.get_buffer_workstation_time())
            self.measurements.add_w2_time_buff_work(c2.get_buffer_workstation_time())

class Workstation3(object):

    def __init__(self, env, buffer4, buffer5, measurements : Measurements, st : ServiceTimes,
                 facility : System, buff_work : System):
        self.env = env
        self.buffer4 = buffer4
        self.buffer5 = buffer5
        self.measurements = measurements
        self.st = st
        self.facility = facility
        self.buff_work = buff_work
        

    def run(self):
        while True:
            self.measurements.add_buffer4_comp_time(len(self.buffer4.items), self.env.now)
            self.measurements.add_buffer5_comp_time(len(self.buffer5.items), self.env.now)
        
            idle_time = self.env.now
            self.measurements.add_blocked_time_start('workstation3', idle_time)
            self.measurements.add_workstation3_length_times(0, idle_time)

            print("Workstation 3 is waiting for product 1 and 3...")

            # while True:
            #    if facility.c1w3.level > 0:
            #        measurements.add_workstation3_length_times(1, env.now)
            #        break
            #    elif facility.c3w3.level > 0:
            #        measurements.add_workstation3_length_times(1, env.now)
            #        break
            #    else:
            #        yield env.timeout(0.1)

            # yield facility.c1w3.get(1) and facility.c3w3.get(1) # Wait until c1 and c3 components are both available

            # TODO: Does this block?
            c1 = yield self.buffer4.get()
            c3 = yield self.buffer5.get()

            idle_time_done = self.env.now
            self.measurements.add_blocked_time_end('workstation3', idle_time_done)

            c1.set_assembly_time(self.env.now)
            c3.set_assembly_time(self.env.now)

            c1.set_queue_time()
            c3.set_queue_time()

            self.measurements.add_buffer4_comp_time(len(self.buffer4.items), self.env.now)
            self.measurements.add_buffer5_comp_time(len(self.buffer5.items), self.env.now)
        
            self.measurements.add_workstation3_length_times(2, self.env.now)
                
            print("Workstation 3 has started assembling product 3")
            service_time = self.st.get_random_w3_st()
            yield self.env.timeout(service_time)
            print("Workstation 3 service time: " + str(service_time) + " minutes")
            print("Workstation 3 has finished assembling product 3")

            # Set the end times of components
            c1.set_end_time(self.env.now)
            c3.set_end_time(self.env.now)

            self.facility.dec_current_comp(2)
            self.facility.add_total_components_departed(2)
            self.buff_work.dec_current_comp(2)
            self.buff_work.add_total_components_departed(2)
            self.measurements.update_comp_aggregate_facility(self.env.now, self.facility.get_current_comp())
            self.measurements.update_comp_aggregate_buff_work('workstation3', self.env.now, self.buff_work.get_current_comp())
                
            c1.set_time_spent()             # Calculates time in the facility
            c1.buffer_workstation_time()    # Calculates time in buffer + workstation

            c3.set_time_spent()             # Calculates time in the facility
            c3.buffer_workstation_time()    # Calculates time in buffer + workstation
                     
            self.measurements.it_w3(idle_time_done - idle_time)
            self.measurements.st_w3(service_time)

            self.measurements.add_prod_3_count()

            self.measurements.add_queue_time('facility', c1.get_queue_time())
            self.measurements.add_queue_time('facility', c3.get_queue_time())
            self.measurements.add_queue_time('workstation3', c1.get_queue_time())
            self.measurements.add_queue_time('workstation3', c3.get_queue_time())

            # In facility
            self.measurements.add_comp_1_time(c1.get_time_spent())
            self.measurements.add_comp_3_time(c3.get_time_spent())

            # In buffer + workstattion
            self.measurements.add_w3_time_buff_work(c1.get_buffer_workstation_time())
            self.measurements.add_w3_time_buff_work(c3.get_buffer_workstation_time())