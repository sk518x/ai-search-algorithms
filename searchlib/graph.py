"""Graph representation and small helpers shared by every algorithm.

A graph is a plain dictionary of dictionaries:

    {"A": {"B": 4, "C": 2}, "B": {"A": 4}, "C": {"A": 2}}

``graph[u][v]`` is the cost of travelling from ``u`` to ``v``.
Using a dict for the neighbours (instead of a list plus a separate weights
table) keeps the cost next to the edge and makes lookups O(1).
"""
from __future__ import annotations

from typing import Dict, Hashable, Iterable, List, Optional, Sequence, Tuple, Union

Node = Hashable
Graph = Dict[Node, Dict[Node, float]]
Edge = Union[Tuple[Node, Node], Tuple[Node, Node, float]]


def build_graph(edges: Iterable[Edge], directed: bool = False) -> Graph:
    """Build a graph from ``(u, v)`` or ``(u, v, cost)`` tuples.

    * A missing cost defaults to 1 (an unweighted edge).
    * Negative costs are rejected, because UCS and A* assume non-negative costs.
    * If the same edge is listed twice, the cheaper cost wins.
    * Undirected graphs (the default) get the edge in both directions.
    """
    graph: Graph = {}
    for edge in edges:
        if len(edge) == 2:
            u, v = edge
            cost = 1
        elif len(edge) == 3:
            u, v, cost = edge
        else:
            raise ValueError(f"edge must be (u, v) or (u, v, cost), got {edge!r}")
        if cost < 0:
            raise ValueError(f"negative cost on edge {u!r} -> {v!r}: {cost}")

        graph.setdefault(u, {})
        graph.setdefault(v, {})
        graph[u][v] = min(cost, graph[u].get(v, cost))
        if not directed:
            graph[v][u] = min(cost, graph[v].get(u, cost))
    return graph


def reverse_graph(graph: Graph) -> Graph:
    """Return the graph with every edge direction flipped."""
    reversed_graph: Graph = {node: {} for node in graph}
    for u, neighbours in graph.items():
        for v, cost in neighbours.items():
            reversed_graph[v][u] = cost
    return reversed_graph


def check_nodes(graph: Graph, *nodes: Node) -> None:
    """Raise ``ValueError`` if any node is not in the graph."""
    for node in nodes:
        if node not in graph:
            raise ValueError(f"unknown node: {node!r}")


def path_cost(graph: Graph, path: Sequence[Node]) -> float:
    """Total cost of walking ``path``. Raises if two consecutive nodes are not connected."""
    total = 0
    for u, v in zip(path, path[1:]):
        if v not in graph.get(u, {}):
            raise ValueError(f"no edge from {u!r} to {v!r}")
        total += graph[u][v]
    return total


def reconstruct_path(parent: Dict[Node, Optional[Node]], goal: Node) -> List[Node]:
    """Walk the ``parent`` links back from ``goal`` to the start node."""
    path = [goal]
    while parent[path[-1]] is not None:
        path.append(parent[path[-1]])
    path.reverse()
    return path
