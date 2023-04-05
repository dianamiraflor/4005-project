class System():
    
    def __init__(self):
        self.current_component_num = 0
        self.total_component_num = 0 

    def add_current_comp(self, amount):
        self.current_component_num += amount

    def dec_current_comp(self, amount):
        temp_count = self.current_component_num - amount

        if self.current_component_num == 0 or temp_count < 0:
            self.current_component_num = 0
        else: 
            self.current_component_num -= amount

    def add_total_components(self):
        self.total_component_num += 1

    def get_current_comp(self):
        return self.current_component_num
    
    def get_total_component_num(self):
        return self.total_component_num