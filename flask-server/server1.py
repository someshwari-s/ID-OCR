from flask import Flask, request, jsonify
import easyocr
import re
from flask_cors import CORS
import mysql.connector
import logging

app = Flask(__name__)
CORS(app)
reader = easyocr.Reader(['en', 'hi'])

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)


@app.route('/upload', methods=['POST'])
def upload_file():
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
        data = extract_pan_data(text)

        return jsonify(data)
    except Exception as e:
        logging.error(f"Error uploading file: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/submit', methods=['POST'])
def submit_data():
    try:
        data = request.json
        save_to_database(data)
        return jsonify({'message': 'Data saved successfully'})
    except Exception as e:
        logging.error(f"Error submitting data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/fetch', methods=['GET'])
def fetch_data():
    try:
        # Connect to MySQL database
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="pan_data"
        )
        cursor = db_connection.cursor(dictionary=True)

        # SQL query to fetch data from the table
        sql = "SELECT user_pan_no, user_dob, user_name, user_father_name FROM pan_data_ocr"
        cursor.execute(sql)
        data = cursor.fetchall()

        # Close the cursor and database connection
        cursor.close()
        db_connection.close()

        return jsonify(data)
    except Exception as e:
        logging.error(f"Error fetching data: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)