
import random


class PrimGenerator():
    def __init__(self, maze):
        self.maze = maze

    def generate(self, start_row=0, start_col=0):
        start = self.maze.get_cell(start_row, start_col)
        if start.visited:
            return
        self.prim(start)

    def prim(self, start):
        frontier = []
        start.visited = True
        neighbors = self.maze.get_neighbors(start, visited_only=True)
        for (cell, _) in neighbors:
            frontier.append(cell)

        while frontier:
            cell = random.choice(frontier)
            frontier.remove(cell)

            cell_neighbors = self.maze.get_neighbors(cell, visited_only=False)

            visited_cell_only = []
            for (neighbor, direction) in cell_neighbors:
                if neighbor.visited is True:
                    visited_cell_only.append((neighbor, direction))
            random.shuffle(visited_cell_only)
            if not visited_cell_only:
                continue
            else:
                new_cell = visited_cell_only[0]
            neighbor, direction = new_cell
            self.__remove_wall(cell, neighbor, direction)
            cell.visited = True
            for (neighbor, _) in cell_neighbors:
                if neighbor.visited is False and neighbor not in frontier:
                    frontier.append(neighbor)

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
