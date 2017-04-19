from datasource import RESTDatasource
from datasource import APIKeyException
from datasource import URIParameterException

class SunlightAPI(RESTDatasource):
	def __init__(self):
		apikey = '' #Sunlight doesn't require one!
		super().__init__(apikey)


	def search(self, query, **params):
	'''
	From the Sunlight API documentation:

	Search the full text of legislation, and other fields.
	The query parameter allows wildcards, quoting for phrases, and nearby
	word operators (full reference) You can also retrieve highlighted excerpts,
	and all normal operators and filters.
	This searches the bill’s full text, short_title, official_title, popular_title, 
	nicknames, summary, and keywords fields.

	For a list of fields which can be used for filtering, see:
	https://sunlightlabs.github.io/congress/bills.html .

	Append the desired fields as keys in **params, such as:
	{
		'enacted_as.law_type' : 'private'
	}
	'''
		endpoint = 'https://congress.api.sunlightfoundation.com/bills/search'
		return super().request(endpoint, params, headers)

	def bills(self, **params):
	'''
	The main endpoint of Sunlight for retrieving data about legislation.
	Various parameters can be passed to retrieve bills according to certain criteria.

	For a list of fields which can be used for filtering, see:
	https://sunlightlabs.github.io/congress/bills.html .

		Append the desired fields as keys in **params, such as:
	{
		'enacted_as.law_type' : 'private'
	}
	'''
		endpoint = 'https://congress.api.sunlightfoundation.com/bills'
		return super().request(endpoint, params, headers)
