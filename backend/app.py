import os
import cv2
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Define the directory for saving uploaded files
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create directory if it doesn't exist

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

    horizontal_lines = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            if abs(y1 - y2) < 10:  # Only consider horizontal lines
                horizontal_lines.append((x1, y1, x2, y2))

    return horizontal_lines

@app.route('/process-image', methods=['POST'])
def process_image():
    try:
        # Get the uploaded file
        file = request.files['image']
        # Generate a unique filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        # Save the uploaded file to the designated directory
        file.save(file_path)

        # Read and process the image
        image = cv2.imread(file_path)
        horizontal_lines = detect_horizontal_lines(image)

        return jsonify({
            "horizontal_lines_count": len(horizontal_lines),
            "saved_file_path": file_path
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
