from models.cell import Cell
import curses
import random
import time

class Maze():
    def __init__(self, width, height, entry, exit, perfect):
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.path = None
        self.show_path = True
        self.grid = [[Cell(row, col) for col in range(width)]
                     for row in range(height)]

        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        curses.start_color()
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_BLUE, 0)
        curses.init_pair(2, curses.COLOR_GREEN, 0)
        curses.init_pair(6, curses.COLOR_YELLOW, 0)
        curses.init_pair(7, curses.COLOR_RED, 0)

    def __del__(self):
        self.close()

    def close(self):
        self.stdscr.keypad(False)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def reset_maze(self):
        for row in self.grid:
            for cell in row:
                cell.visited = False
                cell.north = True
                cell.south = True
                cell.east = True
                cell.west = True

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
        if north:
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
        for row in self.grid:
            for cell in row:
                cell.visited = False

    def display(self):
        self.stdscr.clear()

        h = self.height
        w = self.width

        needed_h = 2*h + 18
        needed_w = 4*w + 27

        max_h, max_w = self.stdscr.getmaxyx()

        if needed_h > max_h or needed_w > max_w:
            self.stdscr.addstr(0, 0, "Fenêtre trop petite pour afficher le labyrinthe !")
            self.stdscr.addstr(1, 0, f"Taille requise: {needed_h}x{needed_w}")
            self.stdscr.addstr(2, 0, f"Taille écran:  {max_h}x{max_w}")
            self.stdscr.refresh()
            self.stdscr.getch()
            return

        # Mur du haut
        color_index = random.randint(6, 7)
        top = "██" * (w * 2 + 1)
        self.stdscr.addstr(0, 0, top, curses.color_pair(color_index))
        
        for r in range(h):
            line_mid = "██"   # mur gauche
            line_bot = "██"   # coin gauche bas

            for c in range(w):
                cell = self.grid[r][c]

                # Intérieur cellule
                line_mid += "  "

                # Mur est
                if cell.east:
                    line_mid += "██"
                else:
                    line_mid += "  "

                # Mur sud
                if cell.south:
                    line_bot += "██"
                else:
                    line_bot += "  "

                # Coin
                line_bot += "██"
            
            self.stdscr.addstr(r * 2 + 1, 0, line_mid, curses.color_pair(color_index))
            self.stdscr.addstr(r * 2 + 2, 0, line_bot, curses.color_pair(color_index))
        
        start_x, start_y = self.entry
        end_x, end_y = self.exit
        self.stdscr.addstr(start_y * 2 + 1, start_x * 4 + 2, "██", curses.color_pair(2))
        self.stdscr.addstr(end_y * 2 + 1, end_x * 4 + 2, "██", curses.color_pair(2))
        self.stdscr.addstr(end_y * 2 + 4, end_x - 6 , "1.Genarate maze", curses.COLOR_WHITE)
        self.stdscr.addstr(end_y * 2 + 5, end_x - 6 , "2.Genarate path", curses.COLOR_WHITE)
        self.stdscr.addstr(end_y * 2 + 6, end_x - 6 , "3.Break", curses.COLOR_WHITE)
        self.stdscr.addstr(end_y * 2 + 7, end_x - 6 , "4.Genarate maze and path", curses.COLOR_WHITE)
        self.stdscr.addstr(end_y * 2 + 8, end_x - 6 , "5.hide / show path", curses.COLOR_WHITE)

        self.stdscr.refresh()

    def get_char(self):
        return self.stdscr.getch()

    def show_hide_path(self):
        """
        Display the path in the maze using curses.
        """
        if self.show_path:
            self.show_path = False
            wall = "██"
        else:
            self.show_path = True
            wall = "  "

        if not self.path:
            return

        # Draw all cells in path
        for j in range(len(self.path) - 1):
            r, c = self.path[j+1]
            y = r * 2 + 1
            x = c * 4 + 2
            if j != len(self.path) - 2:
                self.stdscr.addstr(y, x, wall, curses.color_pair(4))
        # Draw passages between cells
        for i in range(len(self.path) - 1):
            r1, c1 = self.path[i]
            r2, c2 = self.path[i + 1]

            mid_y = (r1 + r2) * 2 // 2 + 1
            mid_x = (c1 + c2) * 4 // 2 + 2
            self.stdscr.addstr(mid_y, mid_x, wall, curses.color_pair(4))
            self.stdscr.refresh()
            time.sleep(0.05)
        self.stdscr.refresh()

    def set_path(self, path):
        self.path = path
