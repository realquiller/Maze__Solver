import unittest
from maze import Maze


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_rows = 12
        num_cols = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_rows,  
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_cols,  
        )
    
    def test_maze_with_different_dimensions(self):
        # Test with different row/column combinations
        m1 = Maze(0, 0, 5, 20, 10, 10)
        self.assertEqual(len(m1._cells), 5)
        self.assertEqual(len(m1._cells[0]), 20)
        
        m2 = Maze(0, 0, 15, 7, 10, 10)
        self.assertEqual(len(m2._cells), 15)
        self.assertEqual(len(m2._cells[0]), 7)



    def test_break_entrance_and_exit(self):
        # Create a small test maze
        test_maze = Maze(0, 0, 3, 3, 10, 10)
        
        # Initialize the cells
        test_maze._create_cells()
        
        # Before breaking walls, check that entrance and exit walls exist
        top_left = test_maze._cells[0][0]
        bottom_right = test_maze._cells[2][2]  # Using 3x3 maze, so indices are 0-2
        
        self.assertTrue(top_left.has_top_wall, "Entrance wall should exist before breaking")
        self.assertTrue(bottom_right.has_bottom_wall, "Exit wall should exist before breaking")
        
        # Call the method we're testing
        test_maze._break_entrance_and_exit()
        
        # Check that walls were properly removed
        self.assertFalse(top_left.has_top_wall, "Entrance wall should be removed")
        self.assertFalse(bottom_right.has_bottom_wall, "Exit wall should be removed")
        
        print("All entrance and exit tests passed!")

    def test_reset_cells_visited(self):
        # Create a simplified maze
        maze = Maze(0, 0, 3, 3, 10, 10)  # 3x3 grid
        
        # Mark every cell's 'visited' property as True
        for row in maze._cells:
            for cell in row:
                cell.visited = True

        # Call the method being tested
        maze._reset_cells_visited()

        # Verify that all cells are reset to False
        for row in maze._cells:
            for cell in row:
                self.assertFalse(cell.visited, "The cell's visited property is not properly reset")

    


    



if __name__ == "__main__":
    unittest.main()