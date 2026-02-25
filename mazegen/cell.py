class Cell ():
    def __init__(
            self,
            row: int,
            col: int,
            north: bool = True,
            south: bool = True,
            east: bool = True,
            west: bool = True) -> None:
        self.row = row
        self.col = col
        self.north = north
        self.south = south
        self.east = east
        self.west = west
        self.visited = False
        self.is_42 = False
        self.hex: str = "0123456789ABCDEF"

    def remove_wall(self, wall: str) -> None:
        if (wall == "north"):
            self.north = False
        elif (wall == "south"):
            self.south = False
        elif (wall == "east"):
            self.east = False
        elif (wall == "west"):
            self.west = False

    def mark_visited(self) -> None:
        self.visited = True

    def get_hex_value(self) -> str:
        num = 0
        if self.west:
            num += 8
        if self.north:
            num += 1
        if self.east:
            num += 2
        if self.south:
            num += 4
        return self.hex[num]
