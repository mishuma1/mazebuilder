from tkinter import Tk, BOTH, Canvas, Label, Button, Toplevel, Frame
from line import Line
from point import Point
import random
from constants import CELL_SIZE
#from cell import Cell

class Cell:
    def __init__(self, root, start_point: Point, end_point: Point, north_wall=False, south_wall=False, east_wall=False, west_wall=False):
    #def __init__(self, root, start_point: Point, end_point: Point, north_wall=True, south_wall=True, east_wall=True, west_wall=True):
        self.root_window = root
        self.north_wall = north_wall
        self.south_wall = south_wall
        self.west_wall = west_wall
        self.east_wall = east_wall

        #self.start_point = start_point
        #self.end_point = end_point
        self.x1 = start_point.x
        self.y1 = start_point.y
        self.x2 = end_point.x
        self.y2 = end_point.y
        #This will be our test to process or not
        self.touched = False
        self.solution = False
        self.outbound = None

    def draw(self):
        if self.north_wall:        
            line = Line(Point(self.x1, self.y1), Point(self.x2,self.y1))
            self.root_window.draw_line(line, "blue")
        if self.south_wall:        
            line = Line(Point(self.x1, self.y2), Point(self.x2,self.y2))
            self.root_window.draw_line(line, "blue")
        if self.west_wall:        
            line = Line(Point(self.x1, self.y1), Point(self.x1,self.y2))
            self.root_window.draw_line(line, "blue")
        if self.east_wall:        
            line = Line(Point(self.x2, self.y1), Point(self.x2,self.y2))
            self.root_window.draw_line(line, "blue")

    def draw_move(self, to_cell, undo=False):
        bgcolor = "gray"
        if undo:
            bgcolor = "red"
        #Draw line, find center
        midpoint = CELL_SIZE //2
        line = Line(Point(self.x1+midpoint,self.y1+midpoint), Point(to_cell.x1+midpoint,to_cell.y1+midpoint))
        line.draw(self.root_window.canvas, bgcolor)


