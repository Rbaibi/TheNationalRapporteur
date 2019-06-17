from extraction import pdf_parser_pdfminer
import os
import json

with open('extracted_data.json') as json_file:
    data = json.load(json_file)
    print('Processed documents: ' + str(len(data)))


dirs = os.walk(os.getcwd() + '/National Rapporteur Publications')

all_dirs = next(dirs)[1]

print('Found ' + str(len(all_dirs)) + ' directories to parse.')


def is_already_processed(dir_name, file_name):
    for processed_file in data:
        if processed_file['title'] == dir_name and processed_file['fileName'] == file_name:
            return True
    return False


def save_data():
    with open('extracted_data.json', 'w') as json_file:
        json.dump(data, json_file, indent=1)


for dir in all_dirs:
    print('Processing directory: ' + dir)
    all_files = os.listdir(os.getcwd() + '/National Rapporteur Publications/' + dir)
    for file in all_files:
        if not file.endswith('.pdf'):
            print('Filename: ' + file + ' is not a pdf.')
            continue
        elif is_already_processed(dir, file):
            print('Document already procssed: ' + file)
        else:
            paragraphs = pdf_parser_pdfminer.process_document(os.getcwd() + '/National Rapporteur Publications/' + dir + '/' + file)
            print('Directory is: ' + dir + ' and filename is: ' + file)
            created_at = input('What is the creation date?')
            type = input('What is the document type?')
            language = input('What is the document language?')
            data.append(
                {
                    "title": dir,
                    "fileName": file,
                    "createdAt": created_at,
                    "type": type,
                    "language": language,
                    "paragraphs": paragraphs,
                    "captions": []
                }
            )
            save_data()
