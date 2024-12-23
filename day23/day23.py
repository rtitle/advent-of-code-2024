from collections import defaultdict
from itertools import permutations
import networkx as nx

def parse_input(filename: str) -> list[tuple[str]]:
    with open(filename, 'r') as file:
        lines = file.readlines()
    res = []
    for line in lines:
        [l, r] = line.strip().split("-")
        res.append((l, r))
    return res
    
def make_graph(lines: list[tuple[str]]) -> dict[str, list[str]]:
    graph = defaultdict(list)
    for l, r in lines:
        graph[l].append(r)
        graph[r].append(l)
    return graph

def do_part_1(graph: dict[str, list[str]]) -> int:
    triples = set()
    for k, v in graph.items():
        for [a, b] in permutations(v, 2):
            if k.startswith("t") or a.startswith("t") or b.startswith("t"):
                if b in graph[a] or a in graph[b]:
                    triples.add(frozenset([k, a, b]))
    return len(triples)

def do_part_1_networkx(lines: list[tuple[str]]) -> int:
    graph = nx.Graph()
    graph.add_edges_from(lines)
    cliques = nx.enumerate_all_cliques(graph)
    valid_clique = lambda c: len(c) == 3 and any(x.startswith("t") for x in c)
    return len(list(filter(valid_clique, cliques)))

def do_part_2(graph: dict[str, list[str]]) -> str:
    pass

# I don't feel great about this
def do_part_2_networkx(lines: list[tuple[str]]) -> str:
    graph = nx.Graph()
    graph.add_edges_from(lines)
    cliques = list(nx.find_cliques(graph))
    largest_clique = max(cliques, key=len)
    return ",".join(sorted(largest_clique))

filename = "day23/input.txt"
lines = parse_input(filename)
graph = make_graph(lines)
part1 = do_part_1(graph)
print(part1)
part1_networkx = do_part_1_networkx(lines)
print(part1_networkx)
part2_networkx = do_part_2_networkx(lines)
print(part2_networkx)