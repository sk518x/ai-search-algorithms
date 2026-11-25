"""Heuristic helpers: factories for common heuristics and checkers for the
two properties that decide whether A* can be trusted."""
from __future__ import annotations

import heapq
import itertools
from typing import Callable, Dict, List, Tuple

from .graph import Graph, Node, reverse_graph

INF = float("inf")
Heuristic = Callable[[Node], float]
EPSILON = 1e-9


def manhattan(goal: Tuple[int, int]) -> Heuristic:
    """Manhattan distance to ``goal`` for grid nodes ``(x, y)`` with 4-way moves and cost 1."""
    gx, gy = goal
    return lambda node: abs(node[0] - gx) + abs(node[1] - gy)


def zero(_node: Node) -> float:
    """The heuristic that knows nothing. A* with this behaves exactly like UCS."""
    return 0.0


def true_costs_to(graph: Graph, goal: Node) -> Dict[Node, float]:
    """Exact cheapest cost from every node *to* ``goal`` (Dijkstra on the reversed graph)."""
    reverse = reverse_graph(graph)
    tie_breaker = itertools.count()
    dist: Dict[Node, float] = {goal: 0}
    frontier: List[Tuple[float, int, Node]] = [(0, next(tie_breaker), goal)]
    while frontier:
        d, _, node = heapq.heappop(frontier)
        if d > dist[node]:
            continue
        for neighbour, cost in reverse[node].items():
            nd = d + cost
            if nd < dist.get(neighbour, INF):
                dist[neighbour] = nd
                heapq.heappush(frontier, (nd, next(tie_breaker), neighbour))
    return dist


def inadmissible_nodes(graph: Graph, goal: Node, h: Heuristic) -> List[Tuple[Node, float, float]]:
    """Nodes where ``h`` overestimates. Returns ``(node, h_value, true_cost)`` tuples.

    Admissible means ``h(n) <= true cost from n to goal`` for every node.
    An empty list means the heuristic is admissible, so A* will be optimal.
    """
    true_cost = true_costs_to(graph, goal)
    return [
        (node, h(node), true_cost[node])
        for node in graph
        if node in true_cost and h(node) > true_cost[node] + EPSILON
    ]


def is_admissible(graph: Graph, goal: Node, h: Heuristic) -> bool:
    return not inadmissible_nodes(graph, goal, h)


def inconsistent_edges(graph: Graph, goal: Node, h: Heuristic) -> List[Tuple[Node, Node]]:
    """Edges ``u -> v`` that break ``h(u) <= cost(u, v) + h(v)``, plus the goal rule ``h(goal) == 0``."""
    bad = [
        (u, v)
        for u, neighbours in graph.items()
        for v, cost in neighbours.items()
        if h(u) > cost + h(v) + EPSILON
    ]
    if abs(h(goal)) > EPSILON:
        bad.append((goal, goal))
    return bad


def is_consistent(graph: Graph, goal: Node, h: Heuristic) -> bool:
    """Consistent (monotone) heuristics never need a node to be expanded twice."""
    return not inconsistent_edges(graph, goal, h)
