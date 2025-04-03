from tkinter import Tk, BOTH, Canvas, Label, Button, Toplevel, Frame
from line import Line
from point import Point
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
	
		#main_label = Label(self.root_widget, text="This is the main window")
		#main_label.pack(padx=200, pady=100)
		# Button to open a new window
		#new_window_button = Button(self.root_widget, text="Open New Window", command=self.open_new_window)
		#new_window_button.pack(pady=10)

		

# Start the Tkinter event loop
	def winsize(self):
		return f"{self.width}x{self.height}"

	def redraw(self):
		self.root_widget.update_idletasks()
		self.root_widget.update()
		lwidth = self.root_widget.winfo_width()
		lheight = self.root_widget.winfo_height()
		#print(f"WIN X: {lwidth}, {lheight}")

	
	def wait_for_close(self):
		self.is_running = True
		while self.is_running:
			self.redraw()
		print("Exiting...")

	def close(self):
		self.is_running = False

	def draw_line(self, line: Line, fill_color):
		line.draw(self.canvas, fill_color)	

	#Test Code from online -- not used yet
	def open_new_window(self):
		new_window = Toplevel(self.root_widget)
		new_window.title("New Window")
		new_window_label = Label(new_window, text="This is a new window")
		new_window_label.pack(padx=200, pady=100)
	
