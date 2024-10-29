import cv2
import numpy as np

def detect_horizontal_lines(image, min_line_length=100, max_line_gap=20):
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


image = cv2.imread("test.png")

open_cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

line_detected_image, horizontal_lines = detect_horizontal_lines(open_cv_image)

cv2.imshow(f"Horizontal Lines", line_detected_image)
cv2.waitKey(0)

y_coords = set()

for line in horizontal_lines:
    x1, y1, x2, y2 = line

    y_coords.add(y1)

print(len(y_coords))
