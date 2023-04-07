from constants import buffer_capacity

class Measurements():

    def __init__(self):
        ### MEASUREMENTS ###

        # ----- Service Times 
        self.service_times = {
            'inspector1': [],
            'inspector22': [],
            'inspector23': [],
            'workstation1':[],
            'workstation2':[],
            'workstation3':[]
        }

        # ----- Idle Times
        self.idle_times = {
            'inspector1': [],
            'inspector2': [],
            'workstation1':[],
            'workstation2':[],
            'workstation3':[]
        }

        # ----- Product Counts
        self.product_counts = {
            'product1': 0,
            'product2' : 0,
            'product3' : 0
        }

        # ------ Component Count - Counts the number of components that entered the system
        self.comp_count_facility = {
            'component1':0,
            'component2':0,
            'component3':0
        }

        # ------ Inspected Component Count
        self.comp_count_inspected = {
            'component1':0,
            'component2':0,
            'component3':0
        }


        # ------ Buffer occupancies 
        self.buffer_occupancies = {
            'buffer1': 0,
            'buffer2': 0,
            'buffer3': 0,
            'buffer4': 0,
            'buffer5': 0
        }

        ################################### USED FOR LITTLE'S LAW

        # ------ Component Times in 'System' - Facility
        self.comp_times_facility = {
            'component1':[],
            'component2':[],
            'component3':[]
        }

        # ------ Component Times in Buffer + Workstation
        # BEFORE: I was combining the service + queue times of component 1 in ALL OF ITS BUFFERS.
        # Had seperate times for each component. Should be seperate times of buffer + workstation
        #
        self.comp_times_buff_work = {
            'workstation1': [], 
            'workstation2': [],
            'workstation3': []
        }

        # ------ # Of Components in Workstation + Time
        # Could be used to determine how often workstation is busy
        # [[number_of_components, time]]

        self.workstation_length_times = {
            'workstation1': [], 
            'workstation2': [],
            'workstation3': []
        }

         # ------ Counts the time inspectors are holding each component for
        self.inspector_component_times = {
            'inspector1':[],
            'inspector22':[],
            'inspector23':[],
        }

        # ------ Records the number of components in a buffer at a specific time
        self.buffer_component_times = {
            'buffer1': [],
            'buffer2': [],
            'buffer3': [],
            'buffer4': [],
            'buffer5': []
        }  

        # ------ Counts the total number of components that have entered the buffer
        self.buffer_total_count = {
            'buffer1': 0,
            'buffer2': 0,
            'buffer3': 0,
            'buffer4': 0,
            'buffer5': 0
        }

        # ------- Mean number of components at a point in time
        self.comp_aggreg_facility = [] # [num components, time]

        self.comp_aggreg_buff_work = {
            'workstation1': [], 
            'workstation2': [],
            'workstation3': []
        } # [num components, time]
    

        # ------- Counts the total amount of components that have entered the system
        # Facility
        self.total_facility_count = 0


        # Buffer + Workstation
        self.total_buff_work_count = {
            'workstation1': 0, 
            'workstation2': 0,
            'workstation3': 0
        }

        self.queue_times = {
            'facility': [],
            'workstation1': [],
            'workstation2': [],
            'workstation3': [],
        }

        self.total_comp_departed = 0

        self.total_comp_departed_buff_work = {
            'workstation1': 0, 
            'workstation2': 0,
            'workstation3': 0
        }

        #########################

    def st_i1(self, st):
        self.service_times['inspector1'].append(st)

    def it_i1(self, it):
        self.idle_times['inspector1'].append(it)


    def st_i2_2(self, st):
        self.service_times['inspector22'].append(st)

    def st_i2_3(self, st):
         self.service_times['inspector23'].append(st)

    def it_i2(self, it):
        self.idle_times['inspector2'].append(it)


    def st_w1(self, st):
        self.service_times['workstation1'].append(st)
    
    def it_w1(self, it):
        self.idle_times['workstation1'].append(it)


    def st_w2(self, st):
        self.service_times['workstation2'].append(st)

    def it_w2(self, it):
        self.idle_times['workstation2'].append(it)


    def st_w3(self, st):
        self.service_times['workstation3'].append(st)

    def it_w3(self, it):
        self.idle_times['workstation3'].append(it)


    def add_prod_1_count(self):
        self.product_counts['product1'] += 1

    def add_prod_2_count(self):
        self.product_counts['product2'] += 1

    def add_prod_3_count(self):
        self.product_counts['product3'] += 1


    def add_comp_1_count(self):
        self.comp_count_facility['component1'] += 1

    def add_comp_2_count(self):
        self.comp_count_facility['component2'] += 1

    def add_comp_3_count(self):
        self.comp_count_facility['component3'] += 1


    def add_inspected_comp_1_count(self):
        self.comp_count_inspected['component1'] += 1

    def add_inspected_comp_2_count(self):
        self.comp_count_inspected['component2'] += 1

    def add_inspected_comp_3_count(self):
        self.comp_count_inspected['component3'] += 1


    def add_comp_1_time(self, time):
        self.comp_times_facility['component1'].append(time)

    def add_comp_2_time(self, time):
        self.comp_times_facility['component2'].append(time)

    def add_comp_3_time(self, time):
        self.comp_times_facility['component3'].append(time)


    def add_w1_time_buff_work(self, time):
        self.comp_times_buff_work['workstation1'].append(time)

    def add_w2_time_buff_work(self, time):
        self.comp_times_buff_work['workstation2'].append(time)

    def add_w3_time_buff_work(self, time):
        self.comp_times_buff_work['workstation3'].append(time)


    def add_workstation1_length_times(self, length, time):
        self.workstation_length_times['workstation1'].append([time, length])

    def add_workstation2_length_times(self, length, time):
        self.workstation_length_times['workstation2'].append([time, length])

    def add_workstation3_length_times(self, length, time):
        self.workstation_length_times['workstation3'].append([time, length])


    def add_buffer1_comp_time(self, length, time):
        self.buffer_component_times['buffer1'].append([time, length])

    def add_buffer2_comp_time(self, length, time):
        self.buffer_component_times['buffer2'].append([time, length])

    def add_buffer3_comp_time(self, length, time):
        self.buffer_component_times['buffer3'].append([time, length])

    def add_buffer4_comp_time(self, length, time):
        self.buffer_component_times['buffer4'].append([time, length])

    def add_buffer5_comp_time(self, length, time):
        self.buffer_component_times['buffer5'].append([time, length])
        

    def add_buffer1_total_count(self):
        self.buffer_total_count['buffer1'] += 1

    def add_buffer2_total_count(self):
        self.buffer_total_count['buffer2'] += 1

    def add_buffer3_total_count(self):
        self.buffer_total_count['buffer3'] += 1

    def add_buffer4_total_count(self):
        self.buffer_total_count['buffer4'] += 1

    def add_buffer5_total_count(self):
        self.buffer_total_count['buffer5'] += 1


    def update_comp_aggregate_facility(self, time, size):
        self.comp_aggreg_facility.append([time, size])
        
    def update_comp_aggregate_buff_work(self, workstation, time, size):
        self.comp_aggreg_buff_work[workstation].append([time, size])


    def set_total_comp_facility(self, amount):
        self.total_facility_count = amount

    def set_total_comp_buff_work(self, workstation, amount):
        self.total_buff_work_count[workstation] = amount


    def add_queue_time(self, key, time):
        self.queue_times[key].append(time)


    def set_components_departed(self, amount):
        self.total_comp_departed = amount

    def set_components_departed_buff_work(self, key, amount):
        self.total_comp_departed_buff_work[key] = amount



