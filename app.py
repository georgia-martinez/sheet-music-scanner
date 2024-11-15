import cv2
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#TODO: Implement the detect_horizontal_lines function
#def detect_horizontal_lines()

@app.route('/process-image', methods=['POST'])
def process_image():
    file = request.files['image']
    file.save("uploaded_image.png")
    image = cv2.imread("uploaded_image.png")
    line_detected_image, horizontal_lines = detect_horizontal_lines(image)
    return jsonify({"horizontal_lines_count": len(horizontal_lines)})

if __name__ == '__main__':
    app.run(debug=True)
if __name__ == '__main__':
    app.run(debug=True)
