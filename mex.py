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
