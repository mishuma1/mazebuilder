from maze import Maze
from cell import Cell
from point import Point
from constants import CELL_SIZE



class Traverse:
    def __init__(self, maze: Maze):
        self.maze = maze
        #self.start_y = maze.start_yx[0]
        #self.start_x = maze.start_yx[1]
        print(f"{maze.start_yx[0]},{maze.start_yx[1]}")
        self.end_cell = f"{self.maze.max_rows -1},{self.maze.max_columns-1}"
        self.time_to_travel(maze.start_yx[0], maze.start_yx[1])

    def time_to_travel(self, y, x):
        #Get cell at this position - draw line from middle top 
        starting_cell = None
        this_cell : Cell = self.maze.maze[y][x]
        if x == 0 and y == 0:
            if not this_cell.north_wall:
                starting_cell = Cell(self.maze.win, Point(0, -1*CELL_SIZE), Point(0, CELL_SIZE)) 
        if y == self.maze.max_rows-1:
            #Check on south being missing
            if not this_cell.south_wall:
                starting_cell = Cell(self.maze.win, Point(0, ((y+1)*CELL_SIZE)), Point(0, (y+2)*CELL_SIZE + CELL_SIZE))
        else:
            if not this_cell.west_wall:
                starting_cell = Cell(self.maze.win, Point((-1*CELL_SIZE), ((y-1)*CELL_SIZE)), Point(0, ((y+1)*CELL_SIZE)))         

        print(f"({-1*CELL_SIZE},{(y-1)*CELL_SIZE}), (0, {(y+1)*CELL_SIZE})")
        #offscreen_cell = Cell(self.maze.win, starting_point, starting_point)
        starting_cell.draw_move(this_cell)

        return
        #tried = [f"{y},{x}"]
        #find_end = self.check_path_for_failure(y, x, [f"{y},{x}"])
 
    
    def check_path_for_failure(self, y,x, tried):
        if self.end_cell in tried:
            return tried
        
        if y+1 < self.maze.max_rows:
            if f"{y+1},{x}" not in tried:
                tried.append(f"{y+1},{x}")
                tried = self.check_path_for_failure(y+1, x, tried)
                if self.end_cell in tried:
                    return tried
        if y-1>= 0:
            if f"{y-1},{x}" not in tried:
                tried.append(f"{y-1},{x}")
                tried = self.check_path_for_failure(y-1, x, tried)
                if self.end_cell in tried:
                    return tried                

        if x+1 < self.maze.max_columns:
            if f"{y},{x+1}" not in tried:
                tried.append(f"{y},{x+1}")
                tried = self.check_path_for_failure(y, x+1, tried)
                if self.end_cell in tried:
                    return tried                

        if x-1>= 0:
            if f"{y},{x-1}" not in tried:
                tried.append(f"{y},{x-1}")
                tried = self.check_path_for_failure(y, x-1, tried)
                if self.end_cell in tried:
                    return tried                
      
        return tried