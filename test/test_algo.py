"""
test_algo.py tests the algorithms for choosing a buffer for inspector 1.

Author: Diana Miraflor
Carleton University
"""
from src.constants import C1W1, C1W2, C1W3, buffer_capacity

def get_chosen_buffer(c1w1, c1w2, c1w3):
    chosen_buffer = C1W1

    # If all the same
    if c1w1 == c1w2 == c1w3:
        print("heree1")
        return chosen_buffer
    
    # Case 1: First buffer (W1) has the lowest amount
    if c1w1 <= c1w2 & c1w1 <= c1w3:
        print("heree2")
        return chosen_buffer

    if c1w2 <= c1w3 | c1w2 < c1w1:
        print("here3")
        chosen_buffer = C1W2
        return chosen_buffer
    
    print("here4")
    chosen_buffer = C1W3
    return chosen_buffer

def get_chosen_buffer_at_capacity(facility):
    # If they are all full 
    # Block 
    free_c1w1 = False
    free_c1w2 = False
    free_c1w3 = False
    chosen_buffer = C1W1
    while (not free_c1w1) & (not free_c1w2) & (not free_c1w3):
        current_c1w1_level = facility.c1w1.level
        current_c1w2_level = facility.c1w2.level
        current_c1w3_level = facility.c1w3.level
        # Wait until one is full
        if current_c1w1_level < buffer_capacity:
            free_c1w1 = True
        if current_c1w2_level < buffer_capacity:
            chosen_buffer = C1W2
            free_c1w2 = True
        if current_c1w3_level < buffer_capacity:
            chosen_buffer = C1W3
            free_c1w3 = True

    return chosen_buffer

if __name__ == '__main__':

    # -------------------------------------- TS 1
    test1 = get_chosen_buffer(0, 0, 0)
    print("Expected: C1W1, Result: " + str(test1))

    test2 = get_chosen_buffer(2, 1, 1)
    print("Expected: C1W2, Result: " + str(test2))

    test3 = get_chosen_buffer(2, 2, 0)
    print("Expected: C1W3, Result: " + str(test3))

    test4 = get_chosen_buffer(1, 1, 2)
    print("Expected: C1W1, Result: " + str(test4))


    # -------------------------------------- TS 2
    # ------------ In progress -------------
    # test1 = get_chosen_buffer_at_capacity()
    # print("Expected: C1W1, Result: " + str(test1))
    
    # test2 = get_chosen_buffer_at_capacity(2, 1, 1)
    # print("Expected: C1W2, Result: " + str(test2))

    # test3 = get_chosen_buffer_at_capacity(2, 2, 0)
    # print("Expected: C1W3, Result: " + str(test3))

    # test4 = get_chosen_buffer_at_capacity(1, 1, 2)
    # print("Expected: C1W1, Result: " + str(test4))
