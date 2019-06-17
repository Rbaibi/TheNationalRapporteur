import os
import json
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
# From PDFInterpreter import both PDFResourceManager and PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
# Import this to raise exception whenever text extraction from PDF is not allowed
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.converter import PDFPageAggregator


def get_pages_from_pdf(file_path):
    # Open and read the pdf file in binary mode
    fp = open(file_path, "rb")

    # Create parser object to parse the pdf content
    parser = PDFParser(fp)

    # Store the parsed content in PDFDocument object
    document = PDFDocument(parser, "")

    # Check if document is extractable, if not abort
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed

    # Create PDFResourceManager object that stores shared resources such as fonts or images
    rsrcmgr = PDFResourceManager()

    # set parameters for analysis
    laparams = LAParams()

    # Create a PDFDevice object which translates interpreted information into desired format
    # Device needs to be connected to resource manager to store shared resources
    # device = PDFDevice(rsrcmgr)
    # Extract the decive to page aggregator to get LT object elements
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)

    # Create interpreter object to process page content from PDFDocument
    # Interpreter needs to be connected to resource manager for shared resources and device
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    page_number = 0
    pages = []

    # Ok now that we have everything to process a pdf document, lets process it page by page
    for page in PDFPage.create_pages(document):
        # As the interpreter processes the page stored in PDFDocument object
        interpreter.process_page(page)
        # The device renders the layout from interpreter
        layout = device.get_result()
        # Out of the many LT objects within layout, we are interested in LTTextBox and LTTextLine
        page_text = ''
        for lt_obj in layout:
            if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                page_text += lt_obj.get_text()

        pages.insert(page_number, page_text)
        page_number += 1

    fp.close()
    return pages


length_treshold = 0.9


# Methods like these make me feel like I'm at a hackathon
def is_new_paragraph_based_on_length(previous_sentence, current_sentence, next_sentence):
    # This statement is a little dangerous.
    if current_sentence[0].isdigit():
        return True

    if next_sentence is None:
        return True

    if previous_sentence is None:
        return False

    if is_line_with_end(current_sentence):
        if len(current_sentence) / len(next_sentence) < length_treshold or len(current_sentence) / len(previous_sentence) < length_treshold:
            return True

    return False


def split_page_to_paragraphs_for_letter(page):
    paragraphs = []
    all_lines = list(filter(lambda x: (len(x) > 1), page.split('\n')))
    end_previous_paragraph = 0
    for index in range(len(all_lines)):
        if is_new_paragraph_based_on_length(safe_get_from_list(all_lines, index - 1), all_lines[index], safe_get_from_list(all_lines, index + 1)):
            paragraphs.append(' '.join(all_lines[end_previous_paragraph:index + 1]))
            end_previous_paragraph = index + 1

    paragraphs_without_newlines = [paragraph.replace('\n', ' ') for paragraph in paragraphs]
    paragraphs_without_short_texts = list(filter((lambda x: (len(x) > 20)), paragraphs_without_newlines))

    if len(paragraphs_without_short_texts) == 0:
        return []
    #  We don't care about the page number.
    if paragraphs_without_short_texts[-1].isdigit():
        return paragraphs_without_short_texts[:-1]

    return paragraphs_without_short_texts


def safe_get_from_list(py_list, index):
    if index < 0:
        return None
    return py_list[index] if index < len(py_list) else None


def is_line_with_end(line):
    return line.rstrip().endswith('.') or line.rstrip().endswith('?') or line.rstrip().endswith('!')


def process_document(file_path):
    extracted_pages = get_pages_from_pdf(file_path)
    all_paragraphs = []

    for page_number, page in enumerate(extracted_pages):
        paragraphs = split_page_to_paragraphs_for_letter(page)
        # Logic to merge two paragraphs from seperate pages
        if len(paragraphs) > 0 and len(all_paragraphs) > 0 and not is_line_with_end(all_paragraphs[-1]['text']) and not isinstance(all_paragraphs[-1]['pagenumber'], (list,)) and not paragraphs[0].isupper():
            # side effect master
            previous_paragraph = all_paragraphs.pop()
            previous_paragraph['text'] += ' ' + paragraphs.pop(0)
            previous_paragraph['pagenumber'] = previous_paragraph['pagenumber']
            all_paragraphs.append(previous_paragraph)

        [all_paragraphs.append({'text': i, 'pagenumber': page_number + 1}) for i in paragraphs]

    print(json.dumps(all_paragraphs))
    return all_paragraphs
