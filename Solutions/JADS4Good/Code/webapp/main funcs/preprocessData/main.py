from googletrans import Translator
import os
from spacy_text_summarise import spacy_summarise
from langdetect import detect
from read_pdf import pdf_to_text
from entity import get_entity
import psycopg2


conn = psycopg2.connect("host="+ip_db+" dbname="+db_name+" user="+user+" password="+password)

all_files = []
publication_list = []

path_folder = "../National Rapporteur Publications/"

for dirpath, dirnames, filenames in os.walk(path_folder):
	for filename in [f for f in filenames if f.endswith(".pdf")]:
	#for filename in [f for f in filenames]:
		path_file = os.path.join(dirpath, filename)

		# PUBLICATION AND DOCUMENT NAME
		publication_name = "".join(dirpath.rsplit(path_folder))
		document_title = filename

		print(publication_name)

		
		# Convert PDF to TEXT
		completePDF = pdf_to_text(path_file)
		length_document = len(completePDF)

		# Detect the language of the text
		lan_detected = detect(completePDF)

		#language = None 
		if(lan_detected=="en"):
			language = 'english'
		if(lan_detected=="nl"):
			language = 'dutch'
		
		# If language is detected

		if (language):

			#No of sentences in the summary
			noSentences = 20

			# Summarise using SPACY
			summarySpacyList = (spacy_summarise(completePDF,noSentences,language))
			summarySpacy = '.'.join(summarySpacyList)

			#Array of dict with text and label and most prominent labels
			labelsText = get_entity(completePDF,language,10)
			

			#Translate to check if it makes sense!
			#translator = Translator()
			#summaryEng = translator.translate(summarySpacy).text
			#print(summaryEng)
			#print("*************")

			cursor = conn.cursor()
			cursor.execute('SELECT publication_id FROM publications WHERE heading=%s',[publication_name])
			pub_id = cursor.fetchall()
			pub_id = pub_id[0][0]


			cursor1= conn.cursor()
			cursor1.execute('INSERT INTO documents (document_name,text,publication_id,summary,language,length) VALUES (%s,%s,%s,%s,%s,%s)',
				[document_title,completePDF,pub_id,summarySpacy,language,length_document])
			conn.commit()

			cursor2 = conn.cursor()
			cursor2.execute('SELECT document_id FROM documents WHERE document_name=%s',[document_title])
			doc_id = cursor2.fetchall()
			doc_id = doc_id[0][0]

			labelsText = [dict(y) for y in set(tuple(x.items()) for x in labelsText)]

			for lb in labelsText:
				text_val = (lb['text'])
				label = (lb['label'])

				cursor4= conn.cursor()
				cursor4.execute('INSERT INTO entities (doc_id,text_value,label) VALUES (%s,%s,%s)',
				[doc_id,text_val,label])
				conn.commit()


		else:
			print('Error Reading File: ', filename)

conn.close()



