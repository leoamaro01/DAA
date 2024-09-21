import random
import time


def sort_potions(A: list[int], B: list[int]):
    n = len(A)

    indexes_A = [-1] * n
    indexes_B = [-1] * n

    for i in range(n):
        indexes_A[A[i] - 1] = i
        indexes_B[B[i] - 1] = i

    best_result = -1
    best_swaps = []
    for i in range(0, n):
        elem = i + 1
        if A[i] == elem and B[i] == elem:
            continue

        swap_items(A, i, indexes_A[i])
        swap_items(B, i, indexes_B[i])

        swaps = sort_potions(A, B)

        swap_items(A, i, indexes_A[i])
        swap_items(B, i, indexes_B[i])

        if best_result == -1 or len(swaps) < best_result:
            best_result = len(swaps)
            best_swaps = swaps

    return [i, *best_swaps]


def dynamic_potion_sort(A: list[int], B: list[int]):
    moves = {}
    return dynamic_potion_sort_aux(A, B, moves)


def dynamic_potion_sort_aux(A: list[int], B: list[int], moves: dict[str, list[int]]):
    list_repr = (tuple(A), tuple(B))
    if list_repr in moves:
        return moves[list_repr]

    n = len(A)

    indexes_A = [-1] * n
    indexes_B = [-1] * n

    for i in range(n):
        indexes_A[A[i] - 1] = i
        indexes_B[B[i] - 1] = i

    best_swaps_count = -1
    best_swaps = []
    for i in range(n):
        elem = i + 1

        if A[i] == elem and B[i] == elem:
            continue

        swap_items(A, i, indexes_A[i])
        swap_items(B, i, indexes_B[i])

        swaps = dynamic_potion_sort_aux(A, B, moves)

        swap_items(A, i, indexes_A[i])
        swap_items(B, i, indexes_B[i])

        if best_swaps_count == -1 or len(swaps) < best_swaps_count:
            best_swaps = swaps
            best_swaps_count = len(swaps)

    result = [i + 1, *best_swaps]

    moves[list_repr] = result

    return result


def swap_items(A: list[int], index1: int, index2: int):
    temp = A[index1]
    A[index1] = A[index2]
    A[index2] = temp


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


def try_func(A, B, f):
    print(A)
    print(B)
    print()
    sort_order = f(A.copy(), B.copy())

    for i in range(len(sort_order)):
        print(sort_order[i])
        swap_items(A, sort_order[i])
        swap_items(B, sort_order[i])
        print(A)
        print(B)
        print()

    return sort_order


tests = 1000

for _ in range(tests):
    A, B = gen_random_arrs(20)

    start_time = time.time()
    result_brute_force = dynamic_potion_sort(A.copy(), B.copy())
    print(f"done dynamic sort in {int((time.time() - start_time) * 1000)}ms")

    start_time = time.time()
    result_smart = sort_potions(A.copy(), B.copy())
    print(f"done brute sort in {int((time.time() - start_time) * 1000)}ms")
