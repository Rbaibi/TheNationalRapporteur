import urllib
import requests

url = "https://www.nationaalrapporteur.nl/binaries/artikel-minderjarige-slachtoffers-in-mensenhandelzaken-dettmeijer-vermeu_tcm23-34810.pdf"

r = requests.get(url)
with open("sample.pdf", "wb") as code:
    code.write(r.content)