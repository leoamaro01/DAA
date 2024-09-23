from math import ceil, log2


def brute_sort_potions(A: list[int], B: list[int]):
    n = len(A)

    indexes_A = [-1] * n
    indexes_B = [-1] * n

    for i in range(n):
        indexes_A[A[i] - 1] = i
        indexes_B[B[i] - 1] = i

    best_result = -1
    best_swap_elem = -1
    best_swaps = []
    for i in range(0, n):
        elem = i + 1
        if A[i] == elem and B[i] == elem:
            continue

        swap_items(A, i, indexes_A[i])
        swap_items(B, i, indexes_B[i])

        swaps = brute_sort_potions(A, B)

        swap_items(A, i, indexes_A[i])
        swap_items(B, i, indexes_B[i])

        if best_result == -1 or len(swaps) < best_result:
            best_result = len(swaps)
            best_swaps = swaps
            best_swap_elem = elem

    if best_result == -1:
        return []

    return [best_swap_elem, *best_swaps]


def dynamic_potion_sort(A: list[int], B: list[int]):
    moves = {}
    n = len(A)

    indexes_A = [-1] * n
    indexes_B = [-1] * n

    for i in range(n):
        indexes_A[A[i] - 1] = i
        indexes_B[B[i] - 1] = i

    bits_per_item = int(ceil(log2(n)))

    initial_identifier_A = A[n - 1]
    initial_identifier_B = B[n - 1]

    for i in range(n - 2, -1, -1):
        initial_identifier_A <<= bits_per_item
        initial_identifier_A |= A[i]

        initial_identifier_B <<= bits_per_item
        initial_identifier_B |= B[i]

    return dynamic_potion_sort_aux(
        A,
        B,
        moves,
        indexes_A,
        indexes_B,
        (initial_identifier_A, initial_identifier_B),
        bits_per_item,
    )


def dynamic_potion_sort_aux(
    A: list[int],
    B: list[int],
    moves: dict[tuple[int, int], list[int]],
    indexes_A: list[int],
    indexes_B: list[int],
    lists_repr: tuple[int, int],
    bits_per_item: int,
) -> list[int]:
    if lists_repr in moves:
        return moves[lists_repr]

    n = len(A)

    best_swaps_count = -1
    best_swaps = []
    best_swap_elem = -1
    for i in range(n):
        elem = i + 1

        # skip item if correct
        if A[i] == elem and B[i] == elem:
            continue

        A_item_at_i = A[i]
        B_item_at_i = B[i]

        i_index_A = indexes_A[i]
        i_index_B = indexes_B[i]

        # swap potions
        swap_items(A, i, i_index_A)
        swap_items(B, i, i_index_B)

        # update indexes array
        swap_items(indexes_A, A_item_at_i - 1, i)
        swap_items(indexes_B, B_item_at_i - 1, i)

        # update lists representation
        new_A_repr = (lists_repr[0] ^ (A_item_at_i << (bits_per_item * i))) ^ (
            (i + 1) << (bits_per_item * i_index_A)
        )
        new_A_repr |= (A_item_at_i << (bits_per_item * i_index_A)) | (
            (i + 1) << (bits_per_item * i)
        )

        new_B_repr = (lists_repr[1] ^ (B_item_at_i << (bits_per_item * i))) ^ (
            (i + 1) << (bits_per_item * i_index_B)
        )
        new_B_repr |= (B_item_at_i << (bits_per_item * i_index_B)) | (
            (i + 1) << (bits_per_item * i)
        )

        swaps = dynamic_potion_sort_aux(
            A,
            B,
            moves,
            indexes_A,
            indexes_B,
            (new_A_repr, new_B_repr),
            bits_per_item,
        )

        # revert swap
        swap_items(A, i, i_index_A)
        swap_items(B, i, i_index_B)

        # revert indexes array update
        swap_items(indexes_A, A_item_at_i - 1, i)
        swap_items(indexes_B, B_item_at_i - 1, i)

        if best_swaps_count == -1 or len(swaps) < best_swaps_count:
            best_swaps = swaps
            best_swaps_count = len(swaps)
            best_swap_elem = elem

    if best_swaps_count == -1:
        return []

    result = [best_swap_elem, *best_swaps]

    moves[lists_repr] = result

    return result


def swap_items(A: list[int], index1: int, index2: int):
    temp = A[index1]
    A[index1] = A[index2]
    A[index2] = temp
