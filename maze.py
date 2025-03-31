import time
from tkinter import Tk, BOTH, Canvas



class Maze:
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win,
    ):
        
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win

        self._create_cells()

    def _create_cells(self):
        self._cells = []
        for i in range(self.num_rows):
            column = []
            for j in range(self.num_cols):
                # Create a new cell
                cell = Cell(0, 0, 0, 0, self.win)  # You'll need to calculate these coordinates
                column.append(cell)
            self._cells.append(column)
        
        # Now that the grid is built, we can safely access any cell
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self._draw_cell(i, j)




    def _draw_cell(self, i, j):
        cell = self._cells[i][j]

        x1 = self.x1 + (j * self.cell_size_x)
        y1 = self.y1 + (i * self.cell_size_y)
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y

        cell._x1 = x1
        cell._y1 = y1
        cell._x2 = x2
        cell._y2 = y2

        cell.draw()

        self._animate()

    def _animate(self):
        self.win.redraw()
        time.sleep(0.05)