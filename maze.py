import random
import time
from cell import Cell
from constants import CELL_SIZE,NORMAL_WIN_X, NORMAL_WIN_Y,DRAW_SPEED
from point import Point
from maze_helpers import set_walls,remove_path

opposite = {
    "north" : "south",
    "south" : "north",
    "east" : "west",
    "west" : "east"
}

class Maze:
    def __init__(self, win, max_x, max_y):
        self.win = win
        self.max_columns = max_x
        self.max_rows = max_y
        self.start_yx = [0,0]
        self.maze = self.fill_structure()
        self.end_postition = [NORMAL_WIN_X, NORMAL_WIN_Y]
        self.end_point = f"{self.max_rows -1},{self.max_columns-1}"

    def fill_structure(self):
        cell_rows = []
        for row in range(0, self.max_rows):
            nw = False
            sw = False
            ww = False
            ew = False
            if row == 0:
                nw = True
            if row == self.max_rows -1:
                sw = True
            start_point_y = row * CELL_SIZE
            cell_columns = []
            for across in range(0, self.max_columns):
                if across == 0:
                    ww = True
                if row == self.max_columns -1:
                    ew = True                
                start_point_x = across * CELL_SIZE
                new_cell = Cell(self.win, Point(start_point_x,start_point_y), Point(start_point_x+ CELL_SIZE,start_point_y + CELL_SIZE),nw,sw,ew,ww)
                cell_columns.append(new_cell)
            cell_rows.append(cell_columns)
        return cell_rows
 
    def safe_choice(self, cur_maze, path, current_paths, y, x):
        if len(current_paths) > 0:
            if path in current_paths:
                find_end = self.check_path_for_failure(cur_maze,y, x, [f"{y},{x}"])
                if self.end_point not in find_end:
                    current_paths.remove(path)
        return current_paths        

    def start_position_rand(self):
        base_y = random.randrange(0,2)
        start_cell = None
        if base_y == 0:
            #Top Corner
            start_cell = Cell(self.win, Point(0,0), Point(0,0))
            start_cell.outbound = "south"
        else:
            #west wall somewhere
            y_rand=random.randrange(0,self.max_rows)
            start_cell = Cell(self.win, Point(0,y_rand), Point(0,y_rand))
            if y_rand == self.max_rows -1:
                start_cell.outbound = "north"
            else:   
                start_cell.outbound = "east"   
      
        return start_cell

    def create_winning_path(self):
        prev_cell = self.start_position_rand()
        self.start_yx = [prev_cell.y1,0]
        x=0
        y=prev_cell.y1
        paths_to_take = ["north", "south", "east", "west"]

        while x != self.max_columns-1  or y != self.max_rows-1 or len(paths_to_take) == 0:
            this_cell = self.maze[y][x]
            this_cell.solution = True 
            this_cell.touched = True  

            this_cell.north_wall = True
            this_cell.south_wall = True
            this_cell.west_wall = True
            this_cell.east_wall = True

            paths_to_take = ["north", "south", "east", "west"]
            opp_side = opposite[prev_cell.outbound]
            setattr(this_cell, f"{opp_side}_wall", False)                
            paths_to_take.remove(opp_side)

            north_cell = None 
            south_cell = None
            east_cell = None 
            west_cell = None

            if x == 0:
                if prev_cell and prev_cell.outbound != "south":
                    this_cell.north_wall = True   
                paths_to_take = remove_path(paths_to_take, ["west"])
            elif x == self.max_columns-1:
                if prev_cell and prev_cell.outbound != "south":
                    this_cell.north_wall = True  
                paths_to_take = remove_path(paths_to_take, ["east", "north"])                    

            if y == 0:
                if prev_cell and prev_cell.outbound != "east":
                    this_cell.west_wall = True              
                paths_to_take = remove_path(paths_to_take, ["west", "north"])                                                           
            elif y == self.max_rows-1:
                if prev_cell and prev_cell.outbound != "east":
                    this_cell.west_wall = True
                paths_to_take = remove_path(paths_to_take, ["west", "south"])          

            tmp_maze = self.maze.copy()
            paths_to_take = self.safe_choice(tmp_maze, "west", paths_to_take, y, x-1)
            paths_to_take = self.safe_choice(tmp_maze, "north", paths_to_take, y-1,x)
            paths_to_take = self.safe_choice(tmp_maze, "east", paths_to_take, y,x+1)
            paths_to_take = self.safe_choice(tmp_maze, "south", paths_to_take, y+1,x)

            while (len(paths_to_take) > 1):
                    path_out = random.randrange(0,len(paths_to_take))
                    wall_to_use = paths_to_take[path_out]
                    setattr(this_cell, f"{wall_to_use}_wall", True)
                    paths_to_take.remove(wall_to_use)

            if len(paths_to_take) > 0:
                this_cell.outbound = paths_to_take[0]
                setattr(this_cell, f"{this_cell.outbound}_wall", False)                

                prev_cell = this_cell 
                match paths_to_take[0]:
                    case "north":
                        y -= 1
                    case "south":
                        y += 1
                    case "east":
                        x += 1
                    case "west":
                        x -= 1

            this_cell.draw()
            self.win.redraw()

        if x == self.max_columns-1  and y == self.max_rows-1:
            this_cell = self.maze[y][x]
            this_cell = set_walls(this_cell, True, False, True, True, True, True)
            setattr(this_cell, f"{opposite[prev_cell.outbound]}_wall", False)

            this_cell.draw()  
            self.win.redraw()
            
    def check_path_for_failure(self, maze, y,x, tried):
        if f"{self.max_rows -1},{self.max_columns-1}" in tried:
            return tried
        if maze[y][x].touched:
            return tried
        if y+1 < self.max_rows:
            if not maze[y+1][x].touched and f"{y+1},{x}" not in tried:
                tried.append(f"{y+1},{x}")
                tried = self.check_path_for_failure(maze, y+1, x, tried)
                if f"{self.max_rows -1},{self.max_columns-1}" in tried:
                    return tried
        if y-1>= 0:
            if not maze[y-1][x].touched and f"{y-1},{x}" not in tried:
                tried.append(f"{y-1},{x}")
                tried = self.check_path_for_failure(maze, y-1, x, tried)
                if f"{self.max_rows -1},{self.max_columns-1}" in tried:
                    return tried                

        if x+1 < self.max_columns:
            if not maze[y][x+1].touched and f"{y},{x+1}" not in tried:
                tried.append(f"{y},{x+1}")
                tried = self.check_path_for_failure(maze, y, x+1, tried)
                if f"{self.max_rows -1},{self.max_columns-1}" in tried:
                    return tried                

        if x-1>= 0:
            if not maze[y][x-1].touched and f"{y},{x-1}" not in tried:
                tried.append(f"{y},{x-1}")
                tried = self.check_path_for_failure(maze, y, x-1, tried)
                if f"{self.max_rows -1},{self.max_columns-1}" in tried:
                    return tried                
      
        return tried
 
    def complete_maze(self):
        for row in range(0, self.max_rows):
            for across in range(0, self.max_columns):
                if not self.maze[row][across].touched:    
                    self.create_fillers(row,across)  

    def get_adj_cell(self, condition, path_cell, wall, y, x):
        if condition:
            tmp_maze = self.maze[y][x]
            if tmp_maze.touched:           
                wall_status = getattr(tmp_maze, f"{wall}_wall")
                setattr(tmp_maze, f"outbound", wall )
                if wall_status:
                    path_cell.append([wall, tmp_maze])     
        return path_cell
     
    def create_connection(self, y, x):
        prev_cell = Cell(self.win, Point(0,0), Point(0,0))
        path_to_open = []
        path_to_open = self.get_adj_cell(y>0, path_to_open, "south", y-1, x)
        path_to_open = self.get_adj_cell(y >= 0 and y < self.max_rows-1, path_to_open, "north", y+1, x)
        path_to_open = self.get_adj_cell(x>0, path_to_open, "east", y, x-1)
        path_to_open = self.get_adj_cell(x >= 0 and x < self.max_columns-1, path_to_open, "west", y, x+1)

        if len(path_to_open) > 0:
            path_out = random.randrange(0,len(path_to_open))
            wall_to_use = path_to_open[path_out][0]
            prev_cell = path_to_open[path_out][1]
            setattr(prev_cell, f"{wall_to_use}_wall", False)
            prev_cell.draw()
            connected = True

        self.win.redraw()   
        return prev_cell     

    def create_fillers(self, y, x):
        connected = False
        #Will call at the end again -- maybe not
        prev_cell = self.create_connection(y, x)
        if prev_cell.outbound is not None:
            connected = True

        while True:
            paths_to_take = ["north", "south", "east", "west"]
            this_cell = self.maze[y][x]
            set_walls(this_cell, True, True, True, True, True)

            if x == 0:
                this_cell.west_wall = True   
                paths_to_take = remove_path(paths_to_take, ["west"])
            elif x == self.max_columns-1:
                this_cell.east_wall = True  
                paths_to_take = remove_path(paths_to_take, ["east"])                 
            if y == 0:
                this_cell.north_wall = True              
                paths_to_take = remove_path(paths_to_take, ["north"]) 
            elif y == self.max_rows-1:
                this_cell.south_wall = True
                paths_to_take = remove_path(paths_to_take, ["south"])    

            if prev_cell.outbound:
                setattr(this_cell, f"{opposite[prev_cell.outbound]}_wall", False)                
                paths_to_take = remove_path(paths_to_take, [opposite[prev_cell.outbound]])

            if y>0 and self.maze[y-1][x].touched:
                paths_to_take = remove_path(paths_to_take, ["north"])               
            if y < self.max_rows-1 and self.maze[y+1][x].touched:
                paths_to_take = remove_path(paths_to_take, ["south"])   
            if x>0 and self.maze[y][x-1].touched:
                paths_to_take = remove_path(paths_to_take, ["west"])   
            if x<self.max_columns - 1 and self.maze[y][x+1].touched:
                paths_to_take = remove_path(paths_to_take, ["east"])   

            if len(paths_to_take) == 0:
                this_cell.draw()  
                self.win.redraw()                
                break

            path_out = random.randrange(0,len(paths_to_take))
            this_cell.outbound = paths_to_take[path_out]
            setattr(this_cell, f"{this_cell.outbound}_wall", False)

            prev_cell = this_cell
            match this_cell.outbound:
                case "north":
                    y -= 1
                case "south":
                    y += 1
                case "west":
                    x -= 1
                case "east":
                    x += 1

            #Last line of the while
            this_cell.draw()  
            self.win.redraw()
            time.sleep(DRAW_SPEED)

