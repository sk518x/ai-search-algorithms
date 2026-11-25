"""Compare the algorithms on (1) the North West road graph and (2) random grid mazes.

Run from the repository root:

    python -m benchmarks.run_benchmarks            # print tables
    python -m benchmarks.run_benchmarks --write    # also save benchmarks/results.md

Metrics
    expanded - nodes examined; the hardware-independent measure of effort
    cost     - total path cost found (lower is better; UCS and A* are optimal)
    hops     - number of edges in the path
    time     - median of several runs, in milliseconds (varies by machine)
"""
from __future__ import annotations

import argparse
import statistics
import time
from pathlib import Path

from searchlib import astar, bfs, dfs, iddfs, manhattan, ucs
from searchlib.datasets import north_west as nw
from searchlib.datasets.grid import solvable_grid

RUNS = 7


def timed(fn):
    """Run ``fn`` several times; return (last result, median milliseconds)."""
    samples = []
    result = None
    for _ in range(RUNS):
        t0 = time.perf_counter()
        result = fn()
        samples.append((time.perf_counter() - t0) * 1000)
    return result, statistics.median(samples)


def table(rows):
    header = "| Algorithm | Path cost | Hops | Nodes expanded | Time (ms) |"
    rule = "|---|---:|---:|---:|---:|"
    lines = [header, rule]
    for name, result, ms in rows:
        lines.append(
            f"| {name} | {result.cost:g} | {result.hops} | {result.expanded} | {ms:.3f} |"
        )
    return "\n".join(lines)


def north_west_section() -> str:
    g, s, t = nw.GRAPH, nw.START, nw.GOAL
    h = nw.HEURISTIC_TO_COLIGNY.__getitem__
    runs = [
        ("BFS", lambda: bfs(g, s, t)),
        ("DFS", lambda: dfs(g, s, t)),
        ("IDDFS", lambda: iddfs(g, s, t)),
        ("UCS", lambda: ucs(g, s, t)),
        ("A*", lambda: astar(g, s, t, h)),
    ]
    rows = [(name, *timed(fn)) for name, fn in runs]
    best = next(r for n, r, _ in rows if n == "UCS")
    return (
        f"### North West roads: {s} to {t} ({len(g)} towns)\n\n"
        + table(rows)
        + f"\n\nOptimal cost is {best.cost:g} via {' -> '.join(best.path)}."
    )


def grid_section(size: int, wall_probability: float, seed: int) -> str:
    g, s, t = solvable_grid(size, size, wall_probability, seed)
    h = manhattan(t)
    # IDDFS is left out on purpose: with only per-branch cycle checking it
    # re-walks an astronomical number of routes in an open grid.
    runs = [
        ("BFS", lambda: bfs(g, s, t)),
        ("DFS", lambda: dfs(g, s, t)),
        ("UCS", lambda: ucs(g, s, t)),
        ("A* (Manhattan)", lambda: astar(g, s, t, h)),
    ]
    rows = [(name, *timed(fn)) for name, fn in runs]
    return (
        f"### {size}x{size} grid, {int(wall_probability * 100)}% walls, seed {seed} "
        f"({len(g)} open cells)\n\n" + table(rows)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="save the tables to benchmarks/results.md")
    args = parser.parse_args()

    sections = [
        "# Benchmark results\n",
        north_west_section(),
        grid_section(30, 0.25, seed=1),
        grid_section(60, 0.25, seed=1),
        grid_section(100, 0.25, seed=1),
        "IDDFS is only run on the road graph: on grids its repeated deepening "
        "explodes (measure it with `python -m benchmarks.iddfs_scaling`).\n",
    ]
    output = "\n\n".join(sections)
    print(output)
    if args.write:
        Path(__file__).with_name("results.md").write_text(output + "\n", encoding="utf-8")
        print("\nSaved to benchmarks/results.md")


if __name__ == "__main__":
    main()
