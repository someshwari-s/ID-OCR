# Import necessary libraries
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
import easyocr
import mysql.connector
import logging

# Import the function to extract Aadhar data from ocr.py
from aadhar_ocr import get_aadhar_data

# Create Flask app
app = Flask(__name__)
CORS(app)
reader = easyocr.Reader(['en', 'hi'])

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# Define function to save data to database
def save_to_database(data):
    try:
        # Connect to MySQL database
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=" ",  # Enter your database password here
            database="aadhar_data"
        )
        cursor = db_connection.cursor()

        # SQL query to insert data into the table
        sql = "INSERT INTO aadhar_ocr (user_aadhar_no, user_name, user_dob, user_gender) VALUES (%s, %s, %s, %s)"
        values = (data['Aadhar No'], data['Name'], data['DOB'], data['Gender'])
        cursor.execute(sql, values)

        # Commit changes and close connection
        db_connection.commit()
        cursor.close()
        db_connection.close()

    except Exception as e:
        # Log the full traceback of the exception
        logging.exception("Error saving data to database")
        raise  # Re-raise the exception to propagate it further

# Define endpoint to handle file upload
@app.route('/upload', methods=['POST'])
def upload_file():
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

# Define endpoint to submit data to the database
@app.route('/submit', methods=['POST'])
def submit_data():
    try:
        data = request.json
        save_to_database(data)
        return jsonify({'message': 'Data saved successfully'})
    except Exception as e:
        logging.error(f"Error submitting data: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Define endpoint to fetch data from the database
@app.route('/fetch', methods=['GET'])
def fetch_data():
    try:
        # Connect to MySQL database
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Enter your database password here
            database="aadhar_data"
        )
        cursor = db_connection.cursor(dictionary=True)

        # SQL query to fetch data from the table
        sql = "SELECT user_aadhar_no, user_name, user_dob, user_gender FROM aadhar_ocr"
        cursor.execute(sql)
        data = cursor.fetchall()

        # Close the cursor and database connection
        cursor.close()
        db_connection.close()

        return jsonify(data)
    except Exception as e:
        logging.error(f"Error fetching data: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
