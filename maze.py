from cell import Cell
from constants import CELL_SIZE,NORMAL_WIN_X, NORMAL_WIN_Y,DRAW_SPEED
from point import Point
import random
import time

class Maze:
    def __init__(self, win, max_x, max_y):
        self.win = win
        self.max_columns = max_x
        self.max_rows = max_y
        self.maze = self.fill_structure()
        #Later change to random spot from midpoint to MAX, color the start and end, maybe
        #Might need to know if left or right of current spot and above/below current spot
        self.end_postition = [NORMAL_WIN_X, NORMAL_WIN_Y]
        self.end_point = f"{self.max_rows -1},{self.max_columns-1}"


    def fill_structure(self):
        #Adding edge frame
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

    def remove_path(self, current_paths, remove_paths):
        for remove_item in remove_paths:
            if remove_item in current_paths:
                current_paths.remove(remove_item)
        return current_paths
    
    def safe_choice(self, cur_maze, path, current_paths, y, x):
        if len(current_paths) > 0:
            if path in current_paths:
                find_end = self.check_path_for_failure(cur_maze,y, x, [f"{y},{x}"])
                if self.end_point not in find_end:
                    current_paths.remove(path)
        return current_paths        

    def opposite_side(self, wall):
        if wall == "west":
            return "east"
        if wall == "east":
            return "west"
        if wall == "north":
            return "south"
        if wall == "south":
            return "north"

    def print_wall_status(self, this_cell: Cell):
        print(f"NW: {this_cell.north_wall}, SW: {this_cell.south_wall}, EW: {this_cell.east_wall}, WW: {this_cell.west_wall}")


    def create_winning_path(self):
        print(f"ROWS: {self.max_rows}, COLS: {self.max_columns}")
        x=0
        y=0
        #Fake cell to avoid if check on first call
        prev_cell = Cell(self.win, Point(0,-1), Point(0,-1),False, False,True,False)
        prev_cell.outbound = "south"
        

        while x != self.max_columns-1  or y != self.max_rows-1:
            print("A++++++++++++++++++++++++++++++++++++++++++++++++++")
            this_cell = self.maze[y][x]
            this_cell.solution = True 
            this_cell.touched = True  

            this_cell.north_wall = True
            this_cell.south_wall = True
            this_cell.west_wall = True
            this_cell.east_wall = True

            paths_to_take = ["north", "south", "east", "west"]
            #open the inbound path to this cell, and remove as an exit
            opp_side = self.opposite_side(prev_cell.outbound)
            setattr(this_cell, f"{opp_side}_wall", False)                
            paths_to_take.remove(opp_side)

            north_cell = None 
            south_cell = None
            east_cell = None 
            west_cell = None
            print(f"A Y: {y}, X: {x}, A PATHS Left: {paths_to_take}")
            self.print_wall_status(this_cell)

            if x == 0:
                if prev_cell and prev_cell.outbound != "south":
                    this_cell.north_wall = True   
                paths_to_take = self.remove_path(paths_to_take, ["west", "north"])
            elif x == self.max_columns-1:
                if prev_cell and prev_cell.outbound != "south":
                    this_cell.north_wall = True  
                paths_to_take = self.remove_path(paths_to_take, ["east", "north"])                    

            if y == 0:
                if prev_cell and prev_cell.outbound != "east":
                    this_cell.west_wall = True              
                paths_to_take = self.remove_path(paths_to_take, ["west", "north"])                                                           
            elif y == self.max_rows-1:
                if prev_cell and prev_cell.outbound != "east":
                    this_cell.west_wall = True
                paths_to_take = self.remove_path(paths_to_take, ["west", "south"])          

            print(f"B PATHS Left: {paths_to_take}")
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
            #else:
                #print("CC No paths to take")
            #print(f"CC NORTH: {this_cell.north_wall}, SOUTH: {this_cell.south_wall}, EAST:{this_cell.east_wall}, WEST: {this_cell.west_wall}") 
            print(f"END Y: {y}, X: {x}, A PATHS Left: {paths_to_take}")
            self.print_wall_status(this_cell)

            this_cell.draw()
            self.win.redraw()
            time.sleep(DRAW_SPEED)
            print("E++++++++++++++++++++++++++++++++++++++++++++++++++")

            
            #print("S================================================")
            
            #Now to figure out where to go and the allowed path to take
            #If x == max x or 0 then no north bound
            #If y == 0 or max y then no west

        print(f"FEND Y: {y}, X: {x}")
        if x == self.max_columns-1  and y == self.max_rows-1:
            print(f"Final Draw: {self.opposite_side(prev_cell.outbound)}")
            #Set all to True, then apply logic - might not need
            this_cell = self.maze[y][x]
            this_cell.north_wall = True
            this_cell.south_wall = False
            this_cell.west_wall = True
            this_cell.east_wall = True
            #OPen the 
            #self.opposite_side(prev_cell.outbound)
            setattr(this_cell, f"{self.opposite_side(prev_cell.outbound)}_wall", False)

            this_cell.draw()  
            self.win.redraw()

        print(f"Found End")
            


    def create_winning_path_orig(self):
        x=0
        y=0
        found_end = False
        prev_cell = None
        while not found_end:
            this_cell = self.maze[y][x]
            this_cell.solution = True 
            this_cell.touched = True       

            if x == self.max_columns-1  and y == self.max_rows-1:
                #Set all to True, then apply logic
                this_cell.north_wall = True
                this_cell.south_wall = True
                this_cell.west_wall = True
                this_cell.east_wall = True
                #OPen the 
                self.opposite_side(prev_cell.outbound)
                setattr(this_cell, f"{self.opposite_side(prev_cell.outbound)}_wall", False)

                this_cell.draw()
                break    

            north_cell = None 
            south_cell = None
            east_cell = None 
            west_cell = None

            paths_to_take = ["north", "south", "east", "west"]

            opp_side = None
            if prev_cell is not None:
                opp_side = self.opposite_side(prev_cell.outbound)
                setattr(this_cell, f"{opp_side}_wall", False)                
                paths_to_take.remove(opp_side)

            if x == 0:
                this_cell.west_wall = True 
                if prev_cell and prev_cell.outbound != "south":
                    this_cell.north_wall = True   

                if "west" in paths_to_take:
                    paths_to_take.remove("west")
                if "north" in paths_to_take:
                    paths_to_take.remove("north")
            elif x == self.max_columns-1:
                this_cell.east_wall = True  
                if prev_cell and prev_cell.outbound != "south":
                    this_cell.north_wall = True  

                if "east" in paths_to_take:
                    paths_to_take.remove("east")                      
                if "north" in paths_to_take:     
                    paths_to_take.remove("north")                  
            if y == 0:
                this_cell.north_wall = True
                if prev_cell and prev_cell.outbound != "east":
                    this_cell.west_wall = True                                                          

                if "north" in paths_to_take:
                    paths_to_take.remove("north")
                if "west" in paths_to_take:
                    paths_to_take.remove("west")             
            elif y == self.max_rows-1:
                this_cell.south_wall = True
                if prev_cell and prev_cell.outbound != "east":
                    this_cell.west_wall = True     

                if "south" in paths_to_take:
                    paths_to_take.remove("south")  
                if "west" in paths_to_take:    
                    paths_to_take.remove("west")  
                if "south" in paths_to_take:     
                    paths_to_take.remove("south")  
                                                        
            end_point = f"{self.max_rows -1},{self.max_columns-1}"
            if "west" in paths_to_take:
                find_end = self.check_path_for_failure(self.maze.copy(),y, x-1, [f"{y},{x-1}"])
                if end_point not in find_end:
                    paths_to_take.remove("west")

            if "north" in paths_to_take:      
                find_end = self.check_path_for_failure(self.maze.copy(), y-1,x,[f"{y-1},{x}"])
                if end_point not in find_end:
                    paths_to_take.remove("north")

            if "east" in paths_to_take:      
                find_end = self.check_path_for_failure(self.maze.copy(), y,x+1,[f"{y},{x+1}"])
                if end_point not in find_end:
                    paths_to_take.remove("east")

            if "south" in paths_to_take:      
                find_end = self.check_path_for_failure(self.maze.copy(), y+1,x,[f"{y+1},{x}"])
                if end_point not in find_end:
                    paths_to_take.remove("south")                                        
           
            selected_path = []
            #print(f"Remaining paths: {paths_to_take}")
            while (len(paths_to_take) > 0):
                path_out = random.randrange(0,len(paths_to_take))
                wall_to_use = paths_to_take[path_out]
                #print(f"Walltouse: {wall_to_use}")
                ty=y
                tx=x
                match wall_to_use:
                    case "north":
                        ty -= 1
                    case "south":
                        ty += 1
                    case "east":
                        tx += 1
                    case "west":
                        tx -= 1

                tmp_cell = self.maze[ty][tx]
                already_used = getattr(tmp_cell, "touched")
                #print(f"Already used:{already_used}")
                if not already_used:
                    selected_path.append(wall_to_use)
                else:
                    setattr(this_cell, f"{wall_to_use}_wall", True)
                paths_to_take.remove(wall_to_use)

            paths_to_take = selected_path
            #print(f"Remaining paths: {paths_to_take}")

            while (len(paths_to_take) > 1):
                    path_out = random.randrange(0,len(paths_to_take))
                    #Reflect to set the wall state
                    wall_to_use = paths_to_take[path_out]
                    setattr(this_cell, f"{wall_to_use}_wall", True)
                    paths_to_take.remove(wall_to_use)
                    #print(f"Remaining paths: {paths_to_take}")
            
            #print(f"DD NORTH: {this_cell.north_wall}, SOUTH: {this_cell.south_wall}, EAST:{this_cell.east_wall}, WEST: {this_cell.west_wall}")
            if len(paths_to_take) > 0:
                #print(f"CC PATH TO TAKE: {paths_to_take}")
                prev_x = x
                prev_y = y
                this_cell.outbound = paths_to_take[0]
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
            #else:
                #print("CC No paths to take")
            #print(f"CC NORTH: {this_cell.north_wall}, SOUTH: {this_cell.south_wall}, EAST:{this_cell.east_wall}, WEST: {this_cell.west_wall}") 
            
            this_cell.draw()
            self.win.redraw()
            time.sleep(.01)


            #print("S================================================")
            
            #Now to figure out where to go and the allowed path to take
            #If x == max x or 0 then no north bound
            #If y == 0 or max y then no west

        print(f"Found End")
            
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
        print("Filling the rest of the maze")
        #Start at 0,1 and if in use .. move to the end of the line, then go to row 1, if any are not used build from the unused spot
        #Keep track of the last check to continue from



