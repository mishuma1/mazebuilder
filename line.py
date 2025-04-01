from tkinter import Tk, BOTH, Canvas, Label, Button, Toplevel, Frame
from point import Point
from constants import LINE_THICK

class Line:
    def __init__(self, start_point: Point,end_point: Point):
        self.start_point = start_point
        self.end_point = end_point

    def draw(self, canvas: Canvas, fill_color):
        canvas.create_line(self.start_point.x, self.start_point.y, 
            self.end_point.x, self.end_point.y, fill=fill_color, width=LINE_THICK)


