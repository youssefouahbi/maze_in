*This project has been created as part of the 42 curriculum by youahbi, zchouikh.*

# A-Maze-ing

## Description
A-Maze-ing is a Python-based maze generation and visualization tool. The project provides a robust engine to generate random mazes (including "perfect" mazes), visualize them in the terminal or via a graphical interface, and solve them using efficient pathfinding algorithms. It focuses on algorithmic complexity, graph theory, and the creation of a reusable software module.

---

## Instructions

### Installation
Ensure you have **Python 3.10+** installed. Install project dependencies using the provided Makefile:
```bash
make install

```

### Execution

Run the program by passing a configuration file as the sole argument:

```bash
python3 a_maze_ing.py config.txt

```

Alternatively, use the Makefile rule:

```bash
make run

```

### Development & Linting

To ensure code quality and type safety according to project standards:

* **Linting:** `make lint` (Runs flake8 and mypy with mandatory flags)
* **Cleaning:** `make clean` (Removes caches and temporary files)
* **Debugging:** `make debug` (Runs with Python's built-in debugger)

---

## Configuration File Format

The configuration file must contain one `KEY=VALUE` pair per line. Lines starting with `#` are treated as comments and ignored.

| Key | Description | Example |
| --- | --- | --- |
| **WIDTH** | Maze width (number of cells) | `WIDTH=20` |
| **HEIGHT** | Maze height (number of cells) | `HEIGHT=15` |
| **ENTRY** | Entry coordinates (x,y) | `ENTRY=0,0` |
| **EXIT** | Exit coordinates (x,y) | `EXIT=19,14` |
| **PERFECT** | Boolean: is the maze perfect (one unique path)? | `PERFECT=True` |
| **ALGO** | Generation algorithm (DFS or PRIM) | `ALGO=PRIM` |
| **OUTPUT_FILE** | Filename for hex wall encoding | `OUTPUT_FILE=maze.txt` |
| **SEED** | Integer for reproducibility | `SEED=42` |

---

## Maze Algorithms

### Chosen Algorithms: Prim's and DFS Algorithms
We utilized both **Prim’s** and **DFS (Recursive Backtracker)** algorithms for maze generation.

* **Why Prim's?** which creates long, winding corridors, Prim’s creates more "sprawling" and complex-looking mazes with many short dead ends. It naturally lends itself to creating **perfect mazes** while maintaining high randomness.
* **Why DFS?** It is computationally fast, memory-efficient, and easily "carves" through a grid. 
---

## Reusable Module: `mazegen`

The core logic is encapsulated in a unique class named `MazeGenerator` within a standalone module. This package is named `mazegen-*` and is suitable for installation via pip.

### Usage Example

```python
from MazeGenerator import MazeGenerator

# 1. Instantiate with custom size and seed
gen = MazeGenerator(width=20, height=20, seed=42)

# 2. Generate with specific entry/exit and algorithm
gen.generate(entry=(0,0), exit=(19,19), perfect=True, algo="PRIM")

# 3. Access Structure & Solution
structure = gen.get_structure() # Access generated structure
path = gen.get_solution_path()  # Access path solution

```

---

## Resources & AI Disclosure

### External Resources

* **Algorithms:** Prim's and DFS theory via Wikipedia and CS50.
* **Graphics:** Python standard library documentation and MiniLibX references.

### AI Usage

AI was used in this project for the following tasks:

1. **Boilerplate Generation:** Creating the initial `Makefile` and `pyproject.toml` structure.
2. **Bug Fixing:** Debugging edge cases in the hexagonal wall encoding logic.
3. **Refactoring:** Converting procedural code into the reusable `MazeGenerator` class.
4. **Documentation:** Generating Python docstrings following PEP 257 standards.

---

## Team & Project Management

### Roles

* **youahbi:** Core generation logic (Prim), Hex encoding, Packaging (`pyproject.toml`).
* **zchouikh:** Config parsing, Solving logic (BFS), Terminal/Visual display.

### Planning & Evolution

* **Anticipated:** A simple linear build from generation to solving.
* **Actual:** We refactored the entire engine mid-project to meet the "Reusable Module" requirement, moving logic out of the main script and into a packageable class.

### Evaluation

* **Success:** The separation of concerns between the module and the interface worked very well.
* **Improvements:** Earlier focus on type hints would have saved time during the linting phase.

### Tools

* **VS Code & Git**
* **Flake8 & Mypy** for quality control.
* **Pip & Setuptools** for building the reusable module.

