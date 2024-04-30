
import re
import easyocr

import sys
sys.stdout.reconfigure(encoding = 'utf-8')

reader = easyocr.Reader(['en', 'hi'])


def get_aadhar_data(img_path):
    result = reader.readtext(img_path, paragraph=False, decoder="beamsearch")

    text = ""
    for i in result:
        text += i[1] + '\n'

    print("Result to string:", text)

    aadhar_data = {}

    # Regular expressions to extract Aadhar number, DOB, and gender
    aadhar_number_pat = r'\b\d{4}\s\d{4}\s\d{4}\b|\b\d{12}\b'  # 12 digits in a row or separated by spaces after every 4 digits
    dob_pat = r'\b(\d{2}-\d{2}-\d{4})|(\d{2}/\d{2}/\d{4})|\b\d{4}\b'  # dd-mm-yyyy, dd/mm/yyyy format, or only year
    gender_pat = r'(Male|MALE|IIALE|Female|Ferale|FEMALE|Transgender)'

    # Search for Aadhar number, DOB, and gender in the text and extract corresponding information
    aadhar_number_match = re.search(aadhar_number_pat, text)
    if aadhar_number_match:
        aadhar_data['Aadhar No'] = aadhar_number_match.group()

    dob_match = re.search(dob_pat, text)
    if dob_match:
        dob_str = dob_match.group()
        if '-' in dob_str or '/' in dob_str:  # If dob is in dd-mm-yyyy or dd/mm/yyyy format
            aadhar_data['DOB'] = dob_str
        else:  # If only the year is provided
            year = int(dob_str)
            dob_str = f'01-01-{year}'
            aadhar_data['DOB'] = dob_str
    else:  # If DOB not found, set default as 01-01-Not Found
        aadhar_data['DOB'] = '01-01-Not Found'

    # Heuristic approach to extract name
    name = get_name_from_text(text)
    if name:
        aadhar_data['Name'] = name
    else:
        aadhar_data['Name'] = 'Not Found'

    gender_match = re.search(gender_pat, text)
    if gender_match:
        gender = gender_match.group().lower()  # Convert to lowercase for uniformity
        if gender.startswith('f'):  # If gender starts with 'f', assume female
            aadhar_data['Gender'] = 'Female'
        elif gender.startswith('m'):  # If gender starts with 'm', assume male
            aadhar_data['Gender'] = 'Male'
        else:
            aadhar_data['Gender'] = 'Not Found'
    else:
        aadhar_data['Gender'] = 'Not Found'

    return aadhar_data


def get_name_from_text(text):
    # Regular expression to capture potential names
    name_pat = r'[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+'  # Matches capitalized words (first and last name) separated by spaces

    # Search for potential names in the text
    name_match = re.search(name_pat, text)
    if name_match:
        return name_match.group().strip()  # Return the captured name
    else:
        return None  # Return None if no name is found

if __name__ == '__main__':
    print(get_aadhar_data("./aadhar2.jpeg"))