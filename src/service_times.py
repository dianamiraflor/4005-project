import data_wrapper
import random

class ServiceTimes():
    def __init__(self):
        self.i1_st = data_wrapper.inspector1_1_st()
        self.i2_2_st = data_wrapper.inspector2_2_st()
        self.i2_3_st = data_wrapper.inspector2_3_st()

        self.w1_st = data_wrapper.workstation1_st()
        self.w2_st = data_wrapper.workstation2_st()
        self.w3_st = data_wrapper.workstation3_st()

    
    def get_random_i1_st(self) -> float: 
        return random.choice(self.i1_st)
    
    def get_random_i2_2_st(self) -> float:
        return random.choice(self.i2_2_st)

    def get_random_i2_3_st(self) -> float:
        return random.choice(self.i2_3_st)

    def get_random_w1_st(self) -> float:
        return random.choice(self.w1_st)
    
    def get_random_w2_st(self) -> float:
        return random.choice(self.w2_st)

    def get_random_w3_st(self) -> float:
        return random.choice(self.w3_st)

