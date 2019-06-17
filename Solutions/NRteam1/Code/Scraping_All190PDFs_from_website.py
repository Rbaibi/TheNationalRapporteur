# Hackaton for Peace, Justice and Security
# June 14th - 16th, 2019
# Challenge: National Rapporteur
# Team: NRteam1

# Goal: Scrape from website all PDFs and store data in file

# Functions:
# Scrape all PDFs with PyPDF2
# Scrape all PDFs with PDFMiner
# Best one: Scrape all PDFs with PDFMiner - in loop to extract pages in a list

# Next Actions:
# -

# Nice to have:
# .doc scraping (doc 157: Persbericht rapportage 2008)


# =============================================================================
# Scrape all PDFs with PyPDF2
# =============================================================================
## Import the libraries
import pandas as pd
import requests
import PyPDF2

## Get information with all PDF urls
df = pd.read_excel(r'output\all_PDFs.xlsx')
len(df) # 190 PDFs
# add Raw_Text field for all content 
df['Raw_Text'] = None 
    
# Loop to extract all PDF data and store it in Raw_Text
for i in range(len(df.urls)): 
#for i in range(0,4):
    url = df.urls[i]
    response = requests.get(url)  
    
    # check if pdf extension:
    if(url[-3:] == 'pdf'):
           
        with open('output/scraped.pdf', 'wb') as f:
            f.write(response.content)
            
        filename = 'output/scraped.pdf'
        pdfFileObj = open(filename,'rb')               # open allows you to read the file
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)   # the pdfReader variable is a readable object that will be parsed
        num_pages = pdfReader.numPages                 # discerning the number of pages will allow us to parse through all the pages
        
        ## Read PDF
        count = 0
        raw_text = ""
        # The while loop will read each page                                                           
        while count < num_pages:                       
            pageObj = pdfReader.getPage(count)
            count +=1
            raw_text += pageObj.extractText()
        
        df.Raw_Text[i] = raw_text
    
    # if not a pdf-extension: do not scrape content 
    else:
        print('\nfile with no PDF extension:', i, '\nURL:', url)
        df.Raw_Text[i] = None

df.columns
# rename and reorder column names
df.columns = ['PDF_name','Publication','Raw_Text']
df = df[['Publication', 'PDF_name', 'Raw_Text']]

## Write to file
#df.to_csv('output/pdf190_content.csv', index=False)
df.to_excel('output/pdf190_content.xlsx', index=False)


# =============================================================================
# Scrape all PDFs with PDFMiner
# =============================================================================
## Import the libraries
import pandas as pd
import requests
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

## Convert function PDFMiner 
def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)
 
    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)
 
    infile = open(fname, 'rb')
    # https://stackoverflow.com/questions/54009871/converting-pdf-to-text-text-extraction-is-not-allowed
#    for page in PDFPage.get_pages(infile, pagenums):
    for page in PDFPage.get_pages(infile, pagenums, password="", check_extractable=False):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text

## Get information with all PDF urls
df = pd.read_excel(r'output\all_PDFs.xlsx')
len(df) # 190 PDFs
# add Raw_Text field for all content 
df['Raw_Text'] = None
   
# Loop to extract all PDF data and store it in Raw_Text
#for i in range(len(df.urls)): 
for i in range(77,78):
    url = df.urls[i]
    response = requests.get(url)  
    
    # check if pdf extension:
    if(url[-3:] == 'pdf'):
    
        with open('output/scraped.pdf', 'wb') as f:
            f.write(response.content)
            
        filename = 'output/scraped.pdf'
        df.Raw_Text[i] = convert(filename)
        f.close()
        
    # if not a pdf-extension: do not scrape content 
    else:
        print('\nfile with no PDF extension:', i, '\nURL:', url)
        df.Raw_Text[i] = None

df.columns
# rename and reorder column names
df.columns = ['PDF_name','Publication','Raw_Text']
df = df[['Publication', 'PDF_name', 'Raw_Text']]

## Write to file
df.to_csv('output/pdfminer190_content.csv', index=False)
df.to_excel('output/pdfminer190_content.xlsx', index=False)
        

# =============================================================================
# Scrape all PDFs with PDFMiner - in loop to extract pages in a list
# =============================================================================
## Import the libraries
import pandas as pd
import requests
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from PyPDF2 import PdfFileReader

## Convert function PDFMiner 
def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)
 
    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)
 
    infile = open(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums, password="", check_extractable=False):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text

## Get information with all PDF urls
df = pd.read_excel(r'output\all_PDFs.xlsx')
len(df) # 190 PDFs
# add Raw_Text field for all content 
df['Raw_Text'] = None

# Loop to extract all PDF data and store it in Raw_Text
for i in range(0,5):
#for i in range(len(df.urls)): 
    url = df.urls[i]
    response = requests.get(url)  
    
    # check if pdf extension:
    if(url[-3:] == 'pdf'):
    
        with open('output/scraped.pdf', 'wb') as f:
            f.write(response.content)
            
        filename = 'output/scraped.pdf'
        pdf = PdfFileReader(open(filename,'rb'))
        nr_pages = pdf.getNumPages()
        pagess = []
        for j in range(nr_pages):
           pagess.append(convert(filename, pages=[j]))
        df.Raw_Text[i] = pagess
        
    # if not a pdf-extension: do not scrape content 
    else:
        print('\nfile with no PDF extension:', i, '\nURL:', url)
        df.Raw_Text[i] = None

df.columns
# rename and reorder column names
df.columns = ['PDF_name','Publication','Raw_Text']
df = df[['Publication', 'PDF_name', 'Raw_Text']]

df.to_pickle('output/pdfminer190_content_per_page.pkl')

## Write to file
df.to_csv('output/pdfminer190_content_per_page.csv', index=False)
df.to_excel('output/pdfminer190_content_per_page.xlsx', index=False)

