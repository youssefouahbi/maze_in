from models.maze import Maze
import curses


def main(stdscr):
    curses.curs_set(0)  # hide the cursor
    stdscr.clear()      # clear the screen


if __name__ == "__main__":
    maze = Maze(10, 10, 0, 0, True)
    maze.display()
