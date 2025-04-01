from window import Window
from line import Line
from point import Point 
from cell import Cell
from constants import (
    CELL_SIZE, WINDOW_SIZE_X, WINDOW_SIZE_Y,
    WINDOW_TITLE, NORMAL_WIN_X, NORMAL_WIN_Y
)
from maze import Maze
import time
import sys

def increase_recursion():
    #Get the current recursion limit
    current_limit = sys.getrecursionlimit()
    print(f"Current recursion limit: {current_limit}")
    # Set a new recursion limit - only for extra large mazes
    new_limit = 10000  # Example: Increase to 2000
    sys.setrecursionlimit(new_limit)  

def main():
    for i in range(0,4):
        print("********************************************************")
    #Make the window / by the cell size
    new_win = Window()
    
    #increase_recursion()

    new_maze = Maze(new_win, NORMAL_WIN_X//CELL_SIZE, NORMAL_WIN_Y//CELL_SIZE)
    new_maze.create_winning_path()
    #maze_start = new_maze.maze[0][0]
    #maze_end = new_maze.maze[0][1]
    #maze_start.draw_move(maze_end, False)


    new_win.wait_for_close()

if __name__ == "__main__":
    main()      