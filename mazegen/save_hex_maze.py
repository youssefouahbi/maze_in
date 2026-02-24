from mazegen.cell import Cell


class genrate_hex_maze:

    def __init__(self):
        self.grid: list[list[Cell]] | None = None
        self.path: str = "example.txt"
        self.enter: tuple[int, int] = (0, 0)
        self.exit: tuple[int, int] = (0, 0)
        self.maze_path: list[tuple[int, int]] | None = None

    def save_map(self):
        if not self.grid:
            return

        with open(self.path, "w") as file:
            for row in self.grid:
                for col in row:
                    file.write(col.get_hex_value())
                file.write("\n")
            file.write(f"\n{self.enter[0]}, {self.enter[1]}")
            file.write(f"\n{self.exit[0]}, {self.exit[1]}")

            file.write("\n")
            if self.__transfaire_path():
                file.write(self.__transfaire_path())

    def __transfaire_path(self) -> str:
        path: str = ""
        if not self.maze_path:
            return
        for i in range(len(self.maze_path) - 1):
            x1, y1 = self.maze_path[i]
            x2, y2 = self.maze_path[i + 1]

            x_move = x1 - x2
            y_move = y1 - y2

            if x_move == 1:
                path += "N"
            elif x_move == -1:
                path += "S"
            if y_move == 1:
                path += "W"
            elif y_move == -1:
                path += "E"
        return path





    def set_map(self, grid: list[list[Cell]]) -> None:
        self.grid = grid

    def set_save_path(self, path: str) -> None:
        self.path = path

    def set_maze_path(self, path: list[tuple[int, int]]) -> None:
        self.maze_path = path

    def set_enter(self, entry: tuple[int, int]):
        self.enter = entry

    def set_exit(self, exit: tuple[int, int]):
        self.exit = exit
