# import module
from pdf2image import convert_from_path
import cv2
import pytesseract
import Config as config
from ApiResponse import Product, Company
import difflib
import json
import string
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def get_matched_data(input_string, search_terms):
    # define the set of special characters to remove
    special_chars = string.punctuation + ' '
    for term in search_terms:
        if term.lower() in input_string.lower():
            start_index = input_string.lower().index(term.lower()) + len(term) + 1
            end_index = input_string[start_index:].index("\n") + start_index
            return input_string[start_index:end_index].strip(special_chars).strip()
    
    #Partial match search
    highest_ratio = 0
    highest_term = ""
    for term in search_terms:
        ratio = difflib.SequenceMatcher(None, term.lower(), input_string.lower()).ratio()
        if ratio > highest_ratio:
            highest_ratio = ratio
            highest_term = term
    if highest_ratio > 0.5:
        start_index = input_string.lower().index(highest_term.lower()) + len(highest_term) + 1
        end_index = input_string[start_index:].index("\n") + start_index
        return input_string[start_index:end_index].strip(special_chars).strip()
    return None

# Store Pdf with convert_from_path function
images = convert_from_path('doc.pdf',500, first_page=1, last_page=1, poppler_path=r'C:\Program Files\poppler-23.01.0\Library\bin')

product = Product()
company = Company()

for i in range(len(images)):
    imageName = 'Page'+ str(i) +'.jpg'
    images[i].save(imageName, 'JPEG')
    textData = pytesseract.image_to_string(imageName)

    # Get Product Name 
    if i == 0:
        part_length = len(textData) // 2
        # One third of the string 
        part1 = textData[:part_length]
        product_name = get_matched_data(part1, config.prod_name_config)
        if product_name is not None:
            product.name = product_name
        
        product_code = get_matched_data(part1, config.prod_code_config)
        if product_code is not None:
            product.code = product_code

        # Company information
        company_regex = re.compile(r'Company\s*:\s*(.*)\n')
        telephone_regex = re.compile(r'Telephone\s*:\s*(.*)\n')
        telefax_regex = re.compile(r'Telefax\s*:\s*(.*)\n')
        email_regex = re.compile(r'E-mail\s*address\s*:\s*(.*)\n')

        company.name = company_regex.search(part1).group(1)
        company.telephone = telephone_regex.search(part1).group(1)
        company.fax = telefax_regex.search(part1).group(1)
        company.email = email_regex.search(part1).group(1)
    
    if i == 2:
        break

# convert the object to a dictionary
product_dict = {"name": product.name, "code": product.code}
company_dict = {"name": company.name, "telephone": company.telephone, "fax": company.fax,"email": company.email  }
result = {
    'product_info': product_dict,
    "company_info": company_dict
}

print(json.dumps(result))
    

