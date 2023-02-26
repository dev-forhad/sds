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


# Store Pdf with convert_from_path function
images = convert_from_path(
    'pdf/format1.pdf', 500, poppler_path=r'C:\Program Files\poppler-23.01.0\Library\bin')

for i in range(len(images)):
    imageName = 'Page' + str(i) + '.jpg'
    images[i].save("image/"+imageName, 'JPEG')
    textData = pytesseract.image_to_string(imageName)
