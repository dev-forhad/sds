import fitz
import pytesseract
import cv2
import numpy as np
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# open the PDF file
pdf_file = "doc.pdf"
doc = fitz.open(pdf_file)

# loop through the pages of the PDF file
for page in doc:
    # get the page as an image
    img = page.getPixmap().getImageData(output="png")

    # perform OCR on the image to extract text
    text = pytesseract.image_to_string(img)

    # check if the text contains the name of the pictogram you are interested in
    if "flammable" in text.lower():
        # convert the image to a format that OpenCV can work with
        img_cv = cv2.imdecode(np.frombuffer(img, np.uint8), -1)

        # use OpenCV to find the contours of the pictogram
        # (you may need to adjust the parameters to get good results)
        contours, hierarchy = cv2.findContours(img_cv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # draw the contours on the image for visualization
        cv2.drawContours(img_cv, contours, -1, (0, 255, 0), 2)
        
        # show the image with the pictogram contours
        cv2.imshow("Image", img_cv)
        cv2.waitKey(0)

# release the resources used by OpenCV
cv2.destroyAllWindows()
