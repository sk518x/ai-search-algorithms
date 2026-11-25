import pytest

from searchlib.graph import build_graph, path_cost, reverse_graph


def test_undirected_edges_go_both_ways():
    g = build_graph([("A", "B", 3)])
    assert g == {"A": {"B": 3}, "B": {"A": 3}}


def test_directed_edges_go_one_way():
    g = build_graph([("A", "B", 3)], directed=True)
    assert g == {"A": {"B": 3}, "B": {}}


def test_missing_cost_defaults_to_one():
    assert build_graph([("A", "B")])["A"]["B"] == 1


def test_duplicate_edge_keeps_cheaper_cost():
    g = build_graph([("A", "B", 9), ("A", "B", 4)])
    assert g["A"]["B"] == 4 and g["B"]["A"] == 4


def test_negative_cost_rejected():
    with pytest.raises(ValueError):
        build_graph([("A", "B", -1)])


def test_malformed_edge_rejected():
    with pytest.raises(ValueError):
        build_graph([("A",)])


def test_path_cost_sums_edges():
    g = build_graph([("A", "B", 2), ("B", "C", 5)])
    assert path_cost(g, ["A", "B", "C"]) == 7
    assert path_cost(g, ["A"]) == 0


def test_path_cost_rejects_missing_edge():
    g = build_graph([("A", "B", 2), ("C", "D", 1)])
    with pytest.raises(ValueError):
        path_cost(g, ["A", "C"])


def test_reverse_graph_flips_edges():
    g = build_graph([("A", "B", 2)], directed=True)
    assert reverse_graph(g) == {"A": {}, "B": {"A": 2}}
