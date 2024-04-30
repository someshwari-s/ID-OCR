# import libs
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import logging

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# # create connection only one time
# # Connect to MySQL database
# db_connection = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="",
#     database="pan_data"
# )
# cursor = db_connection.cursor(dictionary=True)

# # Close the cursor and database connection
# cursor.close()
# db_connection.close()

    
    
def pan_store_data():
    try:
        data = request.json
        save_to_database(data)
        return jsonify({'message': 'Data saved successfully'})
    except Exception as e:
        logging.error(f"Error submitting data: {str(e)}")
        return jsonify({'error': str(e)}), 500

def pan_get_all_data():
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
    
def pan_save_to_database(data):
    # Connect to MySQL database
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="pan_data"
    )
    cursor = db_connection.cursor()

    # SQL query to insert data into the table
    sql = "INSERT INTO pan_data_ocr (user_pan_no, user_dob, user_name, user_father_name) VALUES (%s, %s, %s, %s)"
    values = (data['pan no'], data['Date of Birth'], data['Name'], data['Father name'])
    cursor.execute(sql, values)

    # Commit changes and close connection 
    db_connection.commit()
    cursor.close()
    db_connection.close()
    
##AADHAR
def aadhar_store_data():
    try:
        data = request.json
        save_to_database(data)
        return jsonify({'message': 'Data saved successfully'})
    except Exception as e:
        logging.error(f"Error submitting data: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
def aadhar_get_all_data():
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
  
    
def aadhar_save_to_database(data):
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