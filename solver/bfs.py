# from collections import deque

# class  BFS: 
#     def __init__(self, maze):
#         self.maze = maze
#         self.path: list[tuple] = []

#     def find_path(self, start, end):
#         queue = deque()     #met les cellule a explorer
#         visited = set()    #garder les cellule deja visiter
#         parent = {} # pour reconstruire le trajet

#         queue.append(start)
#         visited.add(start)

#         while queue:
#             """
#              tanque quene n'est vide on continur le bfs
#              -popleft trie le 1er element
#             """
#             cur = queue.popleft()
#             r, c = cur
#             if cur == end:
#                 self.path = []
#                 while cur != start:  # on remonte depuis end vers start selon le parent
#                     self.path.append(cur)
#                     cur = parent[cur]
#                 self.path.append(start)
#                 self.path.reverse()
#                 return self.path

#             cell = self.maze.get_cell(r, c)
#             neighbors = self.get_accessible_neighbors(cell)
#             for n_cell in neighbors:
#                 n_pos = (n_cell.row, n_cell.col)
#                 if n_pos not in visited:
#                     visited.add(n_pos)
#                     parent[n_pos] = cur    # on note que les n_pos a un parent cur
#                     queue.append(n_pos)    # on ajout n_pos pour continue le bfs
#         return None

#     def get_accessible_neighbors(self, cell):
#         neighbors = []
#         r, c = cell.row, cell.col
#         if not cell.north:
#             n = self.maze.get_cell(r-1, c)
#             if n:
#                 neighbors.append(n)
#         if not cell.south:
#             n = self.maze.get_cell(r+1, c)
#             if n:
#                 neighbors.append(n)
#         if not cell.east:
#             n = self.maze.get_cell(r, c+1)
#             if n:
#                 neighbors.append(n)
#         if not cell.west:
#             n = self.maze.get_cell(r, c-1)
#             if n:
#                 neighbors.append(n)
#         return neighbors

from collections import deque
import curses


class BFS:
    def __init__(self, maze):
        self.maze = maze
        self.path: list[tuple] = []

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

    def display_path(self):
        """
        Display the path in the maze using curses.
        """
        if not self.path:
            return

        curses.start_color()
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_YELLOW)

        # Draw all cells in self.path
        for r, c in self.path:
            y = r * 2 + 1
            x = c * 4 + 2
            self.maze.stdscr.addstr(y, x, "██", curses.color_pair(4))

        # Draw passages between cells
        for i in range(len(self.path) - 1):
            r1, c1 = self.path[i]
            r2, c2 = self.path[i + 1]

            mid_y = (r1 + r2) * 2 // 2 + 1
            mid_x = (c1 + c2) * 4 // 2 + 2
            self.maze.stdscr.addstr(mid_y, mid_x, "██", curses.color_pair(4))

        self.maze.stdscr.refresh()
