from flask import Flask, jsonify, request, send_file
from dotenv import load_dotenv
import os
from flask_cors import CORS
from utils import predict_role_from_resume, get_jobs

load_dotenv()

app = Flask(__name__)
CORS(app)

# A simple route
@app.route('/')
def home():
    return "Hello, Flask API!"

# A basic API endpoint
@app.route('/api/data', methods=['GET'])
def get_data():
    sample_data = {'message': 'This is sample data', 'status': 'success'}
    return jsonify(sample_data),200

# An endpoint that accepts POST requests
@app.route('/api/echo', methods=['POST'])
def echo():
    data = request.get_json()
    return jsonify({'you_sent': data})

# Define a folder to save the uploaded files (make sure this directory exists)
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    print("upload_file")
    # Check if the request contains a file
    try:
        if 'file' not in request.files:
            return jsonify({'message': 'No file part'}), 400

        file = request.files['file']
        print(file)

        # If the user doesn't select a file or cancels
        if file.filename == '':
            return jsonify({'message': 'No selected file'}), 400

        # Delete all files in the upload folder
        for f in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, f)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    print(f"Deleted file: {file_path}")
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")

        # Save the file to the upload folder
        if file and file.filename.endswith('.pdf'):  # Check if it's a PDF file
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            print(f"File saved to {filename}")
            file_path = f'pdf/{filename}.pdf'

            predicted_role = predict_role_from_resume(file.filename.split(".pdf")[0])
            jobs = get_jobs(predicted_role)
            # predicted_role = "Data Scientist"
            # filename = 'generated_resume'
            # Send the PDF file
            return jsonify({"predicted_role": predicted_role, "filename": file.filename.split(".pdf")[0],"jobs": jobs}), 200
        else:
            return jsonify({'message': 'Only PDF files are allowed'}), 400
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'An error occurred while uploading the file'}), 500


@app.route('/api/get-resume', methods=['GET'])
def get_resume():
    print("get_resume")
    filename = request.args.get('filename')
    # Check if the request contains a file
    try:
        # Save the file to the upload folder
        print(f"File saved to {filename}")
        file_path = f'pdf/{filename}.pdf'

        # Send the PDF file
        return send_file(file_path), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'An error occurred while uploading the file'}), 500

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)
