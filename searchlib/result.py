"""The value every search algorithm returns."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from .graph import Node


@dataclass(frozen=True)
class SearchResult:
    """Outcome of one search.

    path:     start -> goal as a list of nodes, or ``None`` if the goal is unreachable.
    cost:     total path cost (``inf`` when there is no path).
    expanded: how many nodes the algorithm took off its frontier and examined.
              This is the number we compare between algorithms: fewer is better.
    order:    the nodes in the order they were expanded (IDDFS lists repeats,
              because it really does re-expand nodes on every deeper pass).
    """

    path: Optional[List[Node]]
    cost: float
    expanded: int
    order: List[Node] = field(default_factory=list)

    @property
    def found(self) -> bool:
        return self.path is not None

    @property
    def hops(self) -> Optional[int]:
        """Number of edges in the path (``None`` if no path)."""
        return None if self.path is None else len(self.path) - 1
