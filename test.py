import unittest
from maze import Maze
from constants import NORMAL_WIN_X, NORMAL_WIN_Y, CELL_SIZE
from window import Window

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = NORMAL_WIN_X//CELL_SIZE
        num_rows = NORMAL_WIN_Y//CELL_SIZE
        new_maze = Maze(Window(), num_cols, num_rows)
        self.assertEqual(
            len(new_maze.maze[0]),
            num_cols,
        )
        self.assertEqual(
            len(new_maze.maze),
            num_rows,
        )

if __name__ == "__main__":
    unittest.main()        