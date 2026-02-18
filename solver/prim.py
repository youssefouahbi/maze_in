
import random
import time


class PrimGenerator():
    def __init__(self, maze):
        self.maze = maze

    def generate(self, start_row=0, start_col=0):
        self.maze.reset_maze()
        start = self.maze.get_cell(start_row, start_col)
        if start.visited:
            return
        self.prim(start)

    def prim(self, start, inperfect=False):
        # list for adding invisited the neighbers each time
        frontier = []

        # make the start as visisted
        start.visited = True

        # getting the naieghbers for the first cell
        neighbors = self.maze.get_neighbors(start, visited_only=True)

        # append them to the list
        for (cell, _) in neighbors:
            frontier.append(cell)

        # loop over the list white not empty
        while frontier:
            # choose a random cell from the list
            cell = random.choice(frontier)

            # remove that cell fromthe list frontier
            frontier.remove(cell)

            # get the neighbers of that cell the visited and invisited ones
            cell_neighbors = self.maze.get_neighbors(cell, visited_only=False)

            # list for getting the visisted cells only and add them
            visited_cell_only = []

            for (neighbor, direction) in cell_neighbors:
                if neighbor.visited is True and neighbor.is_42 is False:
                    visited_cell_only.append((neighbor, direction))

            # if there is visited neigbers we got a randm one and try to
            # correct it with the current cell
            if visited_cell_only:
                random.shuffle(visited_cell_only)
                new_cell = visited_cell_only[0]
                neighbor, direction = new_cell
                self.__remove_wall(cell, neighbor, direction)
                self.maze.display()
                time.sleep(.05)

            # to make it inperfect by opening new cell instead of one
            if (inperfect and random.random() < .7 and len(visited_cell_only) >= 3):
                neighbor, direction = visited_cell_only[1]
                self.__remove_wall(cell, neighbor, direction)

            # mark corrent cell as visisted
            cell.visited = True

            # try to add the invisidted naibers to the list frontier
            for (n, _) in cell_neighbors:
                if n.visited is False and n not in frontier and n.is_42 is False:
                    frontier.append(n)

    def __remove_wall(self, current, next_cell, direction):
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

    def apply_mask(self):
        """
        mask = matrice de 0/1
        1 => cellule bloquée (déjà visitée)
        """
        MASK_42 = [
            [0, 0, 0,0,0,0,0,0,0,0,0,0],
            [0, 0, 1,0,0,0,1,1,1,0,0,0],
            [0, 0, 1,0,0,0,0,0,1,0,0,0],
            [0, 0, 1,1,1,0,1,1,1,0,0,0],
            [0, 0, 0,0,1,0,1,0,0,0,0,0],
            [0, 0, 0,0,1,0,1,1,1,0,0,0],
            [0, 0, 0,0,0,0,0,0,0,0,0,0],]

        mh = len(MASK_42)
        mw = len(MASK_42[0])

        # On centre la matrice dans le maze
        offset_r = int((self.maze.height - mh) / 2)
        offset_c = int((self.maze.width - mw) / 2)

        for r in range(mh):
            for c in range(mw):
                if MASK_42[r][c] == 1:
                    mr = r + offset_r
                    mc = c + offset_c
                    if 0 <= mr < self.maze.height and 0 <= mc < self.maze.width:
                        cell = self.maze.grid[mr][mc]
                        cell.visited = True
                        cell.is_42 = True
                        # keep all walls intact so display will block it
                        # cell.north = True
                        # cell.south = True
                        # cell.east = True
                        # cell.west = True
