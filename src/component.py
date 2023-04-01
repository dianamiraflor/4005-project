class Component():

    def __init__(self, id):
        """
        id is to differentiate between the types of components
        id 1: component 1
        id 2: component 2
        id 3: component 3
        """
        self._start_time = 0
        self._inspecting_time_end = 0
        
        self._queue_start = 0
        
        self._end_time = 0                  # The time the component exits the system = the time when workstation starts assemble.
        
        self._time_spent = 0
        self._queue_time = 0
        
        self._is_ready = False
        self._id = id

    def set_start_time(self, time):
        self._start_time = time

    def set_inspecting_time_end(self, time):
        self._inspecting_time_end = time

    def set_queue_start_time(self, time):
        self._queue_start = time

    def set_end_time(self, time):
        self._end_time = time

    def set_queue_time(self):
        self._queue_time = self._end_time - self._queue_start

    def set_time_spent(self):
        self._time_spent = self._end_time - self._start_time

    def now_ready(self):
        self._is_ready = True

    def get_time_spent(self):
        return self._time_spent
    
    def get_id(self):
        return self._id
    
    def get_status(self):
        return self._is_ready