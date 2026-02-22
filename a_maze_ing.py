from models.maze import Maze
from solver.dfs import DFSGenerator
from config.parse import read_config
import sys
from solver.prim import PrimGenerator
from solver.bfs import BFS
from models.save_hex_maze import genrate_hex_maze
import random

# import pudb
# pudb.set_trace()


def main():
    try:
        config = read_config(sys.argv[1])
    except Exception as e:
        eror = f"Erreur config: {e}"
        print(eror)
        return

    maze = Maze(
        config['WIDTH'],
        config['HEIGHT'],
        config['ENTRY'],
        config['EXIT'],
        config['PERFECT'])

    file = genrate_hex_maze()
    file.set_save_path("output_maze.txt")
    # file.set_enter(config["ENTRY"])
    # file.set_exit(config["EXIT"])

    dfs = DFSGenerator(maze)
    prim = PrimGenerator(maze)
    prim.set_seed(42)
    dfs.set_seed(42)

    algo = config['ALGO']
    inperfect = config['PERFECT']

    bfs = BFS(maze)
    start = (maze.entry[1], maze.entry[0])
    end = (maze.exit[1], maze.exit[0])

    def generate_maze():
        if algo == "PRIM":
            prim.generate(0, 0, inperfect)
        elif algo == "DFS":
            dfs.generate(0, 0, inperfect)
        path = bfs.find_path(start, end)
        maze.set_path(path)
        file.set_map(maze.grid)
        file.set_maze_path(path)
        file.save_map()

    def generate_path():
        maze.show_hide_path()

    def change_color(color):
        maze.set_color_index(color)

    generate_maze()
    generate_path()
    while True:
        clicked = maze.get_char()
        if clicked == 49:     # 1
            # change_color(int(random.randint(5, 10)))
            generate_maze()
            maze.set_show_path_flag()
            generate_path()
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
