from models.maze import Maze
from solver.dfs import DFSGenerator
from config.parse import read_config
import sys
from solver.prim import PrimGenerator
from solver.bfs import BFS
from models.save_hex_maze import genrate_hex_maze


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

    algo = "prim"
    inperfect = True

    bfs = BFS(maze)
    start = (maze.entry[1], maze.entry[0])
    end = (maze.exit[1], maze.exit[0])

    def generate_maze():
        if algo == "prim":
            prim.generate(0, 0, inperfect)
        elif algo == "dfs":
            dfs.generate(0, 0, inperfect)
        path = bfs.find_path(start, end)
        file.set_map(maze.grid)
        file.set_maze_path(path)
        file.save_map()

    def generate_path():
        bfs.display_path()

    generate_maze()
    generate_path()

    while True:
        clicked = maze.get_char()
        if clicked == 49:
            generate_maze()
        if clicked == 50:
            generate_path()
        if clicked == 51:
            break

    maze.close()


if __name__ == "__main__":
    main()
