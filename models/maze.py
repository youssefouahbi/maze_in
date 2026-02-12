from models.cell import Cell
import curses


class Maze():
    def __init__(self, width, height, entry, exit, perfect):
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.grid = [[Cell(row, col) for col in range(width)]
                     for row in range(height)]

    def in_bounds(self, row, col):
        if row >= 0 and row < self.height and col >= 0 and col < self.width:
            return True
        else:
            return False

    def get_cell(self, row, col):
        if not self.in_bounds(row, col):
            return None
        else:
            return self.grid[row][col]

    def get_neighbors(self, cell, visited_only=False):
        neighbors = []
        r = cell.row
        c = cell.col

        # North
        north = self.get_cell(r - 1, c)
        if north is not None:
            if not visited_only or not north.visited:
                neighbors.append((north, "north"))

        # South
        south = self.get_cell(r + 1, c)
        if south is not None:
            if not visited_only or not south.visited:
                neighbors.append((south, "south"))

        # East
        east = self.get_cell(r, c + 1)
        if east is not None:
            if not visited_only or not east.visited:
                neighbors.append((east, "east"))

        # West
        west = self.get_cell(r, c - 1)
        if west is not None:
            if not visited_only or not west.visited:
                neighbors.append((west, "west"))
        return neighbors

    def reset_visited(self):
        pass

    def display(self):
        def draw_maze(stdscr):
            curses.curs_set(0)
            stdscr.clear()

            for r, row in enumerate(self.grid):
                line_top = ""
                line_mid = ""

                for c, cell in enumerate(row):
                    if (cell.north or (c > 0 and row[c-1].north)):
                        line_top += "██"
                    else:
                        "██"

                    line_top += "██" if cell.north else "  "

                    line_mid += "██" if cell.west else "  "

                    line_mid += "  "
                line_top += "██"
                line_mid += "██"
                stdscr.addstr(r * 2, 0, line_top)
                stdscr.addstr(r * 2 + 1, 0, line_mid)
            bottom_border = "██" * (len(self.grid[0]) * 2 + 1)
            stdscr.addstr(len(self.grid) * 2, 0, bottom_border)
            stdscr.refresh()
            stdscr.getch()

        curses.wrapper(draw_maze)
