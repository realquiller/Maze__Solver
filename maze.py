import time, random
from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.root = Tk()
        self.root.title("Maze with solution")
        
        self.my_canvas = Canvas(self.root)
        self.my_canvas.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.window_is_running = False

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.window_is_running = True
        while self.window_is_running:
            self.redraw()

    def close(self):
        self.window_is_running = False
        self.root.destroy()

    def draw_line(self, line, fill_color):
        line.draw(self.my_canvas, fill_color)



class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, point_1, point_2):
        self.point_1 = point_1
        self.point_2 = point_2

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.point_1.x, self.point_1.y, self.point_2.x, self.point_2.y, fill=fill_color, width=2
        )

class Cell:
    def __init__(self, _x1, _y1, _x2, _y2, _win=None, has_left_wall=True, has_right_wall=True, has_top_wall=True, has_bottom_wall=True):
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self._x1 = _x1
        self._x2 = _x2
        self._y1 = _y1
        self._y2 = _y2
        self._win = _win
        self.visited = False

    def draw(self):
        if self._win is None:
            return
        
        # Left wall
        point1 = Point(self._x1, self._y1)
        point2 = Point(self._x1, self._y2)
        line1 = Line(point1, point2)
        color = "black" if self.has_left_wall else "#d9d9d9"
        self._win.draw_line(line1, color)
        
        # Right wall
        point1 = Point(self._x2, self._y1)
        point2 = Point(self._x2, self._y2)
        line1 = Line(point1, point2)
        color = "black" if self.has_right_wall else "#d9d9d9"
        self._win.draw_line(line1, color)
        
        # Top wall
        point1 = Point(self._x1, self._y1)
        point2 = Point(self._x2, self._y1)
        line1 = Line(point1, point2)
        color = "black" if self.has_top_wall else "#d9d9d9"
        self._win.draw_line(line1, color)
        
        # Bottom wall
        point1 = Point(self._x1, self._y2)
        point2 = Point(self._x2, self._y2)
        line1 = Line(point1, point2)
        color = "black" if self.has_bottom_wall else "#d9d9d9"
        self._win.draw_line(line1, color)
    
    def draw_move(self, to_cell, undo=False):
        if undo:
            color = "red"
        else:
            color = "gray"
        
        center1_x = self._x1 + ((self._x2 - self._x1) / 2)
        center1_y = self._y1 + ((self._y2 - self._y1) / 2)
        point1 = Point(center1_x, center1_y)

        center2_x = to_cell._x1 + ((to_cell._x2 - to_cell._x1) / 2)
        center2_y = to_cell._y1 + ((to_cell._y2 - to_cell._y1) / 2)
        point2 = Point(center2_x, center2_y)

        line1 = Line(point1, point2)

        self._win.draw_line(line1, color)

class Maze:
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win = None,
            seed = None
    ):
        
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win

        if seed != None:
            random.seed(seed)

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

        if self.win is not None:
            cell.draw()
            self._animate()

    def _animate(self):
        self.win.redraw()
        time.sleep(0.05)

    
    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self.num_rows-1][self.num_cols-1].has_bottom_wall = False
        self._draw_cell(self.num_rows-1, self.num_cols-1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True

        while True:
            possible_ways = []
            if j > 0 and self._cells[i][j-1].visited == False:
                possible_ways.append((0,-1))

            if j < len(self._cells[i]) - 1 and self._cells[i][j+1].visited == False:
                possible_ways.append((0,1))
            
            if i > 0 and self._cells[i-1][j].visited == False:
                possible_ways.append((-1,0))
            
            if i < len(self._cells) - 1 and self._cells[i+1][j].visited == False:
                possible_ways.append((1,0))

            if len(possible_ways) == 0:
                self._cells[i][j].draw()
                return
            else:
                direction = random.choice(possible_ways)
                if direction == (0, -1):
                    self._cells[i][j].has_left_wall = False
                    self._draw_cell(i, j)
                    self._cells[i + direction[0]][j + direction[1]].has_right_wall = False
                    self._draw_cell(i + direction[0], j + direction[1])

                elif direction == (0, 1):
                    self._cells[i][j].has_right_wall = False
                    self._draw_cell(i, j)
                    self._cells[i + direction[0]][j + direction[1]].has_left_wall = False
                    self._draw_cell(i + direction[0], j + direction[1])

                elif direction == (-1, 0):
                    self._cells[i][j].has_top_wall = False
                    self._draw_cell(i, j)
                    self._cells[i + direction[0]][j + direction[1]].has_bottom_wall = False
                    self._draw_cell(i + direction[0], j + direction[1])

                elif direction == (1, 0):
                    self._cells[i][j].has_bottom_wall = False
                    self._draw_cell(i, j)
                    self._cells[i + direction[0]][j + direction[1]].has_top_wall = False
                    self._draw_cell(i + direction[0], j + direction[1])
            
            #print(f"Moving from ({i}, {j}) to ({i + direction[0]}, {j + direction[1]})")
            self._break_walls_r(i + direction[0], j + direction[1])
    
    def _reset_cells_visited(self):
        for row in self._cells:
            for cell in row:
                cell.visited = False

    def solve(self):
        return self._solve_r()
    
    def _solve_r(self, i=0, j=0):
        #CURRENT CELL (VISITED)
        current = self._cells[i][j]
        self._animate()
        current.visited = True
        
        #print(f"checking i: {i} and j: {j} inside solve_r")
        
        # ARE YOU FINISHED?
        if current == self._cells[self.num_rows-1][self.num_cols-1]:
            return True
        
        # CHECK AND MOVE RIGHT
        if j < len(self._cells[i]) - 1 and self._cells[i][j + 1].visited == False and self._cells[i][j].has_right_wall == False:
            self._cells[i][j].draw_move(self._cells[i][j+1])
            if self._solve_r(i, j+1) == True:
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j+1], True)
        
        # CHECK AND MOVE DOWN
        if i < len(self._cells) - 1 and self._cells[i+1][j].visited == False and self._cells[i][j].has_bottom_wall == False:
            self._cells[i][j].draw_move(self._cells[i+1][j])
            if self._solve_r(i+1, j) == True:
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i+1][j], True)

        # CHECK AND MOVE LEFT
        if j > 0 and self._cells[i][j-1].visited == False and self._cells[i][j].has_left_wall == False:
            #print("I AM INSIDE LEFT CHECK")
            self._cells[i][j].draw_move(self._cells[i][j-1])
            if self._solve_r(i, j-1) == True:
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j-1], True)

        # CHECK AND MOVE UP
        if i > 0 and self._cells[i-1][j].visited == False and self._cells[i][j].has_top_wall == False:
            self._cells[i][j].draw_move(self._cells[i-1][j])
            if self._solve_r(i-1, j) == True:
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i-1][j], True)
        
        
        
        return False







            







def main():
    pass
    win = Window(800, 600)


    maze1 = Maze(45, 50, 6, 6, 20, 30, win, 2)
    
    maze1._break_walls_r(0, 0)
    maze1._break_entrance_and_exit()
    maze1._reset_cells_visited()
    maze1.solve()


    win.wait_for_close()


if __name__ == "__main__":
    main()