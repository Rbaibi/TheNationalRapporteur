import PyPDF2

base_path = "/home/jorden/Documents/prive/repositories/nr-incredibles/National Rapporteur Publications/Annual plan 2017/Annual plan 2017 .pdf"

pdfFileObj = open(base_path, 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)


print('Number of pages: ' + str(pdfReader.numPages))

for i in range(pdfReader.numPages):
    page = pdfReader.getPage(i)
    print(page.extractText())
