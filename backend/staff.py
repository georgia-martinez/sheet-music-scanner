import cv2
import numpy as np


def staff_y_coords(image_url, debug=False):
    """
    Returns the y coords for the 5 lines in the staff
    """

    image = cv2.imread(image_url)

    open_cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    line_image, lines = horizontal_lines(open_cv_image)

    if debug:
        cv2.imshow(f"Horizontal Lines", line_image)
        cv2.waitKey(0)

    line_y_coords = set()

    for line in lines:
        x1, y1, x2, y2 = line

        line_y_coords.add(y1)

    line_y_coords = list(line_y_coords);
    line_y_coords.sort()

    line_y_coords = group_and_average(line_y_coords, 5)

    space_y_coords = staff_space_y_coords(line_y_coords)

    result = (line_y_coords + space_y_coords)
    result.sort(reverse=True)

    return result

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

def horizontal_lines(image, min_line_length=100, max_line_gap=20):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    lines = cv2.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi / 180,
        threshold=100,
        minLineLength=min_line_length,
        maxLineGap=max_line_gap
    )
    
    line_image = image.copy()
    horizontal_lines = []

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]

            if abs(y1 - y2) < 10:
                horizontal_lines.append((x1, y1, x2, y2))
                cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    return line_image, horizontal_lines
