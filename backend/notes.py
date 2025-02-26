import cv2
import numpy as np

def get_closer(main_image, boxed_noteheads):
    notehead_centers = []

    for box in boxed_noteheads:
        x1, y1, x2, y2 = box

        cropped_image = main_image[y1:y2, x1:x2]

        _, thresh = cv2.threshold(cropped_image, 1, 255, cv2.THRESH_BINARY_INV)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        largest_contour = max(contours, key=cv2.contourArea)

        M = cv2.moments(largest_contour)

        if M['m00'] != 0:
            cX = int(M['m10'] / M['m00'])
            cY = int(M['m01'] / M['m00'])
        else:
            cX, cY = 0, 0

        notehead_centers.append((cX + x1, cY + y1))

    return notehead_centers

def notehead_coords(image, debug):
    pattern_image = cv2.imread("templates/quarter-note.png", cv2.IMREAD_COLOR)
    pattern_gray = cv2.cvtColor(pattern_image, cv2.COLOR_BGR2GRAY)

    scale = 1.2

    resized_pattern = cv2.resize(pattern_gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    result = cv2.matchTemplate(image, resized_pattern, cv2.TM_CCOEFF_NORMED)

    threshold = 0.3
    locations = np.where(result >= threshold)

    boxes = []

    for pt in zip(*locations[::-1]):
        bottom_right = (pt[0] + resized_pattern.shape[1], pt[1] + resized_pattern.shape[0])
        boxes.append([pt[0], pt[1], bottom_right[0], bottom_right[1]])

    # Combine boxes that close to being the same box
    filtered_boxes = non_max_suppression(boxes, 0.1).tolist()
    filtered_boxes.sort(key=lambda box: box[0])

    notehead_centers = get_closer(image, filtered_boxes)

    if debug:
        color_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        for (x1, y1, x2, y2) in filtered_boxes:
            cv2.rectangle(color_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        for (x, y) in notehead_centers:
            cv2.circle(color_image, (x, y), 1, (0, 0, 255), thickness=10)

        cv2.imshow('Matches', color_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return notehead_centers

def non_max_suppression(boxes, overlap_thresh):
    if len(boxes) == 0:
        return []

    boxes = np.array(boxes)
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]

    # Compute the centroids of the boxes
    centroids = np.stack([(x1 + x2) / 2, (y1 + y2) / 2], axis=1)

    keep = []
    visited = np.zeros(len(boxes), dtype=bool)

    for i in range(len(boxes)):
        if visited[i]:
            continue
        keep.append(i)
        visited[i] = True

        # Compute distances from the current box to all other boxes
        distances = np.linalg.norm(centroids - centroids[i], axis=1)

        # Sort by distances (closest to the current box)
        order = np.argsort(distances)

        # Check overlaps for boxes in sorted order
        for j in order:
            if visited[j] or j == i:
                continue
            xx1 = max(x1[i], x1[j])
            yy1 = max(y1[i], y1[j])
            xx2 = min(x2[i], x2[j])
            yy2 = min(y2[i], y2[j])

            w = max(0, xx2 - xx1 + 1)
            h = max(0, yy2 - yy1 + 1)
            overlap = (w * h) / ((x2[j] - x1[j] + 1) * (y2[j] - y1[j] + 1))

            # Suppress boxes with overlap higher than threshold
            if overlap > overlap_thresh:
                visited[j] = True

    return boxes[keep]