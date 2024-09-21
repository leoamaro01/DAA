import random


class Graph:
    def __init__(self, size: int, adj_list: dict[int, dict[int, bool]]) -> None:
        self.size = size
        self.adj_list = adj_list

    def has_edge(self, u: int, v: int):
        return (u in self.adj_list and v in self.adj_list[u]) or (
            v in self.adj_list and u in self.adj_list[v]
        )

    def is_covered(self, cover: list[int]):
        for vertex in self.adj_list:
            if vertex in cover:
                continue
            for edge_end in self.adj_list[vertex]:
                if edge_end not in cover:
                    return False
        return True


def find_min_cover(G: Graph, costs: list[int]):
    return find_min_cover_aux(G, costs, 0, [])


def find_min_cover_aux(
    G: Graph, costs: list[int], current_cost: int, current_cover: list[int]
):
    if G.is_covered(current_cover):
        return current_cover, current_cost

    best_cover_length = -1
    best_cover = []
    best_cost = -1
    for v in range(G.size):
        if v in current_cover:
            continue

        cover, cost = find_min_cover_aux(
            G, costs, current_cost + costs[v], current_cover + [v]
        )
        cover_length = len(cover)

        if cover_length == best_cover_length:
            if cost < best_cost:
                best_cover = cover
                best_cost = cost
        elif best_cover_length == -1 or cover_length < best_cover_length:
            best_cover = cover
            best_cost = cost
            best_cover_length = cover_length
    return best_cover, best_cost


def find_min_cover_approx(G: Graph, costs: list[int]):
    cover = []
    cost = 0

    edges = []

    for u in G.adj_list:
        for v in G.adj_list[u]:
            edges.append((costs[u] + costs[v], (u, v)))

    edges.sort(key=lambda item: item[0])

    while len(edges) > 0:
        c, (u, v) = edges[0]
        cost += c

        cover.append(u)
        cover.append(v)

        new_edges = []

        for e_c, (e1, e2) in edges:
            if e1 == u or e1 == v or e2 == u or e2 == v:
                continue
            new_edges.append((e_c, (e1, e2)))

        edges = new_edges
    return cover, cost


G: Graph = Graph(
    7,
    {
        0: {1: True, 3: True},
        1: {4: True},
        2: {3: True, 5: True},
        3: {4: True, 6: True, 5: True},
        4: {6: True},
    },
)

G2: Graph = Graph(
    20,
    {
        0: {1: True, 2: True},
        1: {0: True, 3: True, 4: True},
        2: {0: True, 5: True, 6: True},
        3: {1: True, 7: True, 8: True},
        4: {1: True, 9: True, 10: True},
        5: {2: True, 11: True, 12: True},
        6: {2: True, 13: True, 14: True},
        7: {3: True, 15: True, 16: True},
        8: {3: True, 17: True, 18: True},
        9: {4: True, 19: True},
        10: {4: True, 11: True},
        11: {5: True, 10: True, 12: True},
        12: {5: True, 11: True, 13: True},
        13: {6: True, 12: True, 14: True},
        14: {6: True, 13: True, 15: True},
        15: {7: True, 14: True, 16: True},
        16: {7: True, 15: True, 17: True},
        17: {8: True, 16: True, 18: True},
        18: {8: True, 17: True, 19: True},
        19: {9: True, 18: True},
    },
)

G3: Graph = Graph(
    15,
    {
        0: {1: True, 2: True},
        1: {0: True, 3: True, 4: True},
        2: {0: True, 5: True, 6: True},
        3: {1: True, 7: True, 8: True},
        4: {1: True, 9: True, 10: True},
        5: {2: True, 11: True, 12: True},
        6: {2: True, 13: True, 14: True},
        7: {3: True, 8: True, 9: True},
        8: {3: True, 7: True, 10: True},
        9: {4: True, 7: True, 11: True},
        10: {4: True, 8: True, 12: True},
        11: {5: True, 9: True, 13: True},
        12: {5: True, 10: True, 14: True},
        13: {6: True, 11: True, 14: True},
        14: {6: True, 12: True, 13: True},
    },
)

costs = []

for i in range(15):
    costs.append(random.randint(5, 20))

print(costs)
print(sum(costs) / float(len(costs)))
print(find_min_cover_approx(G3, costs))
print(find_min_cover(G3, costs))
