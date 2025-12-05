# 🗺️ Pathfinding Visualizer: A* vs Dijkstra vs BFS

An interactive Python-based visualization tool that compares three popular pathfinding algorithms side-by-side: **A\* (A-Star)**, **Dijkstra's Algorithm**, and **Breadth-First Search (BFS)**. Built with Pygame, this application provides a real-time visual comparison to help understand how each algorithm explores the grid and computes a path under its own strategy.

![Pathfinding Visualizer](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-Required-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- **Side-by-Side Comparison**: Run all three algorithms simultaneously on identical grids
- **Interactive Grid**: Click and drag to create start/end points and obstacles
- **Real-Time Visualization**: Watch algorithms explore the grid in real-time
- **Performance Metrics**: Compare execution time, nodes expanded, and path length
- **Resizable Window**: Dynamic UI that maintains aspect ratio
- **Visual Feedback**: Color-coded cells show explored nodes, paths, and obstacles

## 🎯 Algorithms Implemented

### A* (A-Star) Algorithm
- **Type**: Informed search algorithm
- **Heuristic**: Manhattan distance
- **Optimality**: Guaranteed to find the path with the least cost
- **Efficiency**: Generally fastest due to heuristic guidance

### Dijkstra's Algorithm
- **Type**: Uninformed search algorithm
- **Strategy**: Explores nodes based on cumulative distance
- **Optimality**: Guaranteed to find the path with the least cost
- **Efficiency**: Explores more nodes than A* but reliable

### Breadth-First Search (BFS)
- **Type**: Uninformed search algorithm
- **Strategy**: Explores level by level
- **Optimality**: Finds the shortest path, but is only optimal in cost when all edges have equal weight
- **Efficiency**: Simple but explores many nodes

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- Pygame library

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/HaloV01d/Pathfinding-Visualizer-A-vs-Dijkstra.git
   cd Pathfinding-Visualizer-A-vs-Dijkstra
   ```

2. **Install dependencies**
   ```bash
   pip install pygame
   ```

3. **Run the application**
   ```bash
   python joint_UI.py
   ```

## 🎮 How to Use

### Controls

1. **Left Click**: 
   - First click: Set start point (Orange)
   - Second click: Set end point (Turquoise)
   - Additional clicks: Draw obstacles (Color depends on current mode)

2. **Right Click**: 
   - Remove walls or reset cells

3. **Keyboard Controls**:
   - `SPACE`: Start the visualization
   - `R`: Clear the grid
   - `Q`: Select wall mode (Black)
   - `W`: Select mud mode (Brown)
   - `E`: Select water mode (Blue)

### Workflow

1. Launch the application
2. Click to place your start point
3. Click again to place your end point
4. Draw obstacles by clicking and dragging
5. Press `SPACE` to run all three algorithms
6. Observe the differences in how each algorithm explores the grid
7. Check the statistics panel for performance metrics

## 📊 Understanding the Visualization

### Color Legend

| Color | Meaning |
|-------|---------|
| 🟠 Orange | Start point |
| 🔵 Turquoise | End point |
| ⚫ Black | Wall/Obstacle |
| 🟢 Green | Explored nodes |
| 🔴 Red | Discovered nodes |
| 🟣 Purple | Final path |
| ⬜ White | Normal terrain (weight: 1) |
| 🟫 Brown | Mud terrain (weight: 3) |
| 🟦 Blue | Water terrain (weight: 5) |

### Performance Metrics

The application displays real-time statistics for each algorithm:
- **Execution Time**: How long the algorithm took to find the path
- **Nodes Expanded**: Number of nodes explored during the search
- **Path Length**: Length of the final path found
- **Cost**: Accumulated cost of nodes in path

## 📁 Project Structure

```
Pathfinding-Visualizer-A-vs-Dijkstra/
│
├── joint_UI.py        # Main application with side-by-side comparison
├── A_Star.py          # A* algorithm implementation
├── Dijkstra.py        # Dijkstra's algorithm implementation
├── BFS.py             # Breadth-First Search implementation
├── grid.py            # Grid and Box class definitions
└── README.md          # Project documentation
```

## 🧠 Algorithm Comparison

| Algorithm | Time Complexity | Space Complexity | Uses Heuristic | Best Use Case |
|-----------|-----------------------|------------------|----------------|---------------|
| **A\*** | O((V+E) log V) | O(V) | ✅ Yes | Best for finding lowest cost path efficiently with a good heuristic |
| **Dijkstra** | O((V+E) log V) | O(V) | ❌ No | Weighted graphs, guaranteed lowest cost path |
| **BFS** | O(V+E) | O(V) | ❌ No | Unweighted graphs, level-by-level exploration for shortest path |


*V = vertices, E = edges*

## 🎓 Educational Value

This visualizer is perfect for:
- Computer Science students learning pathfinding algorithms
- Understanding the trade-offs between different search strategies
- Visualizing how heuristics improve search efficiency
- Comparing algorithm performance in different scenarios

## 🛠️ Technical Details

- **Grid Size**: 25×25 cells (configurable in `grid.py`)
- **Window**: Resizable with maintained aspect ratio (2:1)
- **Rendering**: Pygame-based real-time visualization
- **Architecture**: Modular design with separate algorithm implementations

## 💡 Key Insights from Visualization

### Why A* is Faster
A* uses the Manhattan distance heuristic to guide its search towards the goal, resulting in fewer nodes explored compared to uninformed algorithms.

### When to Use Each Algorithm
- **A***: When you need the fastest minimum cost path and can define a good heuristic
- **Dijkstra**: When you need a guaranteed minimum cost path without a heuristic
- **BFS**: When all edges have equal weight and you want simplicity

### Observable Differences
- **A*** explores in a focused direction toward the goal thanks to the heuristic, expanding far fewer nodes.
- **Dijkstra** expands outward uniformly based on cumulative cost, avoiding expensive terrain.
- **BFS** expands outward level-by-level, like Dijkstra but ignoring weights, causing a shorter but higher cost final path.

## 📌 Example Scenarios
The following examples demonstrate how the visualizer behaves on weighted grids:

### Scenario A – Weighted Terrain:

![Screenshot showing the grid layout](assets/scenario1_grid.png "Scenario A layout")


### Scenario A – Results:

![Screenshot showing the results of all 3 algorithms](assets/scenario1_results.png "Scenario A results")


### Scenario B – Weighted Terrain (animated):

![GIF demonstrating visualization of algorithm execution](assets/animation.gif "Scenario B animation")

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

### Ideas for Enhancement
- Add more heuristics (Euclidean, Chebyshev)
- Implement more terrain types
- Add diagonal movement option
- Include more algorithms (Greedy Best-First, Jump Point Search)
- Export visualization as GIF/video
 
