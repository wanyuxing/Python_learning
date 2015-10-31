"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
@Author: Henry Wan
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        if self._grid[target_row][target_col] != 0:
            return False       
        for row in range(target_row + 1, self._height):
            for col in range(self._width):
                if self._grid[row][col] != col + self._width * row:
                    return False
        for col in range(target_col + 1, self._width):
            if self._grid[target_row][col] != col + self._width * target_row:
                return False
        return True
    
    def position_tile(self, target_pos, target_tile):
        """
        Helper function to put target tile (m, n) to target position (i, j) when j > 1. 
        And put 0 tile on the left of target tile
        """
        ans = ''
        tile_value_col = (self._grid[target_tile[0]][target_tile[1]] + 1) % self._width
        tile_value_row = (self._grid[target_tile[0]][target_tile[1]] + 1) / self._width
        if (tile_value_col != 0):
            tile_value_col -= 1
        else:
            tile_value_row -= 1
            tile_value_col = self._width - 1
        # move target value to target position
        while target_tile != (target_pos[0], target_pos[1]):
            zero_pos = self.current_position(0, 0)
            while target_tile[0] < zero_pos[0]:
                self.update_puzzle('u')
                ans += 'u'
                zero_pos = self.current_position(0, 0)
                target_tile = self.current_position(tile_value_row, tile_value_col)
            if target_tile == (target_pos[0], target_pos[1]):
                break
            elif target_tile[0] != zero_pos[0]:
                ans += self.return_org(target_pos[0], target_pos[1], 1)
            else:
                if target_tile[1] > zero_pos[1]:
                    while target_tile[1] > zero_pos[1]:
                        self.update_puzzle('r')
                        ans += 'r'
                        zero_pos = self.current_position(0, 0)
                        target_tile = self.current_position(tile_value_row, tile_value_col)
                    if zero_pos[0] < target_pos[0] - 1 or zero_pos[0] == 0:
                        self.update_puzzle('d')
                        ans += 'd'
                        ans += self.return_org(target_pos[0], target_pos[1], 2)
                    else:
                        self.update_puzzle('u')
                        ans += 'u'
                        ans += self.return_org(target_pos[0], target_pos[1], 2)
                else:
                    while target_tile[1] < zero_pos[1]:
                        self.update_puzzle('l')
                        ans += 'l'
                        zero_pos = self.current_position(0, 0)
                        target_tile = self.current_position(tile_value_row, tile_value_col)
                    if target_tile == (target_pos[0], target_pos[1]):
                        break
                    else:
                        ans += self.return_org(target_pos[0], target_pos[1], 0)
        ans += self.return_org(target_pos[0], target_pos[1] - 1, 1)
        return ans

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        assert target_row > 1, "Row out of range"
        assert target_col > 0, "Col out of range"
        assert self.lower_row_invariant(target_row, target_col), "Not in position"
        # find target value and its current postion
        target_tile = self.current_position(target_row, target_col)
        ans = self.position_tile((target_row, target_col), target_tile)    
        return ans
                    
    def return_org(self, target_row, target_col, step):
        """
        Return the zero back to its origin place by moving left, down, and right. Take
        the target postion and output the move string
        """
        ans = ''
        zero_pos = self.current_position(0, 0)
        if zero_pos != (target_row, target_col):
            for dummy in range(step):
                self.update_puzzle('l')
                ans += 'l'
                zero_pos = self.current_position(0, 0)
            while zero_pos[0] < target_row:
                self.update_puzzle('d')
                ans += 'd'
                zero_pos = self.current_position(0, 0)
            while zero_pos[1] < target_col:
                self.update_puzzle('r')
                ans += 'r'
                zero_pos = self.current_position(0, 0)
        return ans

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        assert target_row > 1, "Row out of range"
        self.update_puzzle('ur')
        ans = 'ur'
        target_pos = self.current_position(target_row, 0)  
        if target_pos != (target_row, 0):
            ans += self.position_tile((target_row - 1, 1), target_pos)
            self.update_puzzle("ruldrdlurdluurddlur")
            ans += "ruldrdlurdluurddlur"
        for dummy in range(self._width - 2):
            self.update_puzzle('r')
            ans += 'r' 
        return ans

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self._grid[0][target_col] != 0:
            return False
        if self._grid[1][target_col] != target_col + self._width:   
            return False
        for row in range(2, self._height):
            for col in range(self._width):
                if self._grid[row][col] != col + self._width * row:
                    return False
        if target_col == self._width - 1:
            return True
        else:
            for row in range(2):
                for col in range(target_col + 1, self._width - 1):
                    if self._grid[row][col] != col + self._width * row:
                        return False
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self._grid[1][target_col] != 0:
            return False
        for row in range(2, self._height):
            for col in range(self._width):
                if self._grid[row][col] != col + self._width * row:
                    return False
        if target_col == self._width - 1:
            return True
        else:
            for row in range(2):
                for col in range(target_col + 1, self._width - 1):
                    if self._grid[row][col] != col + self._width * row:
                        return False
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        ans = ''
        if target_col >= 2:
            assert self.row0_invariant(target_col), "row0_tile not ready"
            self.update_puzzle('ld')
            ans = 'ld'
            if self._grid[0][target_col] != target_col:
                target_tile = self.current_position(0, target_col)
                ans += self.n_2_move((1, target_col - 1), target_tile)
                self.update_puzzle('urdlurrdluldrruld')
                ans += 'urdlurrdluldrruld'
        return ans

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        ans = ''
        if target_col >= 2:
            assert self.row1_invariant(target_col), "row1_tile not ready"
            target_tile = self.current_position(1, target_col)
            ans += self.n_2_move((1, target_col), target_tile)
            zero_tile = self.current_position(0, 0)
            if zero_tile[0] == 1:
                self.update_puzzle('u')
                ans += 'u'
            for dummy in range(zero_tile[1], target_col):
                self.update_puzzle('r')
                ans += 'r'
        return ans

    def n_2_move(self, target_pos, target_tile):
        """
        Move target tile to target_pos in 2*n matrix
        """
        ans = ''
        tile_value_col = (self._grid[target_tile[0]][target_tile[1]] + 1) % self._width
        tile_value_row = (self._grid[target_tile[0]][target_tile[1]] + 1) / self._width
        if (tile_value_col != 0):
            tile_value_col -= 1
        else:
            tile_value_row -= 1
            tile_value_col = self._width - 1
        while target_tile != target_pos:
            if target_tile[0] == 0:
                self.update_puzzle('u')
                ans += 'u'
                target_tile = self.current_position(tile_value_row, tile_value_col)
                if target_tile == target_pos:
                    ans += self.return_org(1, target_pos[1] - 1, 1)
                    break
                else:
                    for dummy in range(target_pos[1] - target_tile[1]):
                        self.update_puzzle('l')
                        ans += 'l'
                    ans += self.return_org(target_pos[0], target_pos[1], 0)
            else:
                target_tile = self.current_position(tile_value_row, tile_value_col)
                for dummy in range(target_pos[1] - target_tile[1]):
                    self.update_puzzle('l')
                    ans += 'l'
                target_tile = self.current_position(tile_value_row, tile_value_col)
                if target_tile == target_pos:
                    break 
                else:
                    self.update_puzzle('u')
                    ans += 'u'
                    zero_tile = self.current_position(0, 0)
                    for dummy in range(target_pos[1] - zero_tile[1]):
                        self.update_puzzle('r')
                        ans += 'r'
                    self.update_puzzle('d')
                    ans += 'd'
        return ans

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        ans = ''
        zero_pos = self.current_position(0, 0)
        if zero_pos[0] < 2 and zero_pos[1] < 2:
            if zero_pos[0] != 0:
                self.update_puzzle('u')
                ans += 'u'
            if zero_pos[1] != 0:
                self.update_puzzle('l')
                ans += 'l'
            while (self.current_position(0, 0) != (0, 0) or self.current_position(0, 1) != (0, 1)
                   or self.current_position(1, 0) != (1, 0) or self.current_position(1, 1) != (1, 1)):
                self.update_puzzle('rdlu')
                ans += 'rdlu'
        return ans

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        ans = ''
        zero_pos = self.current_position(0, 0)
        for dummy in range(self._height - 1 - zero_pos[0]):
            self.update_puzzle('d')
            ans += 'd'
        for dummy in range(self._width - 1 - zero_pos[1]):
            self.update_puzzle('r')
            ans += 'r'
        if self._height > 2:
            for row in range(self._height - 1, 1, -1):
                for col in range(self._width - 1, -1, -1):
                    if col != 0:
                        ans += self.solve_interior_tile(row, col)
                    else:
                        ans += self.solve_col0_tile(row)
        if self._width > 2:
            for col in range(self._width - 1, 1, -1):
                ans += self.solve_row1_tile(col)
                ans += self.solve_row0_tile(col)
        ans += self.solve_2x2()
        return ans

# Start interactive simulation
puzzle = Puzzle(2, 5)
poc_fifteen_gui.FifteenGUI(puzzle)
