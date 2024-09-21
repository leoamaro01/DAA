import math


def div(A, n=0, m=-1):
    if m == -1:
        m = calcMEX(A, 0, len(A))

    res = 0
    if is_valid(A, n, len(A), m):
        res = 1

    for i in range(n + 1, len(A)):
        if is_valid(A, n, i, m):
            res += div(A, i, m)
    return res


def calcMEX(A, i=0, j=-1):
    j = len(A) if j == -1 else j
    found = {}
    max = -1
    for k in range(i, j):
        found[A[k]] = True
        if A[k] > max:
            max = A[k]

    if max < 0:
        return 0

    for i in range(max):
        if i not in found:
            return i

    return max + 1


def is_valid(A, i, j, m):
    return calcMEX(A, i, j) == m


def divide(A):
    n = len(A)
    m = calcMEX(A)

    if m == 0:
        return 2 ** (n - 1)

    blocks: dict[tuple[int, int], int] = {}
    sub_m_indexes = [-1] * m

    last_block_start = 0

    matched = 0

    for i in range(n):
        v = A[i]
        if v < m:
            if sub_m_indexes[v] == -1:
                matched += 1
            sub_m_indexes[v] = i

            if matched == m:
                q, q_i = find_min(sub_m_indexes)

                if len(blocks) == 0:
                    blocks[(q, i)] = 1
                    sub_m_indexes = [-1] * m
                    matched = 0
                else:
                    value = 0
                    for block in blocks:
                        if block[1] >= q:
                            continue
                        k = q - max(block[1], last_block_start) - 1
                        value += blocks[block] * (k + 1)

                    blocks[(q, i)] = value
                    last_block_start = q

                    sub_m_indexes[q_i] = -1
                    matched -= 1
    return sum(blocks.values())


def find_min(B):
    m = B[0]
    m_i = 0
    for i in range(1, len(B)):
        if B[i] < m:
            m_i = i
            m = B[i]
    return m, m_i


arr1 = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3]
arr2 = [2, 5, 33, 14, 8, 5, 0, 12, 7, 0, 2]
arr3 = [5, 33, 0, 8, 5, 0, 12, 7, 0]
arr4 = [1, 0, 2, 5, 2, 6, 2, 0, 8, 5, 1, 8, 2, 7, 1, 2, 0]
arr5 = [1, 0, 9, 9, 5, 0, 8, 5, 1, 6, 7, 0, 1]
arr6 = [5, 6, 33, 0, 8, 5, 1, 0, 1, 0, 12, 7, 0, 1]
arr7 = [1, 34, 123, 0, 425, 31, 12, 45, 1, 0, 34, 34, 1, 0, 54, 22, 17]
arr8 = [0, 1, 2, 3, 4, 5, 34, 21, 12, 1, 21, 0, 34, 2, 16, 21, 43, 5, 4, 3, 2, 1, 0]
arr9 = [2, 3, 0, 1, 4, 1, 4, 0, 2, 1, 1, 4, 3, 0, 3, 1, 2, 0, 4, 1, 2, 3]
arr10 = [0, 0, 0, 0, 0, 0, 0]

super_arr = []

for i in range(1):
    super_arr += arr8

print(divide(arr9))

print(div(arr9))
