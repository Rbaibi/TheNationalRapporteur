import os
import re
from nlp_funcs import *
import io

def clean_files():
    source_path = "../data/text_files/raw/"
    dest_path = "../data/text_files/clean/"
    for file in os.listdir(source_path):
        with io.open(source_path + file, "r", encoding="utf-8") as infile:
            text = ""
            for line in infile:
                text = text + line

        text = process_text(text)

        with io.open(dest_path + file, "w", encoding="utf-8") as outfile:
            outfile.write(text)

if __name__ =="__main__":
    clean_files()