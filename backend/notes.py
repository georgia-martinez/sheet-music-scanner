import cv2
import numpy as np

def non_max_suppression(boxes, overlap_thresh):
    if len(boxes) == 0:
        return []

    boxes = np.array(boxes)
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]

    # Compute the area of the rectangles
    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    order = np.argsort(areas)[::-1]  # Sort by area

    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)

        # Compute overlap
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])

        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)
        overlap = (w * h) / areas[order[1:]]

        # Suppress boxes with overlap higher than threshold
        order = order[np.where(overlap <= overlap_thresh)[0] + 1]

    return boxes[keep]

main_image = cv2.imread("test.png", cv2.IMREAD_COLOR)
pattern_image = cv2.imread("note_head.png", cv2.IMREAD_COLOR)

main_gray = cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY)
pattern_gray = cv2.cvtColor(pattern_image, cv2.COLOR_BGR2GRAY)

result = cv2.matchTemplate(main_gray, pattern_gray, cv2.TM_CCOEFF_NORMED)

threshold = 0.3
locations = np.where(result >= threshold)

scale = 0.4

resized_pattern = cv2.resize(pattern_gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

result = cv2.matchTemplate(main_gray, resized_pattern, cv2.TM_CCOEFF_NORMED)
locations = np.where(result >= threshold)

boxes = []

for pt in zip(*locations[::-1]):
    bottom_right = (pt[0] + resized_pattern.shape[1], pt[1] + resized_pattern.shape[0])
    boxes.append([pt[0], pt[1], bottom_right[0], bottom_right[1]])

# Apply Non-Maximum Suppression
filtered_boxes = non_max_suppression(boxes, overlap_thresh=0.2)

print(len(filtered_boxes))

# Draw rectangles for filtered matches
for (x1, y1, x2, y2) in filtered_boxes:
    cv2.rectangle(main_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

cv2.imshow('Matches', main_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
