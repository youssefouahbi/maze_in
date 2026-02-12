import random
from models.cell import Cell
from models.maze import Maze


class MazeGenerator:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.maze = Maze(rows, cols)
