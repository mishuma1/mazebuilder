from cell import Cell

def set_walls(current_cell: Cell, n,s,e,w, touched, solution=False):
    current_cell.north_wall = n
    current_cell.south_wall = s
    current_cell.east_wall = e
    current_cell.west_wall = w
    current_cell.touched = touched
    current_cell.solution = solution
    return current_cell   

def remove_path(current_paths, remove_paths):
    for remove_item in remove_paths:
        if remove_item in current_paths:
            current_paths.remove(remove_item)
    return current_paths