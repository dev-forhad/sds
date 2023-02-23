import cv2
import pytesseract

# read the image using OpenCV
image = cv2.imread("page0.jpg")
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# extract text from the image
text = pytesseract.image_to_string(image)

# print the extracted text
print(text)
