# Hackaton for Peace, Justice and Security
# June 14th - 16th, 2019
# Challenge: National Rapporteur
# Team: NRteam1

Note: all code and data is stored on Github (private)
We will discuss with National Rapporteur for providing the data and making the Github public or not

Codes:
1) Main code: Search_NR_PDFs
2) Scraping_All190PDFs_from_website.py
3) PDF_import_NR_HB.py

Main code contains:
# PART I: Preparing the documents/webpages: text cleaning and creating 'alldoclist'(all 130 PDFs text content) and 'plot_data' (3D-list with all PDFs with tokenized words)
# PART II: CREATING THE INVERSE-INDEX: creates 'worddic' (dict with all words: vectorized and in which document(s) it occurs on which position(s) and tfidf)
# PART III: The Search Engine: function 'search'
# PART IV: Rank and return (rules based): function 'rank' based on 5 rules and providing summaries
# CASE I: NR: get all information on a certain topic; e.g. prostitution
# CASE II: Student: get all information about victims/ perpetrators
# CASE III: Media: has NR a point of view taking-in a passport of a delinquent of sexual violence against children so that he/ she is not able to travel.
# PART V: Rank and return (machine learning) - Work in Progress


