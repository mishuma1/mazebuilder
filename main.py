import sys
from window import Window
from constants import (
    CELL_SIZE, NORMAL_WIN_X, NORMAL_WIN_Y
)
from maze import Maze
from traverse import Traverse


def increase_recursion():
    #Get the current recursion limit
    current_limit = sys.getrecursionlimit()
    print(f"Current recursion limit: {current_limit}")
    # Set a new recursion limit - only for extra large mazes
    new_limit = 10000  # Example: Increase to 2000
    sys.setrecursionlimit(new_limit)  

def main():
    #-- if wanting a large maze
    increase_recursion() 

    new_win = Window()
    new_maze = Maze(new_win, NORMAL_WIN_X//CELL_SIZE, NORMAL_WIN_Y//CELL_SIZE)
    new_maze.create_winning_path()
    new_maze.complete_maze()
    Traverse(new_maze)
    new_win.wait_for_close()

if __name__ == "__main__":
    main()      