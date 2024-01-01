import math

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

# Unit tests
test_cases = [2, 7, 10, 13, 16]
expected_outputs = [True, True, False, True, False]

for i in range(len(test_cases)):
    output = is_prime(test_cases[i])
    if output == expected_outputs[i]:
        print(f"Test case {i+1} passed.")
    else:
        print(f"Test case {i+1} failed. Expected: {expected_outputs[i]}, Actual: {output}.")