"""
Merge function for 2048 game. Henry Wan
"""
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