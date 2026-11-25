"""Randomised checks: compare every algorithm against a slow, obviously-correct reference."""
import random

import pytest

from searchlib import astar, bfs, build_graph, dfs, iddfs, true_costs_to, ucs, zero
from searchlib.graph import path_cost

INF = float("inf")


def random_graph(n, edge_probability, directed, seed):
    rng = random.Random(seed)
    edges = [
        (u, v, rng.randint(1, 9))
        for u in range(n) for v in range(n)
        if u != v and rng.random() < edge_probability and (directed or u < v)
    ]
    graph = build_graph(edges, directed=directed)
    for node in range(n):
        graph.setdefault(node, {})
    return graph


def bellman_ford(graph, start):
    """Reference shortest distances: simple, slow, and hard to get wrong."""
    dist = {node: INF for node in graph}
    dist[start] = 0
    for _ in range(len(graph) - 1):
        for u, neighbours in graph.items():
            for v, cost in neighbours.items():
                if dist[u] + cost < dist[v]:
                    dist[v] = dist[u] + cost
    return dist


def unit_weights(graph):
    return {u: {v: 1 for v in nbrs} for u, nbrs in graph.items()}


CASES = [(seed, directed) for seed in range(40) for directed in (False, True)]


@pytest.mark.parametrize("seed,directed", CASES)
def test_ucs_and_astar_match_bellman_ford(seed, directed):
    graph = random_graph(12, 0.25, directed, seed)
    start, goal = 0, 11
    expected = bellman_ford(graph, start)[goal]

    assert ucs(graph, start, goal).cost == expected
    assert astar(graph, start, goal, zero).cost == expected

    # An admissible, consistent heuristic: 80% of the true remaining cost.
    true = true_costs_to(graph, goal)
    h = lambda n: 0.8 * true.get(n, 0)
    assert astar(graph, start, goal, h).cost == pytest.approx(expected)


@pytest.mark.parametrize("seed,directed", CASES)
def test_bfs_is_shortest_in_hops(seed, directed):
    graph = random_graph(12, 0.25, directed, seed)
    expected_hops = bellman_ford(unit_weights(graph), 0)[11]
    result = bfs(graph, 0, 11)
    if expected_hops == INF:
        assert not result.found
    else:
        assert result.hops == expected_hops


@pytest.mark.parametrize("seed,directed", CASES)
def test_dfs_finds_a_valid_path_exactly_when_one_exists(seed, directed):
    graph = random_graph(12, 0.25, directed, seed)
    reachable = bellman_ford(graph, 0)[11] != INF
    result = dfs(graph, 0, 11)
    assert result.found == reachable
    if reachable:
        assert result.path[0] == 0 and result.path[-1] == 11
        assert result.cost == path_cost(graph, result.path)


@pytest.mark.parametrize("seed,directed", [(s, d) for s in range(20) for d in (False, True)])
def test_iddfs_matches_bfs_hops_on_small_graphs(seed, directed):
    graph = random_graph(8, 0.25, directed, seed)
    b, i = bfs(graph, 0, 7), iddfs(graph, 0, 7)
    assert b.found == i.found
    if b.found:
        assert i.hops == b.hops
