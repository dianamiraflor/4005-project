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
            'comp1':0,
            'comp2':0,
            'comp3':0
        }

        # ------ Inspected Component Count
        self.comp_count_inspected = {
            'comp1':0,
            'comp2':0,
            'comp3':0
        }

        # ------ Component Times in 'System' - Facility
        self.comp_times_facility = {
            'comp1':[],
            'comp2':[],
            'comp3':[]
        }

        # ------ Component Times in Buffer + Workstation
        self.comp_times_buff_work = {
            'comp1':[],
            'comp2':[],
            'comp3':[]
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


    def add_comp_1_time_buf_work(self, time):
        self.comp_times_buff_work['component1'].append(time)

    def add_comp_2_time_buf_work(self, time):
        self.comp_times_buff_work['component1'].append(time)

    def add_comp_3_time_buf_work(self, time):
        self.comp_times_buff_work['component1'].append(time)


    def add_buffer1_length_times(self, length, time):
        self.buffer_length_times['buffer1'].append([length, time])

    def add_buffer2_length_times(self, length, time):
        self.buffer_length_times['buffer2'].append([length, time])

    def add_buffer3_length_times(self, length, time):
        self.buffer_length_times['buffer3'].append([length, time])

    def add_buffer4_length_times(self, length, time):
        self.buffer_length_times['buffer4'].append([length, time])

    def add_buffer5_length_times(self, length, time):
        self.buffer_length_times['buffer5'].append([length, time])


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
    
    
    def get_component_1_buf_work(self):
        return self.comp_times_buff_work['component1']
    
    def get_component_2_buf_work(self):
        return self.comp_times_buff_work['component2']
    
    def get_component_3_buf_work(self):
        return self.comp_times_buff_work['component3']
    

    def get_buffer1_length_times(self):
        return self.buffer_length_times['buffer1']
    
    def get_buffer2_length_times(self):
        return self.buffer_length_times['buffer2']
    
    def get_buffer3_length_times(self):
        return self.buffer_length_times['buffer3']
    
    def get_buffer4_length_times(self):
        return self.buffer_length_times['buffer4']
    
    def get_buffer5_length_times(self):
        return self.buffer_length_times['buffer5']
    
    
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
    

    def get_comp_count(self):
        return self.comp_count

    def get_comp_count_buf_work(self):
        return self.comp_count_buf_work
