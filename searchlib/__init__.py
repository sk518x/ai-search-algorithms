"""searchlib: BFS, DFS, IDDFS, UCS and A* with tests and benchmarks."""
from .graph import Graph, build_graph, path_cost
from .heuristics import (
    inadmissible_nodes,
    inconsistent_edges,
    is_admissible,
    is_consistent,
    manhattan,
    true_costs_to,
    zero,
)
from .informed import astar
from .result import SearchResult
from .uninformed import bfs, dfs, iddfs, ucs

__all__ = [
    "Graph", "build_graph", "path_cost", "SearchResult",
    "bfs", "dfs", "iddfs", "ucs", "astar",
    "manhattan", "zero", "true_costs_to",
    "is_admissible", "inadmissible_nodes", "is_consistent", "inconsistent_edges",
]
