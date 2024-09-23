import random
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

start_time = time.time()
result_smart = dynamic_potion_sort(A.copy(), B.copy())

print(result_smart)
print("Smart time: ", time.time() - start_time, "s")
