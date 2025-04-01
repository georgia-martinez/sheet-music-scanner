import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN

from utils import show_image, horizontal_lines

def staff_y_coords(image, debug):
    """
    Returns the y coords for the 5 lines in the staff

    :param image:
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
    """
    Given a set of y coords for the staff lines, returns a list of y coords
    for the spaces between the lines
    
    :param line_y_coords: y coords of staff lines
    :return: y coords of spaces between staff lines
    """

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

def isolate_staffs(image, debug=False):
    inverted_image = cv2.bitwise_not(image)
    bw = cv2.adaptiveThreshold(inverted_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, \
                                cv2.THRESH_BINARY, 15, -2)

    horizontal = np.copy(bw)

    cols = horizontal.shape[1]
    horizontal_size = cols // 30

    horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))

    horizontal = cv2.erode(horizontal, horizontalStructure)
    horizontal = cv2.dilate(horizontal, horizontalStructure)

    if debug: show_image("horizontal", horizontal)

    staff_bounds = find_staffs(horizontal)

    _, width = image.shape[:2]

    staff_images = []

    for bounds in staff_bounds:
        lower, upper = bounds

        spacer = 100

        cropped_image = image[lower-spacer:upper+spacer, 0:width]

        staff_images.append(cropped_image)

        show_image("cropped", cropped_image)

    return staff_images

def find_staffs(image):
    # Calculate the histogram (sum of white pixels along y-axis)
    y_histogram = np.sum(image, axis=1)

    # Find peaks in the histogram (rows with high intensity)
    threshold = np.max(y_histogram) * 0.5
    peak_indices = np.where(y_histogram > threshold)[0]

    # Reshape for clustering
    peak_points = np.array(peak_indices).reshape(-1, 1)

    # Apply DBSCAN clustering
    dbscan = DBSCAN(eps=20, min_samples=1) 
    labels = dbscan.fit_predict(peak_points)

    # Group clustered y-coordinates (separate staffs)
    clustered_bounds = []
    
    for label in set(labels):
        if label == -1:
            continue  # Ignore noise
        cluster = peak_points[labels == label].flatten()
        lower_bound = np.min(cluster)
        upper_bound = np.max(cluster)
        clustered_bounds.append((lower_bound, upper_bound))

    clustered_bounds.sort()

    plt.figure(figsize=(10, 5))
    plt.plot(range(len(y_histogram)), y_histogram, color='blue', label="Pixel Intensity")
    plt.gca().invert_yaxis()
    plt.xlabel("Y-Coordinate")
    plt.ylabel("Pixel Intensity Sum")
    plt.title("Y-Axis Pixel Intensity Histogram")

    # Overlay clustered regions on histogram
    for (lower, upper) in clustered_bounds:
        plt.axvspan(lower, upper, color='red', alpha=0.3, label="Detected Line Region" if (lower, upper) == clustered_bounds[0] else "")

    plt.legend()
    plt.show()

    return clustered_bounds  # Returns list of (lower_bound, upper_bound) pairs

def remove_staff(image, debug=False):
    """
    Removes staff line from given image

    :param image:
    """
    # Code from https://docs.opencv.org/4.x/dd/dd7/tutorial_morph_lines_detection.html

    # Apply adaptiveThreshold at the bitwise_not of gray
    image = cv2.bitwise_not(image)
    bw = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, \
                                cv2.THRESH_BINARY, 15, -2)

    # Create the images that will use to extract the horizontal and vertical lines
    horizontal = np.copy(bw)
    vertical = np.copy(bw)

    # Specify size on horizontal axis
    cols = horizontal.shape[1]
    horizontal_size = cols // 30

    # Create structure element for extracting horizontal lines through morphology operations
    horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))

    # Apply morphology operations
    horizontal = cv2.erode(horizontal, horizontalStructure)
    horizontal = cv2.dilate(horizontal, horizontalStructure)

    if debug: show_image("horizontal", horizontal)

    # Specify size on vertical axis
    rows = vertical.shape[0]
    verticalsize = rows // 30

    # Create structure element for extracting vertical lines through morphology operations
    verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, verticalsize))

    # Apply morphology operations
    vertical = cv2.erode(vertical, verticalStructure)
    vertical = cv2.dilate(vertical, verticalStructure)

    if debug: show_image("vertical", vertical)

    # Inverse vertical image
    vertical = cv2.bitwise_not(vertical)

    # Extract edges and smooth image according to the logic
    # 1. extract edges
    # 2. dilate(edges)
    # 3. src.copyTo(smooth)
    # 4. blur smooth img
    # 5. smooth.copyTo(src, edges)

    # Step 1
    edges = cv2.adaptiveThreshold(vertical, 255, cv2.ADAPTIVE_THRESH_MEAN_C, \
                                cv2.THRESH_BINARY, 3, -2)
    if debug: show_image("edges", edges)

    # Step 2
    kernel = np.ones((2, 2), np.uint8)
    edges = cv2.dilate(edges, kernel)
    
    if debug: show_image("dilate", edges)

    # Step 3
    smooth = np.copy(vertical)

    # Step 4
    smooth = cv2.blur(smooth, (2, 2))

    # Step 5
    (rows, cols) = np.where(edges != 0)
    vertical[rows, cols] = smooth[rows, cols]

    if debug: show_image("smooth - final", vertical)

    return vertical