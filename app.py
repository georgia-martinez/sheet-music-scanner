from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/process-image', methods=['POST'])
def process_image():
    # Handle the image processing
    # You can use your existing detect_horizontal_lines function here

    return jsonify({"message": "Image processed successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
