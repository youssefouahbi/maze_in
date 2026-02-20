from models.cell import Cell


class genrate_hex_maze:

    def __init__(self):
        self.grid: list[list[Cell]] | None = None
        self.path: str = "example.txt"

    def save_map(self):
        if not self.grid:
            return

        with open(self.path, "w") as file:
            file.write(str(self.grid))

    def set_map(self, grid: list[list[Cell]]) -> None:
        self.grid = grid

    def set_save_path(self, path: str) -> None:
        self.path = path
