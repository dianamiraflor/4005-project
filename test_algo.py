from src.constants import C1W1, C1W2, C1W3

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


if __name__ == '__main__':
    test1 = get_chosen_buffer(0, 0, 0)
    print("Expected: C1W1, Result: " + str(test1))

    test2 = get_chosen_buffer(2, 1, 1)
    print("Expected: C1W2, Result: " + str(test2))

    test3 = get_chosen_buffer(2, 2, 0)
    print("Expected: C1W3, Result: " + str(test3))

    test4 = get_chosen_buffer(1, 1, 2)
    print("Expected: C1W1, Result: " + str(test4))