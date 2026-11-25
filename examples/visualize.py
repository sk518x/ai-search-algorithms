"""Draw the road graph with each algorithm's route highlighted.

Needs the optional plotting packages:  pip install -r requirements-viz.txt

    python -m examples.visualize          # writes docs/images/north_west_routes.png
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # draw to a file; no window needed
import matplotlib.pyplot as plt
import networkx as nx

from searchlib import astar, bfs, dfs, ucs
from searchlib.datasets import north_west as nw

OUTPUT = Path(__file__).resolve().parent.parent / "docs" / "images" / "north_west_routes.png"


def main() -> None:
    g = nx.Graph()
    for u, neighbours in nw.GRAPH.items():
        for v, cost in neighbours.items():
            g.add_edge(u, v, weight=cost)
    layout = nx.spring_layout(g, seed=7, k=1.2)
    edge_labels = nx.get_edge_attributes(g, "weight")

    runs = [
        ("BFS (fewest hops)", bfs(nw.GRAPH, nw.START, nw.GOAL)),
        ("DFS (any path)", dfs(nw.GRAPH, nw.START, nw.GOAL)),
        ("UCS (cheapest)", ucs(nw.GRAPH, nw.START, nw.GOAL)),
        ("A* (cheapest, fewer nodes)", astar(nw.GRAPH, nw.START, nw.GOAL, nw.HEURISTIC_TO_COLIGNY.__getitem__)),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(13, 10))
    for ax, (title, result) in zip(axes.flat, runs):
        path_edges = list(zip(result.path, result.path[1:]))
        node_colors = [
            "#2e6b5e" if n in (nw.START, nw.GOAL)
            else "#e8a33d" if n in result.path
            else "#c9ced9" if n in result.order
            else "#eef0f4"
            for n in g.nodes
        ]
        nx.draw_networkx_edges(g, layout, ax=ax, edge_color="#b8bcc7", width=1.2)
        nx.draw_networkx_edges(g, layout, edgelist=path_edges, ax=ax, edge_color="#d9541e", width=3.5)
        nx.draw_networkx_nodes(g, layout, ax=ax, node_color=node_colors, node_size=900, edgecolors="#444")
        nx.draw_networkx_labels(g, layout, ax=ax, font_size=7)
        nx.draw_networkx_edge_labels(g, layout, edge_labels=edge_labels, ax=ax, font_size=7)
        ax.set_title(f"{title}\ncost {result.cost:g} | {result.expanded} nodes expanded", fontsize=11)
        ax.axis("off")

    fig.suptitle(f"{nw.START} to {nw.GOAL}: green = start/goal, orange = on the route, "
                 "grey = examined but not used", fontsize=11)
    fig.tight_layout()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT, dpi=130)
    print(f"Saved {OUTPUT}")


if __name__ == "__main__":
    main()
