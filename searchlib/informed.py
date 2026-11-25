"""Informed search: A* uses a heuristic to head towards the goal."""
from __future__ import annotations

import heapq
import itertools
from typing import Callable, Dict, List, Optional, Tuple

from .graph import Graph, Node, check_nodes, path_cost, reconstruct_path
from .result import SearchResult

INF = float("inf")
Heuristic = Callable[[Node], float]


def astar(graph: Graph, start: Node, goal: Node, heuristic: Heuristic) -> SearchResult:
    """A* search.

    Each node is ranked by ``f(n) = g(n) + h(n)`` where

        g(n) = cheapest known cost from the start to n
        h(n) = the heuristic's estimate of the cost from n to the goal

    If ``h`` never overestimates the true remaining cost (it is *admissible*),
    the path returned is optimal. See ``searchlib.heuristics`` for checkers.

    Implementation notes:
    * A node is expanded again if a cheaper route to it turns up later. That is
      what keeps the result optimal even when ``h`` is admissible but not
      consistent. With a consistent heuristic it never happens.
    * Stale heap entries (superseded by a cheaper route) are skipped on pop.
    """
    check_nodes(graph, start, goal)
    tie_breaker = itertools.count()
    frontier: List[Tuple[float, int, Node, float]] = [
        (heuristic(start), next(tie_breaker), start, 0)
    ]
    best_g: Dict[Node, float] = {start: 0}
    parent: Dict[Node, Optional[Node]] = {start: None}
    order: List[Node] = []

    while frontier:
        _, _, node, g = heapq.heappop(frontier)
        if g > best_g[node]:  # stale entry: a cheaper route was found since it was pushed
            continue
        order.append(node)
        if node == goal:
            path = reconstruct_path(parent, goal)
            return SearchResult(path, path_cost(graph, path), len(order), order)
        for neighbour, cost in graph[node].items():
            new_g = g + cost
            if new_g < best_g.get(neighbour, INF):
                best_g[neighbour] = new_g
                parent[neighbour] = node
                heapq.heappush(
                    frontier, (new_g + heuristic(neighbour), next(tie_breaker), neighbour, new_g)
                )
    return SearchResult(None, INF, len(order), order)
