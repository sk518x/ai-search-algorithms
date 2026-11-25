from searchlib import (
    build_graph, inadmissible_nodes, is_admissible, is_consistent, manhattan, true_costs_to, zero,
)
from searchlib.datasets import north_west as nw
from searchlib.datasets import samples


def test_true_costs_to_goal_on_north_west():
    costs = true_costs_to(nw.GRAPH, "Coligny")
    assert costs["Coligny"] == 0
    assert costs["Lichtenburg"] == 30
    assert costs["Disaneng"] == 110


def test_true_costs_follow_edge_direction():
    g = build_graph([("A", "B", 2)], directed=True)
    costs = true_costs_to(g, "B")
    assert costs == {"B": 0, "A": 2}
    # Edges only point A -> B, so B cannot reach A at all.
    assert true_costs_to(g, "A") == {"A": 0}


def test_north_west_heuristic_is_admissible():
    assert is_admissible(nw.GRAPH, nw.GOAL, nw.HEURISTIC_TO_COLIGNY.__getitem__)


def test_north_west_heuristic_is_consistent():
    assert is_consistent(nw.GRAPH, nw.GOAL, nw.HEURISTIC_TO_COLIGNY.__getitem__)


def test_zero_heuristic_is_admissible_and_consistent():
    assert is_admissible(nw.GRAPH, nw.GOAL, zero)
    assert is_consistent(nw.GRAPH, nw.GOAL, zero)


def test_overestimate_is_detected_and_reported():
    h = {"S": 0, "A": 1, "B": 100, "G": 0}.__getitem__
    bad = inadmissible_nodes(samples.WEIGHTED, "G", h)
    assert bad == [("B", 100, 2)]
    assert not is_admissible(samples.WEIGHTED, "G", h)


def test_nonzero_heuristic_at_goal_is_inconsistent():
    assert not is_consistent(nw.GRAPH, nw.GOAL, lambda n: 1)


def test_manhattan_is_admissible_on_open_grid():
    edges = [((x, y), (x + 1, y)) for x in range(4) for y in range(5)]
    edges += [((x, y), (x, y + 1)) for x in range(5) for y in range(4)]
    grid = build_graph(edges)
    assert is_admissible(grid, (4, 4), manhattan((4, 4)))
    assert is_consistent(grid, (4, 4), manhattan((4, 4)))


def test_subtle_overestimate_is_detected():
    """A heuristic only 20% too high must still be flagged, not just a wild one."""
    true = true_costs_to(nw.GRAPH, nw.GOAL)
    h = lambda n: 1.2 * true[n]
    flagged = {node for node, _, _ in inadmissible_nodes(nw.GRAPH, nw.GOAL, h)}
    assert flagged == {n for n in nw.GRAPH if true[n] > 0}   # every node except the goal


def test_scaled_down_true_cost_is_admissible_and_consistent():
    true = true_costs_to(nw.GRAPH, nw.GOAL)
    h = lambda n: 0.8 * true[n]
    assert is_admissible(nw.GRAPH, nw.GOAL, h)
    assert is_consistent(nw.GRAPH, nw.GOAL, h)
