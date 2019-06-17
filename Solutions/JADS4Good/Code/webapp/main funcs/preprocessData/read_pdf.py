import PyPDF2

def pdf_to_text_1(path_file):
	reader=PyPDF2.pdf.PdfFileReader(path_file)
	eachPageText=[]
	for i in range(0,reader.getNumPages()):
		pageText=reader.getPage(i).extractText()
		eachPageText.append(pageText)
		completePDF = ' '.join(eachPageText)
		completePDF = completePDF.replace('\n','')
	return(completePDF)


from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import HTMLConverter,TextConverter,XMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import io


def pdf_to_text(path_to_file):
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path_to_file, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return (text)