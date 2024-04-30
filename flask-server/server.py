from flask import Flask, request, jsonify
from flask_cors import CORS
import easyocr
import logging
from aadhar_ocr import get_aadhar_data
# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)

app = Flask(__name__)
CORS(app)
reader = easyocr.Reader(['en', 'hi'])

import pan_ocr as po
import crud_operations as crud


# @app.route('/aadhar/extract_data', methods=['POST'])
# def aadhar_extract_data():
#     pass

# @app.route('/aadhar/store_data', methods=['POST'])
# def aadhar_store_data():
#     pass

# @app.route('/aadhar/get_all_data', methods=['POST'])
# def aadhar_get_all_data():
#     pass


@app.route('/pan/extract_data', methods=['POST'])
def pan_extract_data():
    try:
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save the uploaded image
        file_path = 'uploaded_image.png'
        file.save(file_path)

        # Process the image
        result = reader.readtext(file_path, paragraph=False, decoder="beamsearch")
        text = ""
        for i in result:
            text += i[1]
            text += '\n'
        data = po.extract_pan_data(text)

        return jsonify(data)
    except Exception as e:
        logging.error(f"Error uploading file: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/pan/store_data', methods=['POST'])
def pan_store_data():
    try:
        data = request.json
        crud.pan_save_to_database(data)
        return jsonify({'message': 'Data saved successfully'})
    except Exception as e:
        logging.error(f"Error submitting data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/pan/get_all_data', methods=['GET'])
def pan_get_all_data():
    return crud.pan_get_all_data()

##aadhar
@app.route('/aadhar/extract_data', methods=['POST'])
def aadhar_extract_data():
    try:
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        file_path = 'uploaded_image.png'
        file.save(file_path)

        # Extract Aadhar data from the uploaded image
        aadhar_data = get_aadhar_data(file_path)

        return jsonify(aadhar_data)
    except Exception as e:
        logging.error(f"Error uploading file: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/aadhar/store_data', methods=['POST'])
def aadhar_store_data():
    try:
        data = request.json
        crud.aadhar_save_to_database(data)
        return jsonify({'message': 'Data saved successfully'})
    except Exception as e:
        logging.error(f"Error submitting data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/aadhar/get_all_data', methods=['GET'])
def aadhar_get_all_data():
    return crud.aadhar_get_all_data()

if __name__ == '__main__':
    app.run(debug=True)