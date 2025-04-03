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

       '''

        print(f"BB y: {y}, x: {x}, paths_to_open: {path_to_open}, paths_to_take: {paths_to_take}")


        if len(path_to_open) > 0:
            #Clear the current wall to match an exiting wall, if one is found
            print(f"CC paths_to_open: {path_to_open}")
            path_out = random.randrange(0,len(path_to_open))
            wall_to_use = path_to_open[path_out]
            print(f"CCC clearing current wall: {wall_to_use}")
            setattr(current_cell, f"{wall_to_use}_wall", False)
            #paths_to_take.remove(wall_to_use) 

            #Just need to clear the connector wall, if any
            print(f"CCC clearing connecting wall: {self.opposite_side(wall_to_use)}")
            prev_cell = t_maze[path_out]
            prev_cell.outbound = self.opposite_side(wall_to_use)
            setattr(prev_cell, f"{prev_cell.outbound}_wall", False)
            
            
            print(f"BBB y: {y}, x: {x}, paths_to_open: {path_to_open}, paths_to_take: {paths_to_take}")

        if not prev_cell:
            prev_cell = Cell(self.win, Point(0,0), Point(0,0))
            prev_cell.outbound = ""




            #Clear the original wall
            #current_cell.draw()  
            #self.win.redraw()

        while len(paths_to_take) > 0:
            paths_to_take = ["north", "south", "east", "west"]
            print("A++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("B++++++++++++++++++++++++++++++++++++++++++++++++++")

        print(f"y: {y}, x: {x}, walls next to us: {path_to_open}")
        '''
                         
        '''
        path_out = random.randrange(0,len(path_to_open))
        wall_to_use = paths_to_take[path_out]
        setattr(this_cell, f"{wall_to_use}_wall", True)
        paths_to_take.remove(wall_to_use)        


        paths_to_take = ["north", "south", "east", "west"]
        while x != self.max_columns-1  or y != self.max_rows-1 or len(paths_to_take) == 0:
            #print("A++++++++++++++++++++++++++++++++++++++++++++++++++")
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
            #print(f"A Y: {y}, X: {x}, A PATHS Left: {paths_to_take}")
            self.print_wall_status(this_cell)

            if x == 0:
                if prev_cell and prev_cell.outbound != "south":
                    this_cell.north_wall = True   
                #paths_to_take = self.remove_path(paths_to_take, ["west", "north"])
                paths_to_take = self.remove_path(paths_to_take, ["west"])
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

            #print(f"B PATHS Left: {paths_to_take}")
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
            #print(f"END Y: {y}, X: {x}, A PATHS Left: {paths_to_take}")
            self.print_wall_status(this_cell)

            this_cell.draw()
            self.win.redraw()
            time.sleep(DRAW_SPEED)
            #print("E++++++++++++++++++++++++++++++++++++++++++++++++++")

            
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
            self.win.redraw()'
            '''


def opposite_side2(self, wall):
    if wall == "west":
        return "east"
    if wall == "east":
        return "west"
    if wall == "north":
        return "south"
    if wall == "south":
        return "north"

def open_new_path(self, logic, y, x, wall, path_to_open, t_maze):
    opp_side = self.opposite_side(wall)

    if logic:
        tmp_maze = self.maze[y][x]
        opp_wall_status = getattr(tmp_maze, f"{opp_side}_wall")
        if tmp_maze.solution and opp_wall_status:
            path_to_open.append(wall)
            t_maze.append(tmp_maze)
    return path_to_open, t_maze