from collections import deque
import curses
import time

class BFS:
    def __init__(self, maze):
        self.maze = maze
        self.path: list[tuple] = []

        curses.init_pair(4, curses.COLOR_BLUE, 0)
        curses.init_pair(5, curses.COLOR_BLACK, 0)

    def find_path(self, start, end):
        """
        BFS to find shortest path from start to end.
        start, end = (row, col)
        """
        queue = deque([start])
        visited = set([start])
        parent = {}

        while queue:
            cur = queue.popleft()
            r, c = cur

            # Reached exit
            if cur == end:
                self.path = []
                while cur != start:
                    self.path.append(cur)
                    cur = parent[cur]
                self.path.append(start)
                self.path.reverse()
                return self.path

            # Get current cell
            cell = self.maze.get_cell(r, c)
            if not cell:
                continue

            # Explore neighbors
            for n_cell in self.get_accessible_neighbors(cell):
                n_pos = (n_cell.row, n_cell.col)
                if n_pos not in visited:
                    visited.add(n_pos)
                    parent[n_pos] = cur
                    queue.append(n_pos)

        # No path found
        self.path = []
        return []

    def get_accessible_neighbors(self, cell):
        """
        Returns all neighbor cells that can be moved to (no wall in between).
        """
        neighbors = []
        r, c = cell.row, cell.col

        if not cell.north:
            n = self.maze.get_cell(r - 1, c)
            if n:
                neighbors.append(n)
        if not cell.south:
            n = self.maze.get_cell(r + 1, c)
            if n:
                neighbors.append(n)
        if not cell.east:
            n = self.maze.get_cell(r, c + 1)
            if n:
                neighbors.append(n)
        if not cell.west:
            n = self.maze.get_cell(r, c - 1)
            if n:
                neighbors.append(n)

        return neighbors
