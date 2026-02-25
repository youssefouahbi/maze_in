
import sys
import random
import curses
from mazegen import ConfigParser
from mazegen import Maze, DFSGenerator, PrimGenerator, BFS, genrate_hex_maze


def main() -> None:
    try:
        config = ConfigParser(sys.argv[1])
    except Exception as e:
        eror = f"Erreur config: {e}"
        print(eror)
        return

    maze = Maze(
        width=config.width,
        height=config.height,
        entry=config.entry,
        exit=config.exit,
        perfect=config.perfect)

    file = genrate_hex_maze()
    file.set_save_path("output_maze.txt")
    file.set_enter(maze.entry)
    file.set_exit(maze.exit)

    dfs = DFSGenerator(maze)
    prim = PrimGenerator(maze)
    prim.set_seed(config.seed)
    dfs.set_seed(config.seed)

    algo = config.algo
    inperfect = config.perfect

    bfs = BFS(maze)
    start = (maze.entry[1], maze.entry[0])
    end = (maze.exit[1], maze.exit[0])

    def generate_maze() -> None:
        maze.remove_path()
        if algo == "PRIM":
            prim.generate(0, 0, inperfect)
        elif algo == "DFS":
            dfs.apply_mask()
            dfs.generate(0, 0, inperfect)
        path = bfs.find_path(start, end)
        maze.set_path(path)
        maze.display()
        maze.highlight_42_cells()
        file.set_map(maze.grid)
        file.set_maze_path(path)
        file.save_map()

    def generate_path() -> None:
        maze.show_path()

    def change_color(color: int) -> None:
        maze.set_color_index(color)
    generate_maze()
    generate_path()

    while True:
        clicked = maze.get_char()
        if clicked == curses.KEY_RESIZE:
            maze.display()
            continue
        if clicked == 49:     # 1
            generate_maze()
        if clicked == 50:    # 2
            maze.show_hide_path()
        if clicked == 51:   # 3
            change_color(int(random.randint(12, 15)))
            maze.display()
        if clicked == 52:    # 4
            break
    maze.close()


if __name__ == "__main__":
    main()
