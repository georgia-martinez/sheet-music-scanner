import os
import cv2
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from music_scanner import scan_music

app = Flask(__name__)
CORS(app)

# Define the directory for saving uploaded files
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create directory if it doesn't exist

@app.route('/process-image', methods=['POST'])
def process_image():
    try:
        file = request.files['image']

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        file.save(file_path)

        music = scan_music(file_path)

        print(music)

        return jsonify({"music": music})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
