from tkinter import Tk, BOTH, Canvas
from line import Line
from constants import NORMAL_WIN_Y, NORMAL_WIN_X, WINDOW_TITLE

class Window:
	def __init__(self):
		print(f"Creating New Window: {NORMAL_WIN_X}, {NORMAL_WIN_Y}")
		self.width = NORMAL_WIN_X
		self.height = NORMAL_WIN_Y
		self.is_running = False
		self.window_dim = self.winsize()
		#No border
		self.border = 0

		self.root_widget = Tk()
		self.root_widget.geometry(self.window_dim)
		self.root_widget.title(WINDOW_TITLE)
		
		self.canvas = Canvas(self.root_widget, bg="white", highlightthickness=self.border)
		self.canvas.pack(fill=BOTH, expand=True)

		#Map exit app
		self.root_widget.protocol("WM_DELETE_WINDOW", self.close)

	def winsize(self):
		return f"{self.width}x{self.height}"

	def redraw(self):
		self.root_widget.update_idletasks()
		self.root_widget.update()
		lwidth = self.root_widget.winfo_width()
		lheight = self.root_widget.winfo_height()

	def wait_for_close(self):
		self.is_running = True
		while self.is_running:
			self.redraw()
		print("Exiting...")

	def close(self):
		self.is_running = False

	def draw_line(self, line: Line, fill_color):
		line.draw(self.canvas, fill_color)	

	
