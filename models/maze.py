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
        for row in self.grid:
            for cell in row:
                cell.visited = False

    def display(self):
        def draw_maze(stdscr):
            curses.curs_set(0)

            h = self.height
            w = self.width

            needed_h = 2*h + 1
            needed_w = 4*w + 2
     
            max_h, max_w = stdscr.getmaxyx()

            if needed_h > max_h or needed_w > max_w:
                stdscr.addstr(0, 0, "Fenêtre trop petite pour afficher le labyrinthe !")
                stdscr.addstr(1, 0, f"Taille requise: {needed_h}x{needed_w}")
                stdscr.addstr(2, 0, f"Taille écran:  {max_h}x{max_w}")
                stdscr.refresh()
                stdscr.getch()
                return
            
            # Mur du haut
                
            top = "██" * (w * 2 + 1)
            stdscr.addstr(0, 0, top)


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

                stdscr.addstr(r * 2 + 1, 0, line_mid)
                stdscr.addstr(r * 2 + 2, 0, line_bot)

            stdscr.refresh()
            stdscr.getch()
        
        curses.wrapper(draw_maze)
