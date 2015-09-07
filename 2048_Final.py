"""
Clone of 2048 game - Henry Wan. This program can only run
on http://www.codeskulptor.org
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0), DOWN: (-1, 0), 
           LEFT: (0, 1), RIGHT: (0, -1)}

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    if (line == []):
        return line

    new_line = []
    # point_a is the position of the first nonzero in a row
    point_a = finder(line)

    while (True):
        if (point_a == -1):
            break
        else:
            # point_b is the postision of the next nonzero in a row
            point_b = finder(line[point_a + 1:])
            if (point_b == -1):
                new_line.append(line[point_a]);
                break
            else:
                if (line[point_a] == line[point_a + 1:][point_b]):
                    new_line.append(line[point_a] + line[point_a + 1:][point_b])
                    nextpointer = finder(line[point_a + point_b + 2:])
                    if (nextpointer == -1):
                        break
                    else:
                        point_a = nextpointer + point_a + point_b + 2
                else:
                    new_line.append(line[point_a])
                    point_a = point_a + point_b + 1
                    point_b = finder(line[point_a + 1:])
    
    # Add zeros to the extend that new_line is the same lenght as line
    while (len(line) > len(new_line)):
        new_line.append(0)
        
    return new_line

def finder(line):
    """
    Function that finds the first nonzero element in a row
    """ 
    if (line == []):
        pos = -1
    else:
        pos_max = len(line) - 1
        pos = 0
        while (True):
            if (line[pos] != 0):
                break
            else:
                # Check whether the pointer goes beyond the line
                if (pos < pos_max):
                    pos += 1
                else:
                    pos = -1
                    break
    return pos

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # initialize data
        self._height = grid_height
        self._width = grid_width
        self._val = []
        
        for row in range(self._height):
            new = []
            for col in range(self._width):
                new.append(0)
            self._val.append(new)
            
        # set up dictionaries of initials piles for movements
        self._INITIAL_PILES = {UP: [], DOWN: [], LEFT: [], RIGHT: []}
        initial_up = []
        initial_down = []
        initial_left = []
        initial_right = []
       
        for col in range(self._width):
            initial_up.append([0, col])       
            initial_down.append((self._height - 1, col))
        self._INITIAL_PILES[UP] = initial_up
        self._INITIAL_PILES[DOWN] = initial_down
        
        for row in range(self._height):
            initial_left.append((row, 0))
            initial_right.append((row, self._width - 1))
        self._INITIAL_PILES[LEFT] = initial_left
        self._INITIAL_PILES[RIGHT] = initial_right

        # set the values of tiles
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        for row in range(self._height):
            for col in range(self._width):
                self._val[row][col] = 0
        self.new_tile()
        self.new_tile()
        
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return ""

    def get_grid_height(self):
        """
        Return the height of grid
        """
        return self._height

    def get_grid_width(self):
        """
        Return the width of grid
        """
        return self._width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        changed = False
        for item in self._INITIAL_PILES[direction]:
            line = self.traverse(item, direction) 
            new_line = merge(line)
            row = item[0]
            col = item[1] 
            for element in new_line:
                if (self._val[row][col] != element):
                    self._val[row][col] = element
                    changed = True
                row += OFFSETS[direction][0]
                col += OFFSETS[direction][1]
        
        if (changed == True):
            self.new_tile()
    
    def traverse(self, start, direction):
        """
        Iterates through the cells in a linear direction
        """
        line = []
        row = start[0]
        col = start[1]
        while (row < self._height and col < self._width 
               and col > -1 and row > -1):
            line.append(self._val[row][col])
            row += OFFSETS[direction][0]
            col += OFFSETS[direction][1]
        return line
    
    def zero(self):
        """
        Checking whether zero value exists in the grid
        """
        for row in range(self._height): 
            for col in range(self._width):
                if (self._val[row][col] == 0):
                    return True
        return False
                
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        if (self.zero() == True):
            row = random.randrange(0, self._height)
            col = random.randrange(0, self._width)
            while (self._val[row][col] != 0):
                row = random.randrange(0, self._height)
                col = random.randrange(0, self._width)
            if (random.random() < 0.9):
                self._val[row][col] = 2
            else:
                self._val[row][col] = 4

    def set_tile(self, row, col, value):
        """
        Set the value to a tile
        """
        self._val[row][col] = value

    def get_tile(self, row, col):
        """
        Get the value of a tile
        """
        return self._val[row][col]

poc_2048_gui.run_gui(TwentyFortyEight(4, 8))