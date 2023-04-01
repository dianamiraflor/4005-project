class Measurements():

    def __init__(self):
        ### MEASUREMENTS ###

        # ----- Service Times 
        self.list_of_st_i1 = [] 
        self.list_of_st_i2_2 = []
        self.list_of_st_i2_3 = []
        self.list_of_st_w1 = []
        self.list_of_st_w2 = []
        self.list_of_st_w3 = []

        # ----- Idle Times
        self.list_of_it_i1 = []
        self.list_of_it_i2 = []
        self.list_of_it_w1 = []
        self.list_of_it_w2 = []
        self.list_of_it_w3 = []

        # ------ Workstation Busy Times
        self.list_of_w1_busy_times = []
        self.list_of_w2_busy_times = []
        self.list_of_w3_busy_times = []

        # ----- Product Counts
        self.product_1_count = 0
        self.product_2_count = 0
        self.product_3_count = 0

        # ------ Component Count
        self.comp_1_count = 0 
        self.comp_2_count = 0
        self.comp_3_count = 0

        # ------ Inspected Component Count
        self.inspected_comp_1_count = 0
        self.inspected_comp_2_count = 0
        self.inspected_comp_3_count = 0

        # ------ Component Times in 'System'
        self.comp_1_time = []
        self.comp_2_time = []
        self.comp_3_time = []

        #########################

    def st_i1(self, st):
        self.list_of_st_i1.append(st)

    def it_i1(self, it):
        self.list_of_it_i1.append(it)

    def st_i2_2(self, st):
        self.list_of_st_i2_2.append(st)

    def st_i2_3(self, st):
        self.list_of_st_i2_3.append(st)

    def it_i2(self, it):
        self.list_of_it_i2.append(it)

    def st_w1(self, st):
        self.list_of_st_w1.append(st)
    
    def it_w1(self, it):
        self.list_of_it_w1.append(it)

    def st_w2(self, st):
        self.list_of_st_w2.append(st)

    def it_w2(self, it):
        self.list_of_it_w2.append(it)

    def st_w3(self, st):
        self.list_of_st_w3.append(st)

    def it_w3(self, it):
        self.list_of_it_w3.append(it)

    def add_prod_1_count(self):
        self.product_1_count = self.product_1_count + 1

    def add_prod_2_count(self):
        self.product_2_count = self.product_2_count + 1

    def add_prod_3_count(self):
        self.product_3_count = self.product_3_count + 1

    def add_comp_1_count(self):
        self.comp_1_count = self.comp_1_count + 1

    def add_comp_2_count(self):
        self.comp_2_count = self.comp_2_count + 1

    def add_comp_3_count(self):
        self.comp_3_count = self.comp_3_count + 1

    def add_inspected_comp_1_count(self):
        self.inspected_comp_1_count = self.inspected_comp_1_count + 1

    def add_inspected_comp_2_count(self):
        self.inspected_comp_2_count = self.inspected_comp_2_count + 1

    def add_inspected_comp_3_count(self):
        self.inspected_comp_3_count = self.inspected_comp_3_count + 1

    def add_comp_1_time(self, time):
        self.comp_1_time.append(time)

    def add_comp_2_time(self, time):
        self.comp_2_time.append(time)

    def add_comp_3_time(self, time):
        self.comp_3_time.append(time)

    def get_list_st_i1(self):
        return self.list_of_st_i1
    
    def get_list_it_i1(self):
        return self.list_of_it_i1
    
    def get_list_st_i2_2(self):
        return self.list_of_st_i2_2
    
    def get_list_st_i2_3(self):
        return self.list_of_st_i2_3
    
    def get_list_it_i2(self):
        return self.list_of_it_i2
    
    def get_list_st_w1(self):
        return self.list_of_st_w1
    
    def get_list_it_w1(self):
        return self.list_of_it_w1
    
    def get_list_st_w2(self):
        return self.list_of_st_w2
    
    def get_list_it_w2(self):
        return self.list_of_it_w2
    
    def get_list_st_w3(self):
        return self.list_of_st_w3
    
    def get_list_it_w3(self):
        return self.list_of_it_w3
    
    def get_product_1_count(self):
        return self.product_1_count
    
    def get_product_2_count(self):
        return self.product_2_count
    
    def get_product_3_count(self):
        return self.product_3_count
    
    def get_component_1_count(self):
        return self.comp_1_count
    
    def get_component_2_count(self):
        return self.comp_2_count
    
    def get_component_3_count(self):
        return self.comp_3_count
    
    def get_inspected_comp_1_count(self):
        return self.inspected_comp_1_count
    
    def get_inspected_comp_2_count(self):
        return self.inspected_comp_2_count
    
    def get_inspected_comp_3_count(self):
        return self.inspected_comp_3_count
    
    def get_component_1_time(self):
        return self.comp_1_time

    def get_component_2_time(self):
        return self.comp_2_time
    
    def get_component_3_time(self):
        return self.comp_3_time
