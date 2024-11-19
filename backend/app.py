import os
import cv2
import numpy as np
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from pdf2image import convert_from_path

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Directory to save uploaded files and extracted images
UPLOAD_FOLDER = "uploads"
PDF_IMAGES_FOLDER = "pdf_images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PDF_IMAGES_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Function to detect staff y-coordinates
def get_staff_coords(image_url, debug=False):
    """
    Returns the y-coordinates for the 5 lines in the staff.
    """
    image = cv2.imread(image_url)
    line_image, horizontal_lines = get_horizontal_lines(image)

    if debug:
        cv2.imshow("Horizontal Lines", line_image)
        cv2.waitKey(0)

    y_coords = set()

    for line in horizontal_lines:
        _, y1, _, y2 = line
        y_coords.add(y1)

    return sorted(y_coords)

# Function to detect horizontal lines
def get_horizontal_lines(image, min_line_length=100, max_line_gap=20):
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
            if abs(y1 - y2) < 10:  # Horizontal line check
                horizontal_lines.append((x1, y1, x2, y2))
                cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return line_image, horizontal_lines

# Route to upload and process a PDF
@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    try:
        if 'file' not in request.files:
            app.logger.error("No file part in the request")
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files['file']
        if file.filename == '':
            app.logger.error("No file selected")
            return jsonify({"error": "No file selected"}), 400

        if not file.filename.endswith('.pdf'):
            app.logger.error("Invalid file type")
            return jsonify({"error": "Invalid file type. Only PDFs are allowed."}), 400

        # Save the uploaded PDF
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        app.logger.info(f"Saved PDF to {file_path}")

        # Process PDF pages
        images = convert_from_path(file_path, output_folder=PDF_IMAGES_FOLDER, fmt='png')
        all_coords = {}

        for i, image in enumerate(images):
            image_path = os.path.join(PDF_IMAGES_FOLDER, f"page_{i + 1}.png")
            image.save(image_path)
            app.logger.info(f"Saved image: {image_path}")

            coords = get_staff_coords(image_path)
            all_coords[f"page_{i + 1}"] = coords
            app.logger.info(f"Coords for page {i + 1}: {coords}")

        return jsonify({
            "message": f"PDF '{file.filename}' processed successfully!",
            "staff_coords": all_coords
        })
    except Exception as e:
        app.logger.error(f"Error processing PDF: {e}")
        return jsonify({"error": str(e)}), 500

# Route to serve PDFs
@app.route('/get-pdf/<filename>', methods=['GET'])
def get_pdf(filename):
    """
    Serves the uploaded PDF file for download.
    """
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
