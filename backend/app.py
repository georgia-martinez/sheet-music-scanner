import os
import cv2
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Database configuration
## TODO Figure out shit shit
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Atomic1@localhost/music_processor'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the directory for saving uploaded files
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create directory if it doesn't exist

# Database model
# This should work out well
class Songs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_name = db.Column(db.String(255), nullable=False)
    artist = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    processed_json = db.Column(db.JSON, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create tables
with app.app_context():
    db.create_all()

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

        # Mock song data (replace with actual processing results)
        song_name = "Sample Song"  # Replace with real logic to get song name
        artist = "Sample Artist"  # Replace with real logic to get artist name
        duration = 180  # Replace with logic to calculate actual duration
        processed_json = {
            "notes": [
                {"note": "C", "duration": 1},
                {"note": "D", "duration": 0.5}
            ]
        }

        # Save data to the database
        song = Songs(
            song_name=song_name,
            artist=artist,
            duration=duration,
            processed_json=processed_json
        )
        db.session.add(song)
        db.session.commit()

        # Return response
        return jsonify({
            "message": "File processed and data saved!",
            "song_id": song.id,
            "horizontal_lines_count": len(processed_json["notes"]),
            "saved_file_path": file_path
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
