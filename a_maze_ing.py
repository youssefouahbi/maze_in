from models.maze import Maze
from solver.dfs import DFSGenerator
from config.parse import read_config
import sys
from solver.prim import PrimGenerator
from solver.bfs import BFS
from models.save_hex_maze import genrate_hex_maze

def genereate_maze():


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

    dfs = DFSGenerator(maze)
    prim = PrimGenerator(maze)

    prim.set_seed(42)
    dfs.set_seed(42)
    dfs.apply_mask()
    prim.apply_mask()

    dfs.generate(0, 0, True)


    bfs = BFS(maze)
    start = (maze.entry[1], maze.entry[0])
    end = (maze.exit[1], maze.exit[0])
    # path = bfs.find_path(start, end)
    # bfs.display_path(list(path))

    
    file.set_map(maze.grid)
    file.save_map()

    while True:
        clicked = maze.get_char()
        if clicked == 49:
            dfs.apply_mask()
            dfs.generate(0, 0, True)
        if clicked == 50:
            path = bfs.find_path(start, end)
            bfs.display_path(list(path))
        if clicked == 51:
            break

    maze.close()


if __name__ == "__main__":
    main()
