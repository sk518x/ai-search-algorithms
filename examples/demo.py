"""Run every algorithm on the North West road graph and print what each one does.

    python -m examples.demo
"""
from searchlib import astar, bfs, dfs, iddfs, ucs
from searchlib.datasets import north_west as nw


def show(name, result):
    route = " -> ".join(result.path) if result.found else "no path"
    print(f"{name:<6} cost={result.cost:<5g} expanded={result.expanded:<3} {route}")


def main() -> None:
    g, start, goal = nw.GRAPH, nw.START, nw.GOAL
    print(f"Route from {start} to {goal}\n")
    show("BFS", bfs(g, start, goal))
    show("DFS", dfs(g, start, goal))
    show("IDDFS", iddfs(g, start, goal))
    show("UCS", ucs(g, start, goal))
    result = astar(g, start, goal, nw.HEURISTIC_TO_COLIGNY.__getitem__)
    show("A*", result)
    print("\nOrder A* examined the towns:", ", ".join(result.order))


if __name__ == "__main__":
    main()
