import os
from PIL import Image
import pytesseract
from datetime import datetime
from wand.image import Image as wi


# Count number of files of specified type
def count_entities(path, ext="any"):

    if ext == 'any':
        return len(os.listdir(path))
    else:
        count = 0
        end = "." + ext
        for file in os.listdir(path):
            if file.endswith(end):
                count += 1
        return count


# Get average length of words in text
def get_avg_len(txt):

    avg_len = 0
    words = []
    lines = txt.split('\n')

    for line in lines:
        for word in line.split(' '):
            words.append(word)

    for word in words:
        avg_len += len(word)

    avg_len = avg_len / len(words)

    return avg_len


# return text or list of image names obtained as result of ocr
def ocr_img(path, get_opt):

    text_list = []
    image_files = []

    num_jpgs = count_entities(path, 'jpg')
    for i in range(1, num_jpgs+1):
        file_path = path + str(i) + '.jpg'
        if i == 1:
            text = pytesseract.image_to_string(Image.open(file_path).resize((3000, 6200)).convert('1'), lang="nld",
                                               config='--psm 6')
        else:
            text = pytesseract.image_to_string(Image.open(file_path).convert('1'), lang="nld", config='--psm 6')

        if get_avg_len(text) < 3:
            image_files.append(i)
        else:
            text_list.append(text)

    if get_opt == 1:
        return text_list, image_files
    elif get_opt == 2:
        return text_list
    else:
        return image_files


# Save list of text as separate txt files
def save_text_list_to_files(text_list, folder_to_save):
    for i in range(1, len(text_list) + 1):
        with open(folder_to_save + str(i) + ".txt", 'w') as outfile:
            outfile.write(str(text_list[i - 1]))


# Compare two date strings and return
def check_dates(a, b):
    try:
        a = datetime.strptime(a, '%d-%m-%Y')
        b = datetime.strptime(b, '%d-%m-%Y')
    except:
        return False

    if a < b:
        return True
    else:
        return False


def convert_pdf_to_images(pdf_path, upload_folder_path):
    # convert pdf to images and save
    pdf = wi(filename=pdf_path, resolution=300)
    pdf_image = pdf.convert("jpeg")
    page_num = 1
    for img in pdf_image.sequence:
        page = wi(image=img, resolution=300)
        page.save(filename=upload_folder_path + str(page_num) + ".jpg")
        page_num += 1

    # Destroy images
    for img in pdf_image.sequence:
        img.destroy()
    pdf.destroy()
    pdf_image.destroy()


def get_list_of_cases_processed(path):

    # Get list of processed case IDs
    with open(path) as infile:
        exc_file = infile.readlines()

    cases = [item.strip() for item in exc_file]
    return cases

def add_case_id_to_file(file, case_id):
    with open(file, 'a') as outfile:
        outfile.write(case_id + "\n")