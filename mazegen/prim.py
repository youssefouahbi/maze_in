
import random
import time
from mazegen.maze import Maze
from mazegen.cell import Cell
from typing import List, Tuple, Optional


class PrimGenerator():
    def __init__(self, maze: Maze) -> None:
        self.maze: Maze = maze
        self.apply_mask()

    def generate(
            self,
            start_row: int = 0,
            start_col: int = 0,
            inperfect: bool = False) -> None:
        self.maze.reset_maze()

        start: Optional[Cell] = self.maze.get_cell(start_row, start_col)
        if start:
            if start.visited:
                return
        self.prim(start, inperfect)

    def prim(
            self,
            start: Optional[Cell],
            inperfect: Optional[bool] = None) -> None:
        frontier: list[Cell] = []
        if start:
            start.visited = True
        neighbors: List[Tuple[Cell, str]] = \
            self.maze.get_neighbors(start, visited_only=True)
        for (cell, _) in neighbors:
            frontier.append(cell)

        while frontier:
            cell = random.choice(frontier)

            frontier.remove(cell)

            cell_neighbors: List[Tuple[Cell, str]] = \
                self.maze.get_neighbors(cell, visited_only=False)

            visited_cell_only: List[Tuple[Cell, str]] = []

            for (neighbor, direction) in cell_neighbors:
                if neighbor.visited is True and neighbor.is_42 is False:
                    visited_cell_only.append((neighbor, direction))

            if visited_cell_only:
                random.shuffle(visited_cell_only)
                new_cell = visited_cell_only[0]
                neighbor, direction = new_cell
                self.__remove_wall(cell, neighbor, direction)
                self.maze.display()
                time.sleep(.01)

            if (not inperfect and random.random() < .7
                    and len(visited_cell_only) >= 3):
                neighbor, direction = visited_cell_only[1]
                self.__remove_wall(cell, neighbor, direction)
            self.__remove_wall(cell, neighbor, direction)
            cell.visited = True

            for (n, _) in cell_neighbors:
                if (n.visited is False and n not in frontier and
                        n.is_42 is False):
                    frontier.append(n)

    def __remove_wall(
            self,
            current: Cell,
            next_cell: Cell,
            direction: str) -> None:
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

    def apply_mask(self) -> None:
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
        offset_r: int = int((self.maze.height - mh) / 2)
        offset_c: int = int((self.maze.width - mw) / 2)

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

    def set_seed(self, seed: Optional[int]) -> None:
        if seed:
            random.seed(seed)
