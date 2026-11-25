# Benchmark results


### North West roads: Disaneng to Coligny (13 towns)

| Algorithm | Path cost | Hops | Nodes expanded | Time (ms) |
|---|---:|---:|---:|---:|
| BFS | 110 | 4 | 13 | 0.012 |
| DFS | 125 | 6 | 9 | 0.009 |
| IDDFS | 110 | 4 | 57 | 0.026 |
| UCS | 110 | 4 | 13 | 0.020 |
| A* | 110 | 4 | 9 | 0.013 |

Optimal cost is 110 via Disaneng -> Mahikeng -> Bakerville -> Lichtenburg -> Coligny.

### 30x30 grid, 25% walls, seed 1 (690 open cells)

| Algorithm | Path cost | Hops | Nodes expanded | Time (ms) |
|---|---:|---:|---:|---:|
| BFS | 60 | 60 | 687 | 0.322 |
| DFS | 136 | 136 | 650 | 0.509 |
| UCS | 60 | 60 | 687 | 0.700 |
| A* (Manhattan) | 60 | 60 | 327 | 0.420 |

### 60x60 grid, 25% walls, seed 1 (2692 open cells)

| Algorithm | Path cost | Hops | Nodes expanded | Time (ms) |
|---|---:|---:|---:|---:|
| BFS | 118 | 118 | 2686 | 1.450 |
| DFS | 516 | 516 | 733 | 0.663 |
| UCS | 118 | 118 | 2686 | 2.864 |
| A* (Manhattan) | 118 | 118 | 1419 | 1.889 |

### 100x100 grid, 25% walls, seed 1 (7436 open cells)

| Algorithm | Path cost | Hops | Nodes expanded | Time (ms) |
|---|---:|---:|---:|---:|
| BFS | 198 | 198 | 7369 | 4.158 |
| DFS | 1424 | 1424 | 6651 | 5.813 |
| UCS | 198 | 198 | 7369 | 8.787 |
| A* (Manhattan) | 198 | 198 | 2268 | 3.025 |

IDDFS is only run on the road graph: on grids its repeated deepening explodes (measure it with `python -m benchmarks.iddfs_scaling`).

