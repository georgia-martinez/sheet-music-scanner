from staff import horizontal_lines
import cv2
import numpy as np

def remove_staff_lines(image_url):
    image = cv2.imread(image_url)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # _, binary_image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    line_image, lines = horizontal_lines(gray, 100, 0, 0)

    final = image.copy()

    # Remove the detected lines by masking them out
    for line in lines:
        x1, y1, x2, y2 = line
        cv2.line(final, (x1, y1), (x2, y2), (255, 255, 255), 2)  # White line to remove

    # Show the final result with horizontal lines removed
    cv2.imshow(f"Horizontal Lines Removed", final)
    cv2.waitKey(0)

    return final

def note_boxes(image_url, debug=False):
    main_image = cv2.imread(image_url, cv2.IMREAD_COLOR)
    # main_image = cv2.cvtColor(remove_staff_lines(image_url), cv2.COLOR_BGR2GRAY)

    pattern_image = cv2.imread("templates/quarter-note.png", cv2.IMREAD_COLOR)

    main_gray = cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY)
    pattern_gray = cv2.cvtColor(pattern_image, cv2.COLOR_BGR2GRAY)

    scale = 1.2

    resized_pattern = cv2.resize(pattern_gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    result = cv2.matchTemplate(main_gray, resized_pattern, cv2.TM_CCOEFF_NORMED)

    threshold = 0.3
    locations = np.where(result >= threshold)

    boxes = []

    for pt in zip(*locations[::-1]):
        bottom_right = (pt[0] + resized_pattern.shape[1], pt[1] + resized_pattern.shape[0])
        boxes.append([pt[0], pt[1], bottom_right[0], bottom_right[1]])

    # Apply Non-Maximum Suppression to remove overlaps
    filtered_boxes = non_max_suppression(boxes, 0.1)

    if debug:
        print(f"Notes found: {len(filtered_boxes)}")

        # Draw rectangles for filtered matches
        for (x1, y1, x2, y2) in filtered_boxes:
            cv2.rectangle(main_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        cv2.imshow('Matches', main_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return filtered_boxes

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

    # Initialize the list to keep indices of selected boxes
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