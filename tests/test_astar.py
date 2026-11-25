from searchlib import astar, build_graph, ucs, zero
from searchlib.datasets import north_west as nw
from searchlib.datasets import samples


def h_nw(node):
    return nw.HEURISTIC_TO_COLIGNY[node]


def test_north_west_optimal_route():
    result = astar(nw.GRAPH, nw.START, nw.GOAL, h_nw)
    assert result.path == ["Disaneng", "Mahikeng", "Bakerville", "Lichtenburg", "Coligny"]
    assert result.cost == 110


def test_astar_matches_ucs_cost_on_north_west():
    assert astar(nw.GRAPH, nw.START, nw.GOAL, h_nw).cost == ucs(nw.GRAPH, nw.START, nw.GOAL).cost


def test_astar_expands_fewer_nodes_than_ucs_on_north_west():
    """Data-specific check: on this graph the heuristic genuinely helps."""
    informed = astar(nw.GRAPH, nw.START, nw.GOAL, h_nw)
    uninformed = ucs(nw.GRAPH, nw.START, nw.GOAL)
    assert informed.expanded < uninformed.expanded


def test_zero_heuristic_behaves_like_ucs():
    a = astar(nw.GRAPH, nw.START, nw.GOAL, zero)
    u = ucs(nw.GRAPH, nw.START, nw.GOAL)
    assert a.cost == u.cost
    assert a.expanded == u.expanded


def test_unreachable_goal():
    result = astar(samples.DISCONNECTED, "A", "E", zero)
    assert not result.found
    assert result.cost == float("inf")


def test_start_equals_goal():
    result = astar(nw.GRAPH, "Coligny", "Coligny", h_nw)
    assert result.path == ["Coligny"] and result.cost == 0


def test_overestimating_heuristic_can_return_a_worse_path():
    """Why admissibility matters. S-B-G costs 4 but S-A-G costs 6.

    h(B) = 100 wildly overestimates, so A* never trusts B and settles for 6.
    """
    g = samples.WEIGHTED
    bad_h = {"S": 0, "A": 1, "B": 100, "G": 0}.__getitem__
    assert astar(g, "S", "G", bad_h).cost == 6          # wrong: not optimal
    assert ucs(g, "S", "G").cost == 4                   # the true optimum


def test_admissible_but_inconsistent_heuristic_is_still_optimal():
    """A* must re-expand a node when a cheaper route to it turns up later.

    B is first reached directly (g=5) and, because h(B)=0, looks so promising it
    is expanded at once. Only later does the cheap route S-A-B (g=2) surface,
    because h(A)=11 made A look unattractive. An A* that never revisits closed
    nodes would return the cost-15 route; the optimum is S-A-B-G at cost 12.
    h is admissible (never above the true cost to G) but inconsistent on A->B.
    """
    g = build_graph(
        [("S", "A", 1), ("S", "B", 5), ("A", "B", 1), ("B", "G", 10)],
        directed=True,
    )
    h = {"S": 0, "A": 11, "B": 0, "G": 0}.__getitem__
    result = astar(g, "S", "G", h)
    assert result.path == ["S", "A", "B", "G"]
    assert result.cost == ucs(g, "S", "G").cost == 12
    assert "B" in result.order and result.order.count("B") == 2  # B really was re-expanded
