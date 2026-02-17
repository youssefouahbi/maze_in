from models.maze import Maze
import curses
from solver.dfs import DFSGenerator
from config.parse import read_config
import sys


def main(stdscr):
    try:
        config = read_config(sys.argv[1])
    except Exception as e:
        stdscr.addstr(0,0, f"Erreur config: {e}")
        stdscr.refresh()
        stdscr.getch()
        return
    maze = Maze(
        config['WIDTH'],
        config['HEIGHT'],
        config['ENTRY'],
        config['EXIT'],
        config['PERFECT'])

    dfs = DFSGenerator(maze)
    dfs.set_seed(None)
    dfs.apply_mask()   # generation du 42 pattern
    dfs.generate(0, 0)   # Génération du labyrinthe
    maze.display()       # Affichage avec curses


if __name__ == "__main__":
    curses.wrapper(main)