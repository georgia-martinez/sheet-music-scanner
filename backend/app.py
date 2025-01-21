import os
import cv2
import numpy as np
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from music_scanner import scan_music

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Atomic1@localhost/music_processor'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Define the directory for saving uploaded files
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create directory if it doesn't exist


class Songs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_name = db.Column(db.String(255), nullable=False)
    artist = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    processed_json = db.Column(db.JSON, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)


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