import cv2
import numpy as np

def horizontal_lines(image, threshold, min_line_length, max_line_gap):
    edges = cv2.Canny(image, 50, 150, apertureSize=3)

    lines = cv2.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi / 180,
        threshold=threshold,
        minLineLength=min_line_length,
        maxLineGap=max_line_gap
    )
    
    horizontal_lines = []

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]

            if abs(y1 - y2) < 10:
                horizontal_lines.append((x1, y1, x2, y2))
    
    return horizontal_lines