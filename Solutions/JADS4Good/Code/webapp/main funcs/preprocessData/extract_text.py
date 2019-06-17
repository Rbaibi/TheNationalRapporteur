from tika import parser
import pandas as pd
import io
import os

def convert_pdf_to_text():
    path_to_pdfs = "../data/PDFS/"
    path_to_save_text = "../data/text_files/raw/"

    for file in os.listdir(path_to_pdfs):

        path_to_open = path_to_pdfs + file
        raw = parser.from_file(path_to_open)
        file_to_save = path_to_save_text + file.strip('.pdf') + ".txt"

        with io.open(file_to_save, "w", encoding="utf-8") as outfile:
            outfile.write(raw['content'])


if __name__ =="__main__":
    convert_pdf_to_text()