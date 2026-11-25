"""Show why IDDFS does not scale to grids: expansions explode while BFS stays tiny.

    python -m benchmarks.iddfs_scaling

Each IDDFS run gets a time limit and is killed if it exceeds it, so the script
always finishes (works on Windows, macOS and Linux).
"""
from __future__ import annotations

import multiprocessing as mp
import sys
import time

from searchlib import bfs, iddfs
from searchlib.datasets.grid import solvable_grid

SIZES = (6, 8, 10, 12, 15)
TIME_LIMIT_SECONDS = 10


def _run_iddfs(size: int, queue) -> None:
    sys.setrecursionlimit(10_000)
    graph, start, goal = solvable_grid(size, size, 0.25, 1)
    t0 = time.perf_counter()
    result = iddfs(graph, start, goal)
    queue.put((result.expanded, time.perf_counter() - t0))


def main() -> None:
    print(f"| Grid | BFS expanded | IDDFS expanded | IDDFS time |")
    print("|---|---:|---:|---:|")
    for size in SIZES:
        graph, start, goal = solvable_grid(size, size, 0.25, 1)
        bfs_expanded = bfs(graph, start, goal).expanded
        queue = mp.Queue()
        worker = mp.Process(target=_run_iddfs, args=(size, queue))
        worker.start()
        worker.join(TIME_LIMIT_SECONDS)
        if worker.is_alive():
            worker.terminate()
            worker.join()
            print(f"| {size}x{size} | {bfs_expanded} | did not finish | > {TIME_LIMIT_SECONDS} s |")
        else:
            expanded, seconds = queue.get()
            print(f"| {size}x{size} | {bfs_expanded} | {expanded:,} | {seconds:.2f} s |")


if __name__ == "__main__":
    main()
