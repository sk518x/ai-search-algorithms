"""Test the tests: break the code on purpose and confirm the test suite notices.

A passing test suite only means something if it fails when the code is wrong.
Each "mutation" below makes one small, realistic bug in a temporary copy of the
project and runs pytest on it. Every mutation should be CAUGHT.

    python -m tools.mutation_check

Run this by hand, not in CI. Each mutation matches an exact line of source, so after
refactoring the code you will need to update MUTATIONS (a stale one prints SKIPPED).
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MUTATIONS = [
    ("A* never re-expands closed nodes", "searchlib/informed.py",
     "        if g > best_g[node]:  # stale entry: a cheaper route was found since it was pushed\n            continue\n",
     "        if node in order:\n            continue\n"),
    ("BFS uses a stack instead of a queue", "searchlib/uninformed.py",
     "node = frontier.popleft()", "node = frontier.pop()"),
    ("DFS explores neighbours in the other order", "searchlib/uninformed.py",
     "for neighbour in reversed(list(graph[node])):", "for neighbour in list(graph[node]):"),
    ("UCS ignores edge costs", "searchlib/uninformed.py",
     "new_g = g + cost\n            if new_g < best.get", "new_g = g + 1\n            if new_g < best.get"),
    ("A* heuristic overestimates (x2)", "searchlib/informed.py",
     "frontier, (new_g + heuristic(neighbour),", "frontier, (new_g + 2 * heuristic(neighbour),"),
    ("IDDFS gives up after one pass", "searchlib/uninformed.py",
     "        if not cutoff:  # the whole reachable graph fit inside this limit: no goal\n            break",
     "        break"),
    ("Path is returned backwards", "searchlib/graph.py",
     "    path.reverse()\n    return path", "    return path"),
    ("build_graph keeps the costlier duplicate edge", "searchlib/graph.py",
     "graph[u][v] = min(cost, graph[u].get(v, cost))", "graph[u][v] = max(cost, graph[u].get(v, cost))"),
    ("Admissibility check is twice too lenient", "searchlib/heuristics.py",
     "if node in true_cost and h(node) > true_cost[node] + EPSILON",
     "if node in true_cost and h(node) > 2 * true_cost[node] + EPSILON"),
]


def main() -> int:
    caught = 0
    for name, relative_path, old, new in MUTATIONS:
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "project"
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(
                "__pycache__", ".pytest_cache", ".git", "*.pyc"))
            target = copy / relative_path
            text = target.read_text(encoding="utf-8")
            if old not in text:
                print(f"SKIPPED  - {name} (source changed; update this mutation)")
                continue
            target.write_text(text.replace(old, new, 1), encoding="utf-8")
            run = subprocess.run(
                [sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider"],
                cwd=copy, capture_output=True, text=True,
            )
        killed = run.returncode != 0
        caught += killed
        print(("CAUGHT   - " if killed else "SURVIVED - ") + name)
    print(f"\n{caught}/{len(MUTATIONS)} mutations caught")
    return 0 if caught == len(MUTATIONS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
