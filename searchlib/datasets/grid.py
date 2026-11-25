"""Random grid mazes for benchmarking on graphs bigger than a few towns."""
from __future__ import annotations

import random
from typing import Tuple

from searchlib.graph import Graph, build_graph
from searchlib.uninformed import bfs

Cell = Tuple[int, int]


def make_grid(width: int, height: int, wall_probability: float, seed: int) -> Graph:
    """A ``width`` x ``height`` grid with randomly placed walls.

    Nodes are ``(x, y)`` cells; each open cell connects to its open
    up/down/left/right neighbours at cost 1. The corners ``(0, 0)`` and
    ``(width-1, height-1)`` are always open.
    """
    rng = random.Random(seed)
    corners = {(0, 0), (width - 1, height - 1)}
    open_cells = {
        (x, y)
        for x in range(width)
        for y in range(height)
        if (x, y) in corners or rng.random() >= wall_probability
    }
    edges = []
    for x, y in open_cells:
        for neighbour in ((x + 1, y), (x, y + 1)):
            if neighbour in open_cells:
                edges.append(((x, y), neighbour))
    graph = build_graph(edges)
    for cell in open_cells:  # keep isolated open cells as nodes too
        graph.setdefault(cell, {})
    return graph


def solvable_grid(width: int, height: int, wall_probability: float, seed: int) -> Tuple[Graph, Cell, Cell]:
    """Return ``(graph, start, goal)`` for the first seed >= ``seed`` that has a path."""
    start, goal = (0, 0), (width - 1, height - 1)
    while True:
        graph = make_grid(width, height, wall_probability, seed)
        if bfs(graph, start, goal).found:
            return graph, start, goal
        seed += 1
