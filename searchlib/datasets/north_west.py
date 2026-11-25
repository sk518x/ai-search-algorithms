"""North West road network from the original A* coursework project.

Edge costs are travel costs between neighbouring towns. ``HEURISTIC_TO_COLIGNY``
holds the hand-assigned "traffic level" estimates of the remaining cost to
Coligny; ``tests/test_heuristics.py`` checks that they never overestimate.
"""
from searchlib.graph import build_graph

EDGES = [
    ("Disaneng", "Mahikeng", 25),
    ("Disaneng", "Madibogo", 35),
    ("Mahikeng", "Mmabatho", 10),
    ("Mahikeng", "Slurry", 20),
    ("Mahikeng", "Bakerville", 35),
    ("Mahikeng", "Madibogo", 30),
    ("Mmabatho", "Slurry", 15),
    ("Slurry", "Zeerust", 35),
    ("Slurry", "Groot Marico", 40),
    ("Slurry", "Bakerville", 25),
    ("Zeerust", "Groot Marico", 20),
    ("Bakerville", "Lichtenburg", 20),
    ("Lichtenburg", "Coligny", 30),
    ("Coligny", "Ottosdal", 35),
    ("Ottosdal", "Sannieshof", 25),
    ("Sannieshof", "Delareyville", 30),
    ("Madibogo", "Sannieshof", 35),
]

GRAPH = build_graph(EDGES)
START = "Disaneng"
GOAL = "Coligny"

HEURISTIC_TO_COLIGNY = {
    "Disaneng": 70,
    "Mahikeng": 50,
    "Mmabatho": 55,
    "Slurry": 45,
    "Zeerust": 65,
    "Groot Marico": 75,
    "Bakerville": 30,
    "Lichtenburg": 20,
    "Coligny": 0,
    "Ottosdal": 25,
    "Sannieshof": 40,
    "Delareyville": 55,
    "Madibogo": 60,
}
