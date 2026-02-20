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

        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        curses.start_color()
        curses.curs_set(0)
        curses.init_pair(4, curses.COLOR_BLUE, 0)
        curses.init_pair(5, curses.COLOR_GREEN, 0)
        curses.init_pair(6, curses.COLOR_YELLOW, 0)

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

        needed_h = 2*h + 1
        needed_w = 4*w + 2

        max_h, max_w = self.stdscr.getmaxyx()

        if needed_h > max_h or needed_w > max_w:
            self.stdscr.addstr(0, 0, "Fenêtre trop petite pour afficher le labyrinthe !")
            self.stdscr.addstr(1, 0, f"Taille requise: {needed_h}x{needed_w}")
            self.stdscr.addstr(2, 0, f"Taille écran:  {max_h}x{max_w}")
            self.stdscr.refresh()
            self.stdscr.getch()
            return

        # Mur du haut

        top = "██" * (w * 2 + 1)
        self.stdscr.addstr(0, 0, top)

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

            self.stdscr.addstr(r * 2 + 1, 0, line_mid)
            self.stdscr.addstr(r * 2 + 2, 0, line_bot)
        
        start_x, start_y = self.entry
        end_x, end_y = self.exit
        self.stdscr.addstr(start_y * 2 + 1, start_x * 4 + 2, "██", curses.color_pair(5))
        self.stdscr.addstr(end_y * 2 + 1, end_x * 4 + 2, "██", curses.color_pair(6))

        self.stdscr.refresh()

    def get_char(self):
        return self.stdscr.getch()

    # def display_path(self, path: list[tuple]):
        # self.stdscr.clear()
        # last_x, last_y = self.exit
        # last_cell = self.grid[last_y][last_x]
        # # if last_cell.is_42 is False:
        for i in range(len(path) - 1):
            r1, c1 = path[i]
            r2, c2 = path[i + 1]

            y1 = r1 * 2 + 1
            x1 = c1 * 4 + 2

            y2 = r2 * 2 + 1
            x2 = c2 * 4 + 2

            # colorier la cellule
            self.stdscr.addstr(y1, x1, "██", curses.color_pair(4))

            # colorier le passage entre les cellules
            mid_y = (y1 + y2) // 2
            mid_x = (x1 + x2) // 2
            self.stdscr.addstr(mid_y, mid_x, "██", curses.color_pair(4))
        # self.stdscr.refresh()