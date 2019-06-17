from flask import Flask, flash, request,render_template,send_file
import psycopg2 as psycopg2
import fitz

def split_space(string):
    return string.strip().split('.')[0]


app = Flask(__name__)

from nlp_funcs import sanititize_input

conn = psycopg2.connect("host=128.199.226.170 user=postgres password=getdatabasemirra dbname=jads4good")
cursor = conn.cursor()

conn1 = psycopg2.connect("host=128.199.226.170 user=postgres password=getdatabasemirra dbname=jads4good")
cursor1 = conn1.cursor()

from googletrans import Translator
translator = Translator()


def highlight_terms(pdf_file,search_term):
    """
    Function that highlights search term, synonyms and relevant sentences into a pdf file
    """
    doc = fitz.open(pdf_file)
    n_pages = doc.pageCount
    for i in range(n_pages):
        page = doc[i]
    
        ## Search terms synonyms and relevant sentences
        text_instances = page.searchFor(search_term)
        ## Highlight search terms
        for inst in text_instances:
            highlight = page.addHighlightAnnot(inst)
            
    ### return pdf highlighted
#     doc.save("hgl_"+pdf_file, garbage=4, deflate=True, clean=True)
    return doc

def highlight_wtv(pdf_file,word_to_vec):
    """
    Function that highlights synonyms into a pdf file
    """
    doc = fitz.open(pdf_file)
    n_pages = doc.pageCount
    for i in range(n_pages):
        page = doc[i]
        
        ## Search terms synonyms and relevant sentences
        text_instances = page.searchFor(word_to_vec)

        ## Highlight search terms
        for inst in text_instances:
            highlight = page.addHighlightAnnot(inst)
            highlight.setColors({"stroke":(135/255,206/255,250/255)})
            highlight.update()
            
    ## return pdf_highlighted
    return doc

def highlight_imps(pdf_file,imp_sents):
    """
    Function that highlights relevant sentences into a pdf file
    """
    doc = fitz.open(pdf_file)
    n_pages = doc.pageCount
    for i in range(n_pages):
        page = doc[i]
        
        ## Search relevant sentences
        text_instances = page.searchFor(imp_sents)
        
        ## Highlight relevant sentences
        for impst in imp_sents:
            highlight = page.addHighlightAnnot(impst)
            highlight.setColors({"stroke":(0,1,0)})
            highlight.update()
    ## return pdf_highlighted
    return doc

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'GET':
		return render_template('upload.html')

