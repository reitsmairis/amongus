from bresenham import bresenham
import numpy as np 
import copy


def end_coordinates(vision_range, angles):
    ''' Defines the end-points of the vision lines.
    
    Parameters:
        vision_range = how much grid cells can an agent look ahead
        angles = a list of angles at which a vision line should be calculated
        
    Returns:
        x_coords = a list of x coordinates of the end-points
        y_coords = a list of y coordinates of the end-points
    '''
    x_coords = []
    y_coords = []
    for i in angles: 
        x = vision_range * np.cos(i)
        y = vision_range * np.sin(i)
        x_coords.append(round(x))
        y_coords.append(round(y))
    
    return x_coords, y_coords


def origin_lines(x_coords, y_coords):
    ''' Defines a list of vision lines from the origin. 
    
    Parameters:
        x_coords = a list of x coordinates of the end-points of the lines
        y_coords = a list of y coordinates of the end-points of the lines
        
    Returns:
        lines = a 2d list containing the vision lines
    ''' 
    lines = []
    for i in range(len(x_coords)):
        line = list(bresenham(0, 0, x_coords[i], y_coords[i]))
        lines.append(line)
    
    return lines


def transform(lines, pos):
    ''' Transforms the vision lines to the position of an agent. 
    
    Parameters:
        lines = a 2d list containing the vision lines from the origin
        pos = position of the agent (x, y)
        
    Returns:
        transformed_lines = a 2d list containing the vision lines from the 
            agents position
       
    ''' 
    transformed_lines = copy.deepcopy(lines)
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            transformed_lines[i][j] = tuple(map(sum, zip(lines[i][j], pos)))
            
    return transformed_lines             

    
# determine the end coordinates of the lines
vision_range = 20
angles = np.arange(0, 2*np.pi, np.pi/250)
x_coords, y_coords = end_coordinates(vision_range, angles)

# use Bresenham's line algorithm to find vision lines from origin
lines = origin_lines(x_coords, y_coords)

