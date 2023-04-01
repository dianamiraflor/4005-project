"""
buffer.py will be implemented as a queue
"""
from component import Component

class Buffer():
    
    def __init__(self, id):
        """
        Given an id to differentiate between the buffers
        id 1: c1w1
        id 2: c1w2
        id 3: c2w2
        id 4: c1w3
        id 5: c3w3

        TODO: Maybe add workstation id ?
        """
        self._id = id                       # Queue ID

        self._buffer_capacity = 2           # Max buffer capacity
        self._buffer_length = 0             # Current buffer size

        self._Queue = []
        self._QueueLengthTime =[[0, 0.0]]   # [[queue_length, clock]] TODO: Will be used for stats

        self._total_count = 0               # This will measure the amount of times put() was called. 
                                            # Or the amount of times a component has been placed in the buffer


    def put(self, comp: Component, time):
        """
        Called by the INSPECTOR
        """

        # Check buffer size
        if self._buffer_length == self._buffer_capacity:
            print(f'Buffer {self._id} at max capacity.')
            return False

        # If there's space then put in the buffer
        else: 
            self._buffer_length += 1  
            self._total_count += 1 
            self._Queue.append(comp)
            self._QueueLengthTime.append([self._buffer_length, time])
            comp.set_queue_time(time)
            return True


    def get(self, time):
        """
        Called by the WORKSTATION
        """

        component = None

        if self._buffer_length == 0:
            print(f'No components available in buffer {self._id}')
            return None
        else:
            self._buffer_length -= 1
            component = self._Queue.pop(0)
            component.set_assembly_time(time)
            self._QueueLengthTime.append([self._buffer_length, time])

            return component
        
    def get_total_count(self):
        return self._total_count
    
    def get_queue_length_time(self):
        return self._QueueLengthTime

       
