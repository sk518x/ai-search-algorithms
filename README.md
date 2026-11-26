# AI Search Algorithms

A Python implementation of five graph-search algorithms: Breadth-First Search (BFS), Depth-First Search (DFS), Iterative Deepening DFS (IDDFS), Uniform-Cost Search (UCS), and A\*.

Built from scratch using Python's standard library, the project includes automated tests, heuristic validation, and performance benchmarks comparing the algorithms on a real road network and randomly generated grid mazes.

The project originated from two university coursework projects (uninformed search and A\* truck routing between North West towns). It was subsequently rebuilt as a unified, tested package with reusable algorithms, consistent search results, and reproducible benchmarks.

## Technologies Used

- **Python** - Algorithm implementations and graph processing.
- **pytest** - Unit, randomised, and algorithm validation tests.
- **GitHub Actions** - Automated testing and continuous integration.
- **Matplotlib** - Optional search-route visualisation.

## Quick Start

Clone the repository and install the development dependencies:

```bash
git clone https://github.com/sk518x/ai-search-algorithms.git
cd ai-search-algorithms

pip install -r requirements-dev.txt
```

Run the examples, tests, and benchmarks:

```bash
python -m examples.demo
python -m pytest
python -m benchmarks.run_benchmarks
```

To generate the route visualisation:

```bash
pip install -r requirements-viz.txt
python -m examples.visualize
```

## Usage Example

The algorithms can be imported and used independently:

```python
from searchlib import astar, bfs
from searchlib.datasets import north_west as nw

result = astar(
    nw.GRAPH,
    "Disaneng",
    "Coligny",
    nw.HEURISTIC_TO_COLIGNY.__getitem__
)

print(result.path)
print(result.cost)
print(result.expanded)
```

Example output:

```text
['Disaneng', 'Mahikeng', 'Bakerville',
 'Lichtenburg', 'Coligny']

Cost: 110
Expanded: 9
```

Each algorithm returns a consistent `SearchResult` containing the discovered path, total cost, number of expanded nodes, and search order.

## Algorithm Comparison

| Algorithm | Optimal? | Optimises         | Data Structure |
| --------- | -------- | ----------------- | -------------- |
| BFS       | Yes      | Fewest hops       | Queue          |
| DFS       | No       | No guarantee      | Stack          |
| IDDFS     | Yes      | Fewest hops       | Recursion      |
| UCS       | Yes      | Lowest total cost | Priority queue |
| A\*       | Yes\*    | Lowest total cost | Priority queue |

- **BFS:** Explores the graph level by level.
- **DFS:** Explores one branch deeply before backtracking.
- **IDDFS:** Repeatedly performs depth-limited DFS, combining BFS's optimality for unweighted graphs with DFS's low memory usage.
- **UCS:** Expands the lowest-cost path first, equivalent to Dijkstra's algorithm.
- _**A**_**\*:** Combines actual path cost with a heuristic estimate to guide the search towards the goal.

\*A\*\* is optimal when its heuristic is admissible (never overestimates the remaining cost). The `searchlib.heuristics` module includes admissibility and consistency checkers.

## Benchmark Results

All algorithms return the same result structure, allowing their performance to be compared consistently.

Node expansions provide a useful measure of search effort independent of machine hardware, while execution time provides an additional measure of practical performance.

### North West Road Network

Disaneng to Coligny across a network of 13 towns.

| Algorithm | Path Cost | Hops | Nodes Expanded |
| --------- | --------: | ---: | -------------: |
| BFS       |       110 |    4 |             13 |
| DFS       |       125 |    6 |              9 |
| IDDFS     |       110 |    4 |             57 |
| UCS       |       110 |    4 |             13 |
| A\*       |       110 |    4 |              9 |

### Random Grid Maze

100 × 100 grid with 25% randomly generated walls and 7,436 open cells.

| Algorithm       | Path Cost | Nodes Expanded |
| --------------- | --------: | -------------: |
| BFS             |       198 |          7,369 |
| DFS             |     1,424 |          6,651 |
| UCS             |       198 |          7,369 |
| A\* (Manhattan) |       198 |          2,268 |

Full benchmark results, including 30 × 30 and 60 × 60 grids and execution times, are available in [`benchmarks/results.md`](benchmarks/results.md).