# --------------------------------------------------------------

    def get_service_times(self):
        return self.service_times


    def get_list_st_i1(self):
        return self.service_times['inspector1']
    
    def get_list_it_i1(self):
        return self.idle_times['inspector1']
    
    
    def get_list_st_i2_2(self):
        return self.service_times['inspector22']
    
    def get_list_st_i2_3(self):
        return self.service_times['inspector23']
    
    def get_list_it_i2(self):
        return self.idle_times['inspector2']
    
    
    def get_list_st_w1(self):
        return self.service_times['workstation1']
    
    def get_list_it_w1(self):
        return self.idle_times['workstation1']
    
    
    def get_list_st_w2(self):
        return self.service_times['workstation2']
    
    def get_list_it_w2(self):
        return self.idle_times['workstation2']
    
    
    def get_list_st_w3(self):
        return self.service_times['workstation3']
    
    def get_list_it_w3(self):
        return self.idle_times['workstation3']
    
    
    def get_product_1_count(self):
        return self.product_counts['product1']
    
    def get_product_2_count(self):
        return self.product_counts['product2']
    
    def get_product_3_count(self):
        return self.product_counts['product3']
    
    
    def get_component_1_count(self):
        return self.comp_count_facility['component1']
    
    def get_component_2_count(self):
        return self.comp_count_facility['component2']
    
    def get_component_3_count(self):
        return self.comp_count_facility['component3']
    

    def get_inspected_comp_1_count(self):
        return self.comp_count_inspected['component1']
    
    def get_inspected_comp_2_count(self):
        return self.comp_count_inspected['component2']
    
    def get_inspected_comp_3_count(self):
        return self.comp_count_inspected['component3']
    
    
    def get_component_times(self):
        return self.comp_times_facility
    
    
    def get_component_1_buf_work(self):
        return self.comp_times_buff_work['workstation1']
    
    def get_component_2_buf_work(self):
        return self.comp_times_buff_work['workstation2']
    
    def get_component_3_buf_work(self):
        return self.comp_times_buff_work['workstation3']
    
    
    def get_workstation1_length_times(self):
        return self.workstation_length_times['workstation1']
    
    def get_workstation2_length_times(self):
        return self.workstation_length_times['workstation2']
    
    def get_workstation3_length_times(self):
        return self.workstation_length_times['workstation3']
    
    def get_workstation_length_times(self):
        return self.workstation_length_times
    
        
    def get_buffer_comp_times(self):
        return self.buffer_component_times
    

    def get_buffer_total_count(self):
        return self.buffer_total_count
    
    def get_aggreg_facility(self):
        return self.comp_aggreg_facility
    
    def get_aggreg_buff_work(self):
        return self.comp_aggreg_buff_work
    

    def get_total_facility_count(self):
        return self.total_facility_count
    
    def get_total_buff_work_count(self):
        return self.total_buff_work_count
    

    def get_queue_times(self):
        return self.queue_times
    

    def get_total_comp_departed(self):
        return self.total_comp_departed


    def get_total_comp_departed_buff_work(self):
        return self.total_comp_departed_buff_work