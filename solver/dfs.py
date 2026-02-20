import random
import time

class DFSGenerator:
    # accéder aux cellules
    # casser les murs
    # demander les voisins
    def __init__(self, maze):
        self.maze = maze
        self.apply_mask()
    
    def apply_mask(self):
        self.maze.reset_maze()
        """
        mask = matrice de 0/1
        1 => cellule bloquée (déjà visitée)
        """
        MASK_42 = [
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,1,0,0,0,1,1,1,0,0,0],
            [0,0,1,0,0,0,0,0,1,0,0,0],
            [0,0,1,1,1,0,1,1,1,0,0,0],
            [0,0,0,0,1,0,1,0,0,0,0,0],
            [0,0,0,0,1,0,1,1,1,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0],]
        
        mh = len(MASK_42)
        mw = len(MASK_42[0])

        # On centre la matrice dans le maze
        offset_r = (self.maze.height - mh) // 2
        offset_c = (self.maze.width - mw) // 2

        for r in range(mh):
            for c in range(mw):
                if MASK_42[r][c] == 1:
                    mr = r + offset_r
                    mc = c + offset_c
                    if 0 <= mr < self.maze.height and 0 <= mc < self.maze.width:
                        cell = self.maze.grid[mr][mc]
                        cell.visited = True

    def generate(self, start_row=0, start_col=0, inperfect=None):
        
        start = self.maze.get_cell(start_row, start_col)
        if start.visited:
            return
        self._dfs(start, inperfect)

    def _dfs(self, cell, inperfect):
        cell.visited = True   # marquer comme visite
        neighbors = self.maze.get_neighbors(cell, visited_only=True) #recup les voisins non visite
        self.maze.display()
        time.sleep(.01)
        random.shuffle(neighbors)

        if inperfect and random.random() < .5 and neighbors:
            if len(neighbors) > 2:
                cell1, dira = neighbors[-1]
                self.__remove_wall(cell, cell1, dira)

        for (next_cell, direction) in neighbors:
            if not next_cell.visited:
                self.__remove_wall(cell, next_cell, direction)
                self._dfs(next_cell, inperfect)


    def __remove_wall(self, current, next_cell, direction):    # casser le mure entre 2 cellules
        if direction == "north":
            current.north = False
            next_cell.south = False     # on onleve nord du current et sud du next cellul, et le donc metre connecte
        elif direction == "south":
            current.south = False
            next_cell.north = False
        elif direction == "east":
            current.east = False
            next_cell.west = False
        elif direction == "west":
            current.west = False
            next_cell.east = False

    def set_seed(self, seed):
        if seed:
            random.seed(seed)
