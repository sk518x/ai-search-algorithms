import pytest

from searchlib import bfs, dfs, iddfs, ucs
from searchlib.datasets import samples
from searchlib.graph import path_cost

ALGORITHMS = [bfs, dfs, iddfs, ucs]
IDS = [f.__name__ for f in ALGORITHMS]


def assert_valid_path(graph, result, start, goal):
    """A returned path must start/end correctly, follow real edges, and report its true cost."""
    assert result.found
    assert result.path[0] == start and result.path[-1] == goal
    assert result.cost == path_cost(graph, result.path)  # raises if an edge is missing


@pytest.mark.parametrize("algo", ALGORITHMS, ids=IDS)
def test_finds_path_in_tree(algo):
    result = algo(samples.TREE, "A", "G")
    assert result.path == ["A", "B", "E", "G"]
    assert_valid_path(samples.TREE, result, "A", "G")


@pytest.mark.parametrize("algo", ALGORITHMS, ids=IDS)
def test_start_equals_goal(algo):
    result = algo(samples.TREE, "A", "A")
    assert result.path == ["A"]
    assert result.cost == 0
    assert result.hops == 0


@pytest.mark.parametrize("algo", ALGORITHMS, ids=IDS)
def test_unreachable_goal_returns_not_found(algo):
    result = algo(samples.DISCONNECTED, "A", "E")
    assert not result.found
    assert result.path is None
    assert result.cost == float("inf")


@pytest.mark.parametrize("algo", ALGORITHMS, ids=IDS)
def test_unknown_node_raises(algo):
    with pytest.raises(ValueError):
        algo(samples.TREE, "A", "Z")
    with pytest.raises(ValueError):
        algo(samples.TREE, "Z", "A")


@pytest.mark.parametrize("algo", ALGORITHMS, ids=IDS)
def test_terminates_on_cycles(algo):
    result = algo(samples.CYCLE, "A", "D")
    assert_valid_path(samples.CYCLE, result, "A", "D")


def test_bfs_finds_fewest_hops_but_dfs_may_not():
    g = samples.SHORTCUT
    assert bfs(g, "S", "G").path == ["S", "G"]
    assert dfs(g, "S", "G").path == ["S", "A", "B", "G"]  # valid, but longer


def test_iddfs_matches_bfs_hops():
    g = samples.SHORTCUT
    assert iddfs(g, "S", "G").hops == bfs(g, "S", "G").hops == 1


def test_iddfs_respects_max_depth():
    # G is 3 hops from S via the only route in a straight chain.
    from searchlib import build_graph
    chain = build_graph([("S", "A"), ("A", "B"), ("B", "G")], directed=True)
    assert iddfs(chain, "S", "G", max_depth=2).found is False
    assert iddfs(chain, "S", "G", max_depth=3).found is True


def test_iddfs_reexpands_shallow_nodes():
    """The cost of iterative deepening: it expands more nodes than BFS."""
    g = samples.TREE
    assert iddfs(g, "A", "G").expanded > bfs(g, "A", "G").expanded


def test_ucs_minimises_cost_not_hops():
    g = samples.WEIGHTED
    result = ucs(g, "S", "G")
    assert result.path == ["S", "B", "G"]
    assert result.cost == 4


def test_traversal_order_is_recorded():
    result = bfs(samples.TREE, "A", "G")
    assert result.order == ["A", "B", "C", "D", "E", "F", "G"]
    assert result.expanded == len(result.order)
