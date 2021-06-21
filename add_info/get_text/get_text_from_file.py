import csv

from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import os

def from_file_to_img(startPage, endPage, PDF_file = "d.pdf"):
    pages = convert_from_path(PDF_file, 500)
    image_counter = 1
    for page in range(startPage, endPage+1, 1):
        filename = "page_" + str(image_counter) + ".jpg"
        page.save(filename, 'JPEG')
        image_counter = image_counter + 1
    return image_counter

def write_text(startPage, endPage, PDF_file ):
    image_counter = from_file_to_img(startPage, endPage, PDF_file)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
    filelimit = image_counter - 1
    outfile = "out_text.txt"
    f = open(outfile, "a")

    for i in range(1, filelimit + 1):
        filename = "page_" + str(i) + ".jpg"
        text = str(((pytesseract.image_to_string(Image.open(filename)))))
        text = text.replace('-\n', '')
        f.write(text)

    f.close()

def readCSV(filename='changed_data.csv'):
    mentions = dict()
    with open(filename, encoding='utf-8') as reader:
        file = csv.reader(reader, delimiter=';')
        count= 0
        for line in file:
            if count != 0:
                num = 0
                l = dict()
                for item in line[2:]:
                    num += 1
                    if item != '' and int(item) != 0:
                        l[str(num)] = float(item)
                mentions[line[1]] = l
            count +=1
    return mentions


def ReadFile(filename="input.txt"):
    f = open(filename)
    r = csv.reader(f)
    mentions = dict()
    for line in r:
        user = line[0]
        product = line[1]
        rate = float(line[2])
        if not user in mentions:
            mentions[user] = dict()
        mentions[user][product] = rate
    f.close()
    print(mentions)
    return mentions