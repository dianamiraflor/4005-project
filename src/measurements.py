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

        # ------ Component Times in 'System' - Facility
        self.comp_times_facility = {
            'component1':[],
            'component2':[],
            'component3':[]
        }

        # ------ Component Times in Buffer + Workstation
        self.comp_times_buff_work = {
            'component1':[],
            'component2':[],
            'component3':[]
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

        self.buffer_component_times = {
            'buffer1': [],
            'buffer2': [],
            'buffer3': [],
            'buffer4': [],
            'buffer5': []
        }

        self.buffer_total_count = {
            'buffer1': 0,
            'buffer2': 0,
            'buffer3': 0,
            'buffer4': 0,
            'buffer5': 0
        }

        # ------- Mean number of components at a point in time
        self.comp_count = []

        self.comp_count_buf_work = []

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

    
    def avg_buff1_occ(self, length):
        self.buffer_occupancies['buffer1'] += (length / buffer_capacity)

    def avg_buff2_occ(self, length):
        self.buffer_occupancies['buffer2'] += (length / buffer_capacity)

    def avg_buff3_occ(self, length):
        self.buffer_occupancies['buffer3'] += (length / buffer_capacity)

    def avg_buff4_occ(self, length):
        self.buffer_occupancies['buffer4'] += (length / buffer_capacity)

    def avg_buff5_occ(self, length):
        self.buffer_occupancies['buffer5'] += (length / buffer_capacity)


    def add_comp_1_time_buf_work(self, time):
        self.comp_times_buff_work['component1'].append(time)

    def add_comp_2_time_buf_work(self, time):
        self.comp_times_buff_work['component2'].append(time)

    def add_comp_3_time_buf_work(self, time):
        self.comp_times_buff_work['component3'].append(time)


    def add_workstation1_length_times(self, length, time):
        self.workstation_length_times['workstation1'].append([length, time])

    def add_workstation2_length_times(self, length, time):
        self.workstation_length_times['workstation2'].append([length, time])

    def add_workstation3_length_times(self, length, time):
        self.workstation_length_times['workstation3'].append([length, time])


    def add_inspector1_component_times(self, length, time):
        self.inspector_component_times['inspector1'].append([length, time])

    def add_inspector22_component_times(self, length, time):
        self.inspector_component_times['inspector22'].append([length, time])

    def add_inspector23_component_times(self, length, time):
        self.inspector_component_times['inspector23'].append([length, time])


    def add_buffer1_comp_time(self, length, time):
        self.buffer_component_times['buffer1'].append([length, time])

    def add_buffer2_comp_time(self, length, time):
        self.buffer_component_times['buffer2'].append([length, time])

    def add_buffer3_comp_time(self, length, time):
        self.buffer_component_times['buffer3'].append([length, time])

    def add_buffer4_comp_time(self, length, time):
        self.buffer_component_times['buffer4'].append([length, time])

    def add_buffer5_comp_time(self, length, time):
        self.buffer_component_times['buffer5'].append([length, time])\
        

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


    def add_comp_count(self, time, amount):
        self.comp_count.append([time, amount])

    def add_comp_count_buf_work(self, time, amount):
        self.comp_count_buf_work.append([time, amount])

# --------------------------------------------------------------


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
    
    
    def get_component_1_time(self):
        return self.comp_times_facility['component1']

    def get_component_2_time(self):
        return self.comp_times_facility['component2']
    
    def get_component_3_time(self):
        return self.comp_times_facility['component3']
    
    def get_component_times(self):
        return self.comp_times_facility
    
    
    def get_component_1_buf_work(self):
        return self.comp_times_buff_work['component1']
    
    def get_component_2_buf_work(self):
        return self.comp_times_buff_work['component2']
    
    def get_component_3_buf_work(self):
        return self.comp_times_buff_work['component3']
    
    
    def get_workstation1_length_times(self):
        return self.workstation_length_times['workstation1']
    
    def get_workstation2_length_times(self):
        return self.workstation_length_times['workstation2']
    
    def get_workstation3_length_times(self):
        return self.workstation_length_times['workstation3']
    
    def get_workstation_length_times(self):
        return self.workstation_length_times
    

    def get_inspector1_comp_times(self):
        return self.inspector_component_times['inspector1']
    
    def get_inspector22_comp_times(self):
        return self.inspector_component_times['inspector22']
    
    def get_inspector23_comp_times(self):
        return self.inspector_component_times['inspector23']
    
    def get_inspector_comp_times(self):
        return self.inspector_component_times
    

    def get_buffer1_comp_time(self):
        return self.buffer_component_times['buffer1']

    def get_buffer2_comp_time(self):
        return self.buffer_component_times['buffer2']

    def get_buffer3_comp_time(self):
        return self.buffer_component_times['buffer3']

    def get_buffer4_comp_time(self):
        return self.buffer_component_times['buffer4']

    def get_buffer5_comp_time(self):
        return self.buffer_component_times['buffer5']
    

    def get_buffer_total_count(self):
        return self.buffer_total_count
    
    def get_comp_count(self):
        return self.comp_count

    def get_comp_count_buf_work(self):
        return self.comp_count_buf_work
    
    def get_buffer_comp_times(self):
        return self.buffer_component_times
    
    def get_buff_occupancies(self):
        return self.buffer_occupancies
        
