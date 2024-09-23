import random
import time
import time
from magic import *


def gen_random_arrs(size):
    arr1 = list(range(1, size + 1))

    arr_random = []
    for i in range(size):
        arr_random.append(arr1.pop(random.randint(0, len(arr1) - 1)))

    arr1 = list(range(1, size + 1))

    arr_random2 = []
    for i in range(size):
        arr_random2.append(arr1.pop(random.randint(0, len(arr1) - 1)))

    return arr_random, arr_random2


A, B = gen_random_arrs(9)

binary_times = []
non_binary_times = []

for i in range(10):
    start_time = time.time()
    result_smart = dynamic_potion_sort(A.copy(), B.copy())
    binary_times.append(time.time() - start_time)

    start_time = time.time()
    result_non_binary = brute_sort_potions(A.copy(), B.copy())
    non_binary_times.append(time.time() - start_time)

print(f"binary in {float(sum(binary_times)) / len(binary_times) * 1000}ms average")

print(
    f"non binary in {float(sum(non_binary_times)) / len(binary_times) * 1000}ms average"
)
