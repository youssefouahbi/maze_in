import random
import time
from mazegen.maze import Maze
from mazegen.cell import Cell
from typing import List, Optional, Tuple


class DFSGenerator:
    def __init__(self, maze: Maze) -> None:
        self.maze: Maze = maze
        self.apply_mask()

    def apply_mask(self) -> None:
        self.maze.reset_maze()
        """
        mask = matrice de 0/1
        1 => cellule bloquée (déjà visitée)
        """
        MASK_42: List[List] = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        mh: int = len(MASK_42)
        mw: int = len(MASK_42[0])
        offset_r: int = (self.maze.height - mh) // 2
        offset_c: int = (self.maze.width - mw) // 2

        for r in range(mh):
            for c in range(mw):
                if MASK_42[r][c] == 1:
                    mr: int = r + offset_r
                    mc: int = c + offset_c
                    if (0 <= mr < self.maze.height
                            and 0 <= mc < self.maze.width):
                        cell = self.maze.grid[mr][mc]
                        cell.visited = True
                        cell.is_42 = True

    def generate(
            self,
            start_row: int = 0,
            start_col: int = 0,
            inperfect: Optional[bool] = None) -> None:
        start: Optional[Cell] = self.maze.get_cell(start_row, start_col)
        if start:
            if start.visited:
                return
        self._dfs(start, inperfect)

    def _dfs(self, cell: Optional[Cell], inperfect: Optional[bool]) -> None:
        if cell:
            cell.visited = True
        neighbors: List[Tuple[Cell, str]] =\
            self.maze.get_neighbors(cell, visited_only=True)
        self.maze.display()
        time.sleep(.01)
        random.shuffle(neighbors)

        if not inperfect and random.random() < .5 and neighbors:
            if len(neighbors) > 2:
                cell1, dira = neighbors[-1]
                self.__remove_wall(cell, cell1, dira)

        for (next_cell, direction) in neighbors:
            if not next_cell.visited:
                self.__remove_wall(cell, next_cell, direction)
                self._dfs(next_cell, inperfect)

    def __remove_wall(
            self,
            current: Optional[Cell],
            next_cell: Optional[Cell],
            direction: str) -> None:
        if current and next_cell:
            if direction == "north":
                current.north = False
                next_cell.south = False
            elif direction == "south":
                current.south = False
                next_cell.north = False
            elif direction == "east":
                current.east = False
                next_cell.west = False
            elif direction == "west":
                current.west = False
                next_cell.east = False

    def set_seed(self, seed: Optional[int]) -> None:
        if seed:
            random.seed(seed)
