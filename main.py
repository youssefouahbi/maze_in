from models.maze import Maze
from solver.dfs import DFSGenerator
from config.parse import read_config
import sys
from solver.prim import PrimGenerator


def main():
    try:
        config = read_config(sys.argv[1])
    except Exception as e:
        eror = f"Erreur config: {e}"
    maze = Maze(
        config['WIDTH'],
        config['HEIGHT'],
        config['ENTRY'],
        config['EXIT'],
        config['PERFECT'])

    dfs = DFSGenerator(maze)
    prim = PrimGenerator(maze)
    dfs.set_seed(None)
    dfs.apply_mask()
    dfs.generate(0, 0, True)

    while True:
        clicked = maze.get_char()
        if clicked == 49:
            dfs.apply_mask()
            dfs.generate(0, 0)
        if clicked == 52:
            break


    maze.close()


if __name__ == "__main__":
    main()
