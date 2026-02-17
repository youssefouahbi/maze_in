

class Cell ():
    def __init__(self, row, col, north=True, south=True, east=True, west=True):
        self.row = row
        self.col = col
        self.north = north
        self.south = south
        self.east = east
        self.west = west
        self.visited = False

    def has_wall(self, wall) -> bool:
        if (wall == "north"):
            return self.north
        elif (wall == "south"):
            return self.south
        elif (wall == "east"):
            return self.east
        elif (wall == "west"):
            return self.west

    def remove_wall(self, wall):
        if (wall == "north"):
            self.north = False
        elif (wall == "south"):
            self.south = False
        elif (wall == "east"):
            self.east = False
        elif (wall == "west"):
            self.west = False

    def mark_visited(self):
        self.visited = True
