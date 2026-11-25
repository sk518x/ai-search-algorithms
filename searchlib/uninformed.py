"""Uninformed search: algorithms that know nothing about where the goal is.

    bfs   - fewest edges (hops), uses a queue
    dfs   - finds *a* path, not necessarily a short one, uses a stack
    iddfs - depth-first memory use with breadth-first shortest-hops result
    ucs   - cheapest total cost (Dijkstra's algorithm) for weighted graphs

All of them take ``(graph, start, goal)`` and return a ``SearchResult``.
"""
from __future__ import annotations

import heapq
import itertools
from collections import deque
from typing import Dict, List, Optional, Set, Tuple

from .graph import Graph, Node, check_nodes, path_cost, reconstruct_path
from .result import SearchResult

INF = float("inf")


def _found(graph: Graph, parent: Dict[Node, Optional[Node]], goal: Node, order: List[Node]) -> SearchResult:
    path = reconstruct_path(parent, goal)
    return SearchResult(path, path_cost(graph, path), len(order), order)


def _not_found(order: List[Node]) -> SearchResult:
    return SearchResult(None, INF, len(order), order)


def bfs(graph: Graph, start: Node, goal: Node) -> SearchResult:
    """Breadth-first search. Returns the path with the fewest edges.

    ``parent`` does two jobs: it remembers how we reached each node (so we can
    rebuild the path) and it is the visited set. A dict lookup is O(1), unlike
    ``x in some_list`` which is O(n).
    """
    check_nodes(graph, start, goal)
    parent: Dict[Node, Optional[Node]] = {start: None}
    frontier = deque([start])
    order: List[Node] = []

    while frontier:
        node = frontier.popleft()
        order.append(node)
        if node == goal:
            return _found(graph, parent, goal, order)
        for neighbour in graph[node]:
            if neighbour not in parent:
                parent[neighbour] = node
                frontier.append(neighbour)
    return _not_found(order)


def dfs(graph: Graph, start: Node, goal: Node) -> SearchResult:
    """Depth-first search. Finds a path, but not necessarily the shortest one.

    Each stack entry remembers which node pushed it. A node's parent is only
    recorded when it is popped for the first time, so the recorded parents
    always form a valid depth-first tree.
    """
    check_nodes(graph, start, goal)
    parent: Dict[Node, Optional[Node]] = {}
    stack: List[Tuple[Node, Optional[Node]]] = [(start, None)]
    order: List[Node] = []

    while stack:
        node, came_from = stack.pop()
        if node in parent:
            continue
        parent[node] = came_from
        order.append(node)
        if node == goal:
            return _found(graph, parent, goal, order)
        # Reversed so the first neighbour is explored first (matches textbook order).
        for neighbour in reversed(list(graph[node])):
            if neighbour not in parent:
                stack.append((neighbour, node))
    return _not_found(order)


def _depth_limited(
    graph: Graph,
    node: Node,
    goal: Node,
    limit: int,
    path: List[Node],
    on_path: Set[Node],
    order: List[Node],
) -> Tuple[Optional[List[Node]], bool]:
    """One depth-limited DFS pass. Returns ``(path_or_None, hit_the_limit)``."""
    order.append(node)
    if node == goal:
        return list(path), False

    if limit == 0:
        # Did the limit stop us from exploring something new?
        return None, any(n not in on_path for n in graph[node])

    cutoff = False
    for neighbour in graph[node]:
        if neighbour in on_path:  # avoid walking in circles
            continue
        path.append(neighbour)
        on_path.add(neighbour)
        found, hit_limit = _depth_limited(graph, neighbour, goal, limit - 1, path, on_path, order)
        path.pop()
        on_path.remove(neighbour)
        if found is not None:
            return found, False
        cutoff = cutoff or hit_limit
    return None, cutoff


def iddfs(graph: Graph, start: Node, goal: Node, max_depth: Optional[int] = None) -> SearchResult:
    """Iterative-deepening DFS: run depth-limited DFS with limits 0, 1, 2, ...

    Finds the path with the fewest edges (like BFS) while only ever storing the
    current branch (like DFS). The price is repeated work: shallow nodes are
    expanded again on every pass, and that shows up in ``expanded``.

    Note: this only avoids cycles along the *current* branch, so it is meant
    for small graphs and trees. It is recursive, so very deep graphs can hit
    Python's recursion limit.
    """
    check_nodes(graph, start, goal)
    if max_depth is None:
        max_depth = len(graph) - 1
    order: List[Node] = []

    for limit in range(max_depth + 1):
        path, cutoff = _depth_limited(graph, start, goal, limit, [start], {start}, order)
        if path is not None:
            return SearchResult(path, path_cost(graph, path), len(order), order)
        if not cutoff:  # the whole reachable graph fit inside this limit: no goal
            break
    return _not_found(order)


def ucs(graph: Graph, start: Node, goal: Node) -> SearchResult:
    """Uniform-cost search (Dijkstra). Returns the cheapest path by total cost.

    The heap can hold several entries for one node (we push again whenever we
    find a cheaper route). Stale entries are skipped when popped.
    """
    check_nodes(graph, start, goal)
    tie_breaker = itertools.count()  # stops the heap from ever comparing nodes
    frontier: List[Tuple[float, int, Node]] = [(0, next(tie_breaker), start)]
    best: Dict[Node, float] = {start: 0}
    parent: Dict[Node, Optional[Node]] = {start: None}
    closed: Set[Node] = set()
    order: List[Node] = []

    while frontier:
        g, _, node = heapq.heappop(frontier)
        if node in closed:
            continue
        closed.add(node)
        order.append(node)
        if node == goal:
            return _found(graph, parent, goal, order)
        for neighbour, cost in graph[node].items():
            new_g = g + cost
            if new_g < best.get(neighbour, INF):
                best[neighbour] = new_g
                parent[neighbour] = node
                heapq.heappush(frontier, (new_g, next(tie_breaker), neighbour))
    return _not_found(order)
