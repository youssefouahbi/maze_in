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

    # def display_path(self, hide):
    #     """
    #     Display the path in the maze using curses.
    #     """
    #     if not self.path:
    #         return

    #     color = 4
    #     if hide:
    #         color = 5

    #     # Draw all cells in path
    #     for j in range(len(self.path) - 1):
    #         r, c = self.path[j+1]
    #         y = r * 2 + 1
    #         x = c * 4 + 2
    #         if j != len(self.path) - 2:
    #             self.maze.stdscr.addstr(y, x, "██", curses.color_pair(color))
    #     # Draw passages between cells
    #     for i in range(len(self.path) - 1):
    #         r1, c1 = self.path[i]
    #         r2, c2 = self.path[i + 1]

    #         mid_y = (r1 + r2) * 2 // 2 + 1
    #         mid_x = (c1 + c2) * 4 // 2 + 2
    #         self.maze.stdscr.addstr(mid_y, mid_x, "██", curses.color_pair(color))
    #         self.maze.stdscr.refresh()
    #         time.sleep(0.05)
    #     self.maze.stdscr.refresh()

    # def hide_path(self):
    #     if not self.path:
    #         return

    #     curses.start_color()
    #     curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLACK)

    #     # Draw all cells in path
    #     for j in range(len(self.path) - 1):
    #         r, c = self.path[j+1]
    #         y = r * 2 + 1
    #         x = c * 4 + 2
    #         if j != len(self.path) - 2:
    #             self.maze.stdscr.addstr(y, x, "██", curses.color_pair(4))
    #     # Draw passages between cells
    #     for i in range(len(self.path) - 1):
    #         r1, c1 = self.path[i]
    #         r2, c2 = self.path[i + 1]

    #         mid_y = (r1 + r2) * 2 // 2 + 1
    #         mid_x = (c1 + c2) * 4 // 2 + 2
    #         self.maze.stdscr.addstr(mid_y, mid_x, "██", curses.color_pair(4))
    #         self.maze.stdscr.refresh()
    #         time.sleep(0.05)
    #     self.maze.stdscr.refresh()

    # def show_path(self):
        if not self.path:
            return
 
        curses.start_color()
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)

        # Draw all cells in path
        for j in range(len(self.path) - 1):
            r, c = self.path[j+1]
            y = r * 2 + 1
            x = c * 4 + 2
            if j != len(self.path) - 2:
                self.maze.stdscr.addstr(y, x, "██", curses.color_pair(4))
        # Draw passages between cells
        for i in range(len(self.path) - 1):
            r1, c1 = self.path[i]
            r2, c2 = self.path[i + 1]

            mid_y = (r1 + r2) * 2 // 2 + 1
            mid_x = (c1 + c2) * 4 // 2 + 2
            self.maze.stdscr.addstr(mid_y, mid_x, "██", curses.color_pair(4))
            self.maze.stdscr.refresh()
            time.sleep(0.05)
        self.maze.stdscr.refresh()