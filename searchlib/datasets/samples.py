"""Small graphs used to demonstrate and test specific behaviours."""
from searchlib.graph import build_graph

# The directed tree from the original BFS/DFS/IDDFS project.
TREE = build_graph(
    [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"), ("C", "F"), ("E", "G")],
    directed=True,
)

# DFS dives down the long branch first (S -> A -> B -> G, 3 hops),
# while BFS finds the direct edge (S -> G, 1 hop).
SHORTCUT = build_graph([("S", "A"), ("A", "B"), ("B", "G"), ("S", "G")], directed=True)

# A graph with a cycle, to prove nothing loops forever.
CYCLE = build_graph([("A", "B"), ("B", "C"), ("C", "A"), ("C", "D")])

# Two separate components: D is unreachable from A.
DISCONNECTED = build_graph([("A", "B"), ("B", "C"), ("D", "E")])

# The cheapest route (S-B-G, cost 4) is not the one with fewest hops
# versus S-A-G (cost 6); both have 2 hops. Used to show that weights matter.
WEIGHTED = build_graph([("S", "A", 1), ("A", "G", 5), ("S", "B", 2), ("B", "G", 2)], directed=True)