@app.route('/', methods=['GET', 'POST'])
def index():
	result_emp = ""
	# GET Request
	if request.method == 'GET':
		query = """ SELECT documents.doc_name,documents.doc_type,documents.language,publications.title,publications.publication_date,publications.intro
		,publications.article,
		documents.file_basename,documents.document_id
		FROM documents,publications WHERE documents.publication_id=publications.publication_id order by publications.publication_date"""
		cursor.execute(query)
		result_set = cursor.fetchall()
		number_documents = (len(result_set))

		if(number_documents>10):
			doc_display = 10
		else:
			doc_display = number_documents


		query_emp = """ SELECT name,function,phone,email from employees order by name asc"""
		cursor.execute(query_emp)
		result_emp = cursor.fetchall()

		return render_template('index.html',result_set=result_set,number_documents=number_documents,doc_display=doc_display,result_emp=result_emp,len_emp=0,word_vectors='')
	

	# POST Request
	else:
		doc_type = request.form['type_doc']
		search_term = request.form['zoekterm']
		year_range = request.form['amount']

		year_from = (str(year_range.split('-')[0])+'-01-01').replace(' ','')
		year_to = (str(int(year_range.split('-')[1])+1)+'-01-01').replace(' ','')

		word_vectors = []

		if((doc_type=='All')&(search_term=='')):
			query= """ SELECT documents.doc_name,documents.doc_type,documents.language,publications.title,publications.publication_date,
			publications.intro,publications.article,documents.file_basename,documents.document_id FROM documents,publications 
			WHERE documents.publication_id=publications.publication_id AND publications.publication_date>=%s AND 
			publications.publication_date<%s ORDER BY publications.publication_date"""
			cursor.execute(query,[year_from,year_to])
			result_set = cursor.fetchall()

		if((doc_type!='All') & (search_term=='')):

			query= """ SELECT documents.doc_name,documents.doc_type,documents.language,publications.title,publications.publication_date,
				publications.intro,publications.article,documents.file_basename,documents.document_id FROM documents,publications 
				WHERE documents.publication_id=publications.publication_id 
				AND documents.doc_type=%s AND publications.publication_date>=%s AND publications.publication_date<%s 
				ORDER BY publications.publication_date """
			cursor.execute(query,[doc_type,year_from,year_to])
			result_set = cursor.fetchall()

		len_employees = 0

		if(search_term!=''):
			search_term = sanititize_input(search_term)
			l = list(search_term.split(' '))
			search_term_en = translator.translate(search_term)
			l.append(search_term_en.text)

			if(len(l)>1):
				t = tuple(l)
				query = """ SELECT similar_word FROM keywords WHERE keyword IN {}""".format(t)
				cursor.execute(query)
			else:
				query = """ SELECT similar_word FROM keywords WHERE keyword=%s"""
				cursor.execute(query,[search_term])
				
			
			similar_words = cursor.fetchall()
			word_vectors = []
			for sw in similar_words:
				word_vectors.append(sw[0])
			word_vectors.append(search_term)
			word_vectors.append(search_term_en.text)

			if(doc_type=='All'):
				query = """ SELECT documents.document_id FROM documents,publications WHERE 
				publications.publication_id = documents.publication_id AND publications.publication_date>=%s 
				AND publications.publication_date<%s"""
				cursor.execute(query,[year_from,year_to])
			else:
				query = """ SELECT DISTINCT documents.document_id FROM documents,publications WHERE publications.publication_date>=%s 
				AND publications.publication_date<%s AND publications.publication_id = documents.publication_id AND documents.doc_type=%s"""
				cursor.execute(query,[year_from,year_to,doc_type])

			doc_numbers = cursor.fetchall()

			documents_sel = []
			
			for docs in doc_numbers:
				documents_sel.append(docs[0])

			doc_tuple = tuple(documents_sel)
			search_term_tuple = tuple(word_vectors)

			if(len(word_vectors)>1):

				query = """ SELECT sum(tf_idf_nl.tf_idf),documents.document_id
				FROM tf_idf_nl,documents 
				WHERE documents.document_id IN {}
				AND tf_idf_nl.n_gram_text IN {} 
				AND tf_idf_nl.document_id=documents.document_id 
				GROUP BY documents.document_id""".format(doc_tuple,search_term_tuple)

				cursor.execute(query)
				result_set1 = cursor.fetchall()

				query1 = """ SELECT sum(tf_idf_en.tf_idf),documents.document_id
				FROM tf_idf_en,documents 
				WHERE documents.document_id IN {}
				AND tf_idf_en.n_gram_text IN {} 
				AND tf_idf_en.document_id=documents.document_id 
				GROUP BY documents.document_id""".format(doc_tuple,search_term_tuple)

				cursor1.execute(query1)
				result_set2 = cursor1.fetchall()

				result_set = result_set1+result_set2

			else:

				query = """ SELECT sum(tf_idf_nl.tf_idf),documents.document_id
				FROM tf_idf_nl,documents 
				WHERE tf_idf_nl.document_id=documents.document_id
				AND documents.document_id IN {} 
				AND tf_idf_nl.n_gram_text = %s OR 
				GROUP BY documents.document_id""".format(doc_tuple)

				cursor.execute(query)
				result_set1 = cursor.fetchall()

				query1 = """ SELECT sum(tf_idf_en.tf_idf),documents.document_id
				FROM tf_idf_en,documents 
				WHERE tf_idf_en.document_id=documents.document_id
				AND documents.document_id IN {} 
				AND tf_idf_en.n_gram_text = %s OR 
				GROUP BY documents.document_id""".format(doc_tuple)

				cursor1.execute(query1,[word_vectors[0]])
				result_set2 = cursor1.fetchall()

				result_set = result_set1+result_set2

			
			sorted_result = sorted(result_set,reverse=True)

			doc_list = []

			for sr in sorted_result:
				doc_list.append(sr[1])


			query_files = """SELECT documents.doc_name,documents.doc_type,documents.language,publications.title,publications.publication_date,
					publications.intro,publications.article,documents.file_basename,documents.document_id FROM documents,publications 
					WHERE documents.publication_id=publications.publication_id 
					AND documents.document_id IN {} """.format(tuple(doc_list))

			cursor.execute(query_files)
			result_set = cursor.fetchall()

			query_emp = """ SELECT employees.employee_id,employees.name,employees.function,employees.phone,employees.email,
			tf_idf_employees.tf_idf,tf_idf_employees.n_gram
			FROM employees, tf_idf_employees
			WHERE tf_idf_employees.employee_id=employees.employee_id AND
			tf_idf_employees.n_gram=%s 
			ORDER BY tf_idf_employees.tf_idf desc LIMIT 3"""

			cursor.execute(query_emp,[search_term])
			result_emp = cursor.fetchall()
			len_employees = len(result_emp)

		number_documents = len(result_set)


		if(number_documents>10):
			doc_display = 10
		else:
			doc_display = number_documents


		return render_template('index.html',result_set=result_set,number_documents=number_documents,doc_display=doc_display,result_emp=result_emp,len_emp=len_employees,word_vectors=search_term)

@app.route('/pdf',methods=['GET','POST'])
def readpdf():
	if request.method == 'POST':
		name_file = (request.form['test'])
		#word_vectors = (request.form['word_vec'])
		static_file = 'static/new_pdfs/'+name_file+'.pdf'
		# doc1 = highlight_terms(test_file,search_term)
		#search_terms = word_vectors
		#for i in range(len(search_terms)):
			#if i == 0:
				#file_to_save = 'Data_files/new_file_' + str(i) + '.pdf'
				#doc1 = highlight_terms(static_file,search_terms[i])
				#doc1.save(file_to_save, garbage=4, deflate=True, clean=True)
				#doc1.close()
			#else:
				#file_to_open = 'Data_files/new_file_' + str(i-1) + '.pdf'
				#file_to_save = 'Data_files/new_file_' + str(i) + '.pdf'
				#doc2 = highlight_terms(file_to_open,search_terms[i])
				#doc2.save(file_to_save, garbage=4, deflate=True, clean=True)
				#doc2.close()

		return send_file(static_file, attachment_filename='file.pdf')
		
if  __name__=="__main__":
	app.jinja_env.filters['split_space'] = split_space
	app.run(debug=True)



	
	