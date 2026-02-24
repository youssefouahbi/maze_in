from typing import List, Tuple, Optional, Any
from mazegen import Maze, PrimGenerator, DFSGenerator, BFS


class MazeGenerator:
    """
    A reusable maze generator module[cite: 219].
    """
    def __init__(self, width: int, height: int, seed: Optional[int] = None):
        # Initialize basic parameters [cite: 223]
        self.width = width
        self.height = height
        self.seed = seed
        self.maze: Optional[Maze] = None
        self.solution: List[Tuple[int, int]] = []

    def generate(self, entry: Tuple[int, int], exit: Tuple[int, int], 
                 perfect: bool = True, algo: str = "PRIM") -> None:
        """
        The core logic to build the maze.
        """
        # 1. Initialize your Maze object
        self.maze = Maze(self.width, self.height, entry, exit, perfect)   
        # 2. Setup your algorithm (Prim or DFS) using self.seed
        # ... logic for choosing algorithm goes here ...

        if algo == "PRIM":
            prim = PrimGenerator(self.maze)
            prim.set_seed(self.seed)
            prim.generate(0, 0, perfect)
        elif algo == "DFS":
            dfs = DFSGenerator(self.maze)
            dfs.apply_mask()
            self.maze.display()
            self.maze.highlight_42_cells()
            dfs.generate(0, 0, perfect)

    def get_structure(self) -> Any:
        """
        Returns the generated maze structure.
        """
        # Return the grid or the maze object
        return self.maze

    def get_solution_path(self) -> List[Tuple[int, int]]:
        """
        Calculates and returns the path from entry to exit.
        """
        # check if the maze really exists
        if not self.maze:
            return
        # Use your BFS solver here and return the list of coordinates
        bfs = BFS(self.maze)
        start = (self.maze.entry[1], self.maze.entry[0])
        end = (self.maze.exit[1], self.maze.exit[0])
        path = bfs.find_path(start, end)
        self.maze.set_path(path)
        return path
