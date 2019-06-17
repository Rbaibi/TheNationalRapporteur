import datefinder

def get_dates(text):
	matches = datefinder.find_dates(text)
	for match in matches:
	    return (match)