import cv2
import numpy as np

from utils import horizontal_lines

def staff_y_coords(image, debug):
    """
    Returns the y coords for the 5 lines in the staff
    """

    lines = horizontal_lines(image, 100, 100, 20)

    line_y_coords = set()

    for line in lines:
        x1, y1, x2, y2 = line

        line_y_coords.add(y1)

    line_y_coords = list(line_y_coords);
    line_y_coords.sort()

    line_y_coords = group_and_average(line_y_coords, 5)

    space_y_coords = staff_space_y_coords(line_y_coords)

    all_y_coords = (line_y_coords + space_y_coords)
    all_y_coords.sort()

    if debug:
        color_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        for y in all_y_coords:
            cv2.line(color_image, (0, int(y)), (color_image.shape[1], int(y)), (0, 255, 0), 1)

        cv2.imshow("Staff Lines Found", color_image)
        cv2.waitKey(0)

    return all_y_coords

def staff_space_y_coords(line_y_coords):
    result = []

    for i in range(len(line_y_coords)):
        if i == len(line_y_coords)-1:
            break
        
        middle = int((line_y_coords[i+1] + line_y_coords[i]) / 2);

        result.append(middle)

    return result;

def group_and_average(values, n):
    if len(values) <= n:
        return values
    
    values = sorted(values)
    
    step = len(values) // n
    
    grouped_values = []
    
    for i in range(0, len(values), step):
        group = values[i:i + step]
        
        avg = np.mean(group)
        
        grouped_values.append(int(avg))
    
    while len(grouped_values) > n:
        last = grouped_values.pop()
        grouped_values[-1] = int(np.mean([grouped_values[-1], last]))
    
    return grouped_values
