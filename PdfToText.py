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

    # Partial match search
    highest_ratio = 0
    highest_term = ""
    for term in search_terms:
        ratio = difflib.SequenceMatcher(
            None, term.lower(), input_string.lower()).ratio()
        if ratio > highest_ratio:
            highest_ratio = ratio
            highest_term = term
    if highest_ratio > 0.5:
        start_index = input_string.lower().index(
            highest_term.lower()) + len(highest_term) + 1
        end_index = input_string[start_index:].index("\n") + start_index
        return input_string[start_index:end_index].strip(special_chars).strip()
    return None


def extract_company_details(text):
    company_name = re.findall(
        r'(?:Company|Company\s*:)[:\s]*(.*?)\n', text, re.IGNORECASE)
    telephone = re.findall(
        r'(?:T\.|Telephone)[:\s]*(.*?)\n', text, re.IGNORECASE)
    email = re.findall(
        r'(?:E-mail address|Email)[:\s]*(\S+@\S+)', text, re.IGNORECASE)
    if len(email) == 0:
        # regular expression pattern to match email address
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        # find all matches in the text
        matches = re.findall(pattern, text)
        email = [matches[0]] if matches else []

    return {
        "company_name": company_name[0].strip() if company_name else None,
        "telephone": telephone[0].strip() if telephone else None,
        "email": email[0].strip() if email else None,
    }


def get_hazard_statements(text):
    pattern = r'H\d+\s+.*?(?=\n\n|\Z)'
    matches = re.findall(pattern, text, re.DOTALL)
    return matches


# Store Pdf with convert_from_path function
images = convert_from_path('pdf/format2.pdf', 500, first_page=1,
                           last_page=1,  poppler_path=r'C:\Program Files\poppler-23.01.0\Library\bin')

product = Product()
company = Company()

for i in range(len(images)):
    imageName = 'Page' + str(i) + '.jpg'
    images[i].save("image/"+imageName, 'JPEG')
    textData = pytesseract.image_to_string("image/"+imageName)

    # Get Product Name
    if i == 0:
        part_length = len(textData) // 2
        # One third of the string
        part1 = textData[:part_length]

        # Hazard Statement
        part2 = textData[len(textData)//2:]
        hazard_statements = get_hazard_statements(part2)
        print(hazard_statements)

        product_name = get_matched_data(part1, config.prod_name_config)
        if product_name is not None:
            product.name = product_name

        product_code = get_matched_data(part1, config.prod_code_config)
        if product_code is not None:
            product.code = product_code

        # Signal Word
        signal_word = get_matched_data(part2, config.signal_word_config)
        if signal_word is not None:
            product.signal_word = signal_word

        print(extract_company_details(part1))

        # Company information

    if i == 2:
        break

# convert the object to a dictionary
product_dict = {"name": product.name, "code": product.code,
                "signal word": product.signal_word}
company_dict = {"name": company.name, "telephone": company.telephone,
                "fax": company.fax, "email": company.email}
result = {
    'product_info': product_dict,
    "company_info": company_dict
}

print(json.dumps(result))
