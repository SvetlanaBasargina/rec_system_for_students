import re
from PIL import Image
import pytesseract
import cv2
import os

def get_test_from_img(file):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

    image = cv2.imread(file)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)

    text = pytesseract.image_to_string(Image.open(filename), lang='rus')
    os.remove(filename)
    return re.sub("^\s+|\n|\r|\s+$", ' ', text)

def get_digits(str1):
    c = ""
    for i in str1:
        if i.isdigit():
            c += i
    return c

def find_score(keywords, text):
    num = get_digits(text)
    res = ''
    if len(num) > 0:
        for word in keywords:
            for n in num:
                if re.search(str(n) + word, text):
                    res = n
    return res

def find_fio(text):
    return re.fullmatch(r'[А-ЯЁ][а-яё]+\s+[А-ЯЁ][а-яё]+(?:\s+[А-ЯЁ][а-яё]+)?', text)



# text1 = get_test_from_img('12345.jpg')
# print(text1)