### What the Results Show

- **DFS does not guarantee optimal paths.** Although it expanded fewer nodes than BFS on the road network, its route cost was 125 compared with the optimal cost of 110.
- _A can reduce search effort significantly._\* On the 100 × 100 grid, it expanded approximately 69% fewer nodes than UCS while finding a path with the same optimal cost.
- **IDDFS trades additional computation for lower memory usage.** It repeatedly explores shallow nodes, which can become expensive on larger search spaces.
- **Fewer expansions do not always mean faster execution.** Heap operations and heuristic calculations introduce overhead, meaning A\* can sometimes take longer than BFS on smaller grids.

### IDDFS Scaling

IDDFS can become particularly expensive as search depth increases.

| Grid    | BFS Expanded | IDDFS Expanded | IDDFS Time |
| ------- | -----------: | -------------: | ---------: |
| 6 × 6   |           28 |          1,538 |     0.00 s |
| 10 × 10 |           67 |         56,406 |     0.05 s |
| 12 × 12 |          106 |      3,057,531 |     1.81 s |
| 15 × 15 |          163 | Did not finish |     > 10 s |

These results demonstrate the computational cost of repeatedly exploring nodes during iterative deepening.

Reproduce the experiment using:

```bash
python -m benchmarks.iddfs_scaling
```

## Testing and Validation

The project includes 42 test functions, covering 333 test cases when the randomised tests are expanded.

The test suite includes:

- **Unit tests:** Correct paths, start-equals-goal cases, unreachable goals, unknown nodes, cycles, and algorithm-specific behaviour.
- **Randomised tests:** Generated directed and undirected graphs compare UCS and A\* against a Bellman-Ford reference, BFS against a unit-weight reference, DFS for path validity, and IDDFS against BFS.
- **Heuristic validation:** Tests for admissibility and consistency, including deliberately overestimating heuristics.
- _A re-expansion:_\* Verifies that A\* can revisit nodes when necessary to preserve optimality with an admissible but inconsistent heuristic.

### Mutation Testing

To evaluate whether the tests detect actual implementation errors, the project includes a mutation-testing tool:

```bash
python -m tools.mutation_check
```

It introduces nine realistic code mutations, including replacing BFS's queue with a stack, ignoring edge costs in UCS, and returning paths in reverse order.

**Current result: 9 out of 9 mutations detected.**

The test suite runs automatically through GitHub Actions on Python 3.10–3.12. Mutation testing is performed manually because the checks depend on specific source-code locations and may require updates after refactoring.

## Project Structure

```text
searchlib/
    graph.py        Graph representation and path helpers
    result.py       SearchResult data structure
    uninformed.py   BFS, DFS, IDDFS and UCS
    informed.py     A* search
    heuristics.py   Heuristics and validation checkers
    datasets/       Road networks and grid mazes

tests/              Unit, heuristic and randomised tests
benchmarks/         Performance comparisons and IDDFS scaling
examples/           Demonstrations and route visualisation
tools/              Mutation-testing utility
```

## Design Decisions

- **Weighted graph representation:** Graphs use `{node: {neighbour: cost}}`, keeping edge weights alongside their connections and avoiding a separate weight lookup structure.
- **Efficient visited tracking:** Dictionaries and sets provide efficient membership checks instead of repeatedly searching through lists.
- **Consistent result structure:** All algorithms return the same `SearchResult` type, simplifying testing and benchmarking.
- _A re-expansion:_\* Nodes can be revisited when a cheaper route is discovered, preserving optimality with admissible but inconsistent heuristics.
- **Priority queue management:** Outdated heap entries are skipped rather than removed, since Python's `heapq` does not provide a decrease-key operation.

## Limitations

- Edge costs must be non-negative.
- IDDFS is recursive and only prevents cycles along its current search branch, making it more suitable for smaller graphs and trees.
- The road-network heuristic uses manually assigned estimates rather than geographical coordinates.
- Grid benchmarks use randomly generated walls with a fixed seed, so results may differ from real-world maps.

## Future Improvements

Potential extensions include:

- Bidirectional search.
- Iterative Deepening A\* (IDA\*).
- Heuristics derived from real geographical coordinates using OpenStreetMap data.
- Step-by-step visualisation of frontier expansion and path discovery.
