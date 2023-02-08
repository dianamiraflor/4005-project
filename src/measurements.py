measured_service_times = {
    'inspector_1' : [],
    'inspector_2' : [],
    'workstation_1' : [],
    'workstation_2' : [],
    'workstation_3' : []
}

# Idle time for an inspector = Blocked inspector
measured_idle_times = {
    'inspector_1' : [],
    'inspector_2' : [],
    'workstation_1' : [],
    'workstation_2' : [],
    'workstation_3' : []
}

# To find throughput
products_assembled = {
    'p1': 0,
    'p2' : 0,
    'p3' : 0
}

# Time a component has been in a buffer


def add_measured_service_time(process, st):
    measured_service_times[process].append(st)

def add_measured_idle_time(process, it):
    measured_idle_times[process].append(it)

def add_assembled_product(product):
    products_assembled[product] += 1

def get_measured_service_times(process):
    return measured_service_times[process]

def get_measured_idle_times(process):
    return measured_idle_times[process]

def get_products_assembled(product):
    return products_assembled[product]

