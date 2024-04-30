import re
# import easyocr
import mysql.connector
def convert_date(date):
    if not date:
        return date
    return date[6:] + '-' + date[3:5] + '-' + date[:2]

def extract_pan_data(text):
    # Reading the image, extracting text from it, and storing the text into a list.
    all_text_list = re.split(r'[\n]', text)

    # Process the text list to remove all whitespace elements in the list.
    text_list = list()
    for i in all_text_list:
        if re.match(r'^(\s)+$', i) or i=='':
            continue
        else:
            text_list.append(i)

    # Extracting all the necessary details from the pruned text list.
    # 1) PAN Card No.
    pan_no_pat = r'.*Permanent Account Number Card.*|.*Permanent Account Number.*|.*Permanent Account.*|.*Permanent.*|.*Perm.*|.*Acc.*'
    pan_no = ""
    for i, text in enumerate(text_list):
        if re.match(pan_no_pat, text):
            pan_no = text_list[i+1]
        else:
            continue
    user_pan_no = ""
    for i in pan_no:
        if i.isalnum():
          user_pan_no = user_pan_no + i
        else:
          continue
    # ###########################################

    # 2) DOB
    pan_dob_pat = r'(Year|Birth|irth|YoB|YOB:|DOB:|DOB)'
    user_dob = ""
    dob_idx = -1
    for idx, i in enumerate(text_list):
      if re.search(pan_dob_pat, i):      
        date_str=''
        date_ele = text_list[idx+1]
        dob_idx = idx + 1
        for x in date_ele:
            if re.match(r'\d', x):
                date_str = date_str+x
            elif re.match(r'/', x):
                date_str = date_str+x
            else:
                continue
        user_dob = date_str
        break
      else:
        continue
    if(user_dob == ""):
      pan_date_pat = r'^\d{2}/\d{2}/\d{4}$'
      for idx,i in enumerate(text_list):
        if re.search(pan_date_pat , i):
          dob_idx = idx
          user_dob = i
        else:
          continue

    # Convert date format
    user_dob = convert_date(user_dob)

    # ###########################################
    
    # 3) NAME
    pan_name_pat = r'.*(name|Name).*'
    user_name = ""
    for idx, i in enumerate(text_list):
        if re.search(pan_name_pat, i):
          user_name = text_list[idx + 1]
          break
        else:
          continue
    if(user_name == ""):
      user_name = text_list[dob_idx - 2]


    # 4) Father name 
    pan_father_name_pat = r'.*(Father | father).*(name | Name)'
    user_father_name = ""
    for idx, i in enumerate(text_list):
      if re.search(pan_father_name_pat, i):
        user_father_name = text_list[idx + 1]
        break
      else:
        continue
    if(user_father_name == ""):
      user_father_name = text_list[dob_idx - 1]

    # print("Father name" , user_father_name)


    # ###########################################
    return {
        'pan no' : user_pan_no,
        'Date of Birth' : user_dob,
        'Name' : user_name,
        'Father name' : user_father_name
    }

if __name__ == '__main__':
  app.run(debug=True)